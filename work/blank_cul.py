# -*- coding:utf-8 -*-
import time
import calendar
import bisect

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime

from mongo_cli import db

# def reset_date_start(date_x, month):
#     date_x = date_x + relativedelta(months=month)
#     date_x = "%d-%02d-01 00:00:00"%(date_x.year, date_x.month)
#     return datetime.strptime(date_x, "%Y-%m-%d %H:%M:%S")

# def reset_date_end(date_y, month):
#     date_y = date_y + relativedelta(months=month)
#     date_y_days = calendar.monthrange(date_y.year, date_y.month)[1]
#     date_y = "%d-%02d-%02d 23:59:59"%(date_y.year, date_y.month, date_y_days)
#     return datetime.strptime(date_y, "%Y-%m-%d %H:%M:%S")

BLANK_DEGREE_MAP = {
    'blank_times_count_30': ([0, 1, 2, float('inf')], [0,1,2,3], 0.3), #0.3
    'blank_times_count_90': ([1, 3, 6, float('inf')], [0,1,2,3], 0.25), #0.25
    'blank_times_count_180': ([1, 5, 12, float('inf')], [0,1,2,3], 0.15), #0.15
    'blank_times_count_max': ([120, 240, 480, float('inf')], [0,1,2,3], 0.3) #0.3
}

RESULT_MAPPING = ([0, 1, 2, 3], [0,1,2,3])

import time
# 时间字符串转时间戳（datetimeStr to timestamp）
def dateStrToTimestamp(str_, frmt='%Y-%m-%d %H:%M:%S'):
#     return time.mktime(datetime.strptime(str_, frmt).timetuple())
    return time.mktime(time.strptime(str_, frmt))

def cut_months(term, nums=3, frmt="%Y%m"):
    return [(datetime.strptime(term, frmt) - relativedelta(months=i)).strftime(frmt) for i in xrange(0, nums)]

class CulBlankTime(object):

    def __init__(self):
        self.count_30 = 0
        self.count_90 = 0
        self.count_180 = 0
        self.lenth = 0
        self.max_start = ''
        self.blank_times_list = []
        self.times = []
        self.open_date = ""
        self.last_time = ""
        self.missing_list = []
        
    def _get_data(self, sid):
        data = db['moxie_call_log'].find_one({'sid':sid})
        calls = [dateStrToTimestamp(j.get('time')) for i in data['calls'] for j in i.get('items')]  # 2018-10-31 10:42:05
        smses = [dateStrToTimestamp(j.get('time')) for i in data['smses'] for j in i.get('items')]  # 2018-10-31 10:42:05
        nets = [dateStrToTimestamp(j.get('time')) for i in data['nets'] for j in i.get('items')]  # 2018-10-31 10:42:05
        self.times = calls + smses + nets
        open_date = data.get("open_time", "") # 2015-06-08
        self.open_date = dateStrToTimestamp(open_date, frmt="%Y-%m-%d") if open_date else ""
        self.missing_list =[k for k,v in data.get("month_info").get("month_list").iteritems() if v == -1]
#         print self.missing_list
        last_time = data.get("last_modify_time", "")
        self.last_time = dateStrToTimestamp(last_time) if last_time else float(int(time.time()))
#         return times, open_date, missing_list

    def deal_blank(self, sid):
        self._get_data(sid)
        blank_ret = self.times
        open_date = self.open_date
        # 添加最近时间
        blank_ret.append(self.last_time)
        # 处理有开卡日期情况
        if open_date not in ['', u'运营商未透露']:
            query_date = datetime.today() + relativedelta(months=-5)
            query_month = query_date.strftime("%Y%m")
            first_month = query_date.strftime('%Y-%m-01 00:00:00')
            time_first = time.mktime(time.strptime(first_month, "%Y-%m-%d %H:%M:%S"))
            if float(open_date) > time_first:
                time_first = float(open_date)
            else:
                # 处理首月缺失情况，以第一条记录所在月份为第一月
                if query_month in self.missing_list:
                    query_date = datetime.fromtimestamp(blank_ret[0])
                    first_month = query_date.strftime('%Y-%m-01 00:00:00')
                    time_first = time.mktime(time.strptime(first_month, "%Y-%m-%d %H:%M:%S"))
            blank_ret.append(time_first)
#         lens = (len(blank_ret),len(set(blank_ret)))
        reduce(self.count_times, sorted(set(blank_ret)))
        
        # 计算静默度
        cul_data = {
            "blank_times_count_30": str(self.count_30),
            "blank_times_count_90": str(self.count_90),
            "blank_times_count_180": str(self.count_180),
            "blank_times_count_max": "{:.2f}".format(self.lenth),
        }
#         print cul_data
#         blank_times_degree = self._cul_blank_degree(cul_data)
        return {'sid':sid, 'data':cul_data}

    def _cul_blank_degree(self, data):
        score_total = 0
        for k, v in BLANK_DEGREE_MAP.items():
#             print v,data[k]
            idx = bisect.bisect_left(v[0], int(float(data[k])))
#             print idx
            score_total += v[1][idx]*v[2]
#         print score_total
        idx_result = bisect.bisect_left(RESULT_MAPPING[0], score_total)
        return RESULT_MAPPING[1][idx_result]
    
    def reset_date_start(self, date_x, flag):
        if flag:
            date_x = date_x + relativedelta(months=1)
            if date_x.strftime("%Y%m") not in self.missing_list:
                return date_x.replace(day=1,hour=0,minute=0,second=0)
            else:
                return self.reset_date_start(date_x, flag)
        else:
            date_x = date_x + relativedelta(months=-1)
            if date_x.strftime("%Y%m") not in self.missing_list:
                date_x = date_x + relativedelta(months=1)
                return date_x.replace(day=1,hour=0,minute=0,second=0)
            else:
                return self.reset_date_start(date_x, flag)
        
    def count_times(self, x, y):
        """
        计数缄默时间
        """
#         lenth_day = int((y-x)/86400)
        # 当月&近3月
        local_mon = datetime.now().strftime("%Y%m")
        recent_3m = cut_months(local_mon)
        date_x = datetime.fromtimestamp(x)
        date_y = datetime.fromtimestamp(y)
        month_x = date_x.strftime("%Y%m")
        month_y = date_y.strftime("%Y%m")
#         print date_x,date_y
        lenth_day = date_y - date_x
        common_list = []
        #处理日期在缺失列表内
        if self.missing_list:
            # 处理边界数据
            if month_x in self.missing_list and month_y in self.missing_list:
                date_x = self.reset_date_start(date_x, 0)
                date_y = self.reset_date_start(date_y, 1)
            elif month_x in self.missing_list:
                date_x = self.reset_date_start(date_x, 1)
            elif month_y in self.missing_list:
                date_y = self.reset_date_start(date_y, 0)
            lenth_day = date_y - date_x
#             print date_x, date_y
            # 组建判定月份
            dates = [dt.strftime("%Y%m") for dt in rrule(freq=MONTHLY, dtstart=date_x, bymonthday=-1).between(date_x, date_y)]
#             print 'dates', dates
            # 如判断月份为当月，list增加当月
            if date_y.month == datetime.now().month and local_mon not in dates:
                dates.append(local_mon)
            # 获取需减去月份
            common_list = list(set.intersection(set(dates),set(self.missing_list)))
#             print 'common_list', common_list
            # 重新生成静默天数
            if local_mon in common_list:
                common_list.remove(local_mon)
                remove_day = date_y - datetime.strptime(local_mon,'%Y%m')
                lenth_day -= remove_day
        blank_day = lenth_day.days
        remain_hours = float(lenth_day.seconds*1.0/3600)
        blank_day -= sum([calendar.monthrange(int(query_date[:4]), int(query_date[-2:]))[1] for query_date in common_list if query_date ])
#         print 'blank_day', blank_day
        if blank_day >= 3:
            lenth_hour = blank_day*24 + remain_hours
            blank_tuple = (str(int(time.mktime(date_x.timetuple()))), str(
                int(time.mktime(date_y.timetuple()))), "{:.2f}".format(lenth_hour))
            self.blank_times_list.insert(0, blank_tuple)
            if x > self.last_time - 2592000:
                self.count_30+=1
            if x > self.last_time - 7776000:
                self.count_90+=1
#             if month_x == local_mon:
#                 self.count_30+=1
#             if month_x in recent_3m:
#                 self.count_90+=1
            self.count_180+=1
            if lenth_hour > self.lenth:
                self.lenth = lenth_hour
                self.max_start = str(int(time.mktime(date_x.timetuple())))
        return y