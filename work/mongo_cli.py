# -*- coding: utf-8 -*-
import pymongo,random
import redis
import json
import uuid
import time
import copy
import pandas as pd
from datetime import datetime
import sys
# reload(sys)
# sys.setdefaultencoding("utf8")
# execute mode(testing / dev / prod)
MODE = 'prod'

def select_mode(mode):
    # define different executing mode database connection
    if mode == 'prod':
        host = '172.18.52.209'
        port = 27017
        replicaset = 'spiderrs0'
        readPreference = 'secondaryPreferred'
        authSource = 'crs'
        user = 'crs_read'
        password = 'Cb9nLy7cJb'
        db = 'crs'
        rds_host = '172.18.52.250'
        rds_port = 19000
        rds_db = [0, 1, 2, 3, 4, 5]
    elif mode == 'dev':
        host = ['172.18.19.187:27017', '172.18.19.188:27017']
        port = 27017
        replicaset = 'rs0'
        readPreference = 'secondaryPreferred'
        authSource = 'admin'
        user = 'readwrite'
        password = 'yulore456'
        db = 'crs'
        rds_host = '172.18.19.218'
        rds_port = 6379
        rds_db = [0, 1, 2, 3, 4, 5]
    elif mode == 'testing':
        host = ['172.18.19.187:27017', '172.18.19.188:27017']
        port = 27017
        replicaset = 'rs0'
        readPreference = 'secondaryPreferred'
        authSource = 'admin'
        user = 'readwrite'
        password = 'yulore456'
        db = 'crs'
        rds_host = '172.18.19.101'
        rds_port = 6379
        rds_db = [0, 1, 2, 3, 4, 5]
    else:
        print('参数错误！')
        exit(1)

    base_config = {'host': host,
                   'port': port,
                   'db': db,
                   'replicaset': replicaset,
                   'readPreference': readPreference,
                   'authSource': authSource,
                   'user': user,
                   'password': password}

    call_log_config = copy.deepcopy(base_config)
    call_log_config['collection'] = 'call_log'

    sid_info_config = copy.deepcopy(base_config)
    sid_info_config['collection'] = 'sid_info'

    user_info_config = copy.deepcopy(base_config)
    user_info_config['collection'] = 'user_info'

    phone_bill_config = copy.deepcopy(base_config)
    phone_bill_config['collection'] = 'phone_bill'

    report_config = copy.deepcopy(base_config)
    report_config['collection'] = 'report'
   
    moxie_call_log_config = copy.deepcopy(base_config)
    moxie_call_log_config['collection'] = 'moxie_call_log'
    
    phone_config = copy.deepcopy(base_config)
    phone_config['collection'] = 'phone'
    
    hsu_config = copy.deepcopy(base_config)
    hsu_config['collection'] = 'hsu'

    db_config = {
        'base': base_config,
        'user_info': user_info_config,
        'call_log': call_log_config,
        'sid_info': sid_info_config,
        'phone_bill': phone_bill_config,
        'report': report_config,
        'moxie_call_log': moxie_call_log_config,
        'hsu': hsu_config,
        'phone': phone_config

    }

    redis_config = {
        'host' : rds_host,
        'port' : rds_port,
        'db'   : rds_db
    }
    return db_config, redis_config


class RedisWrapper(object):
    """
    Redis连接类
    """
    def __init__(self,mode=MODE):
        tmp, self.config = select_mode(mode)
        self.conn = None
        self._set_conn()

    def _set_conn(self,db=0):
        conn_pool = redis.ConnectionPool(host=self.config['host'], port=self.config['port'],db=self.config['db'][0])
        self.conn = redis.StrictRedis(connection_pool=conn_pool)

    def get_redis(self):
        return self.conn

# print(RedisWrapper().conn)
redis_conn = RedisWrapper().conn
redis_dev = RedisWrapper(mode='dev').conn

class MongodbConnection(object):
    """
    MongoDB连接类
    """
    def __init__(self, mode=MODE):
        self.conn = None
        self._config, _ = select_mode(mode)
        self._set_conn()

    def _set_conn(self):
        conf_=self._config["base"]
        client = pymongo.MongoClient(conf_['host'], authSource=conf_['authSource'], username=conf_['user'], password=conf_['password'], connect=False)
        self.conn = client[conf_['db']]

    def get_conn(self):
        return {
            'user_info': self.conn[self._config["user_info"]["collection"]],
            'call_log': self.conn[self._config["call_log"]["collection"]],
            'sid_info': self.conn[self._config["sid_info"]["collection"]],
            'report': self.conn[self._config["report"]["collection"]],
            'moxie_call_log': self.conn[self._config["moxie_call_log"]["collection"]],
            'hsu': self.conn[self._config["hsu"]["collection"]],
            'phone': self.conn[self._config["phone"]["collection"]]

        }

db = MongodbConnection().get_conn()
db_dev = MongodbConnection(mode='dev').get_conn()

# def one_in_queue():
#     #sid = 'SID70b9f813e4d54298bdb318a4780b50bd'
# 	#sid_info = db["sid_info"]
#     #res = sid_info.find({'status':0}).sort("_id",-1).limit(300)
#     #sid_list = [x.get('sid') for x in res]
#     #print sid_list
# 	sid_list = ["SIDc528ecb787f4407a990e7c37f47b1258", "SIDffba7de6c4ab3d3d99b2752f971fa1b9", "SID31ff0fccbdf539ba7ea73e192ecf14e9", "SIDb5c3c04d99bb6aa338cb2b556006a03e", "SID5b8f5b6427e4f6a72558932104772e46", "SID869b8a60f5b44818a1cea8547f7ee8c3", "SIDe64167e88d76b45b51a2b345698f48b7", "SIDa372e5758f7d4a998a175b1932dfb01f", "SID4d9cca23194c7113e312719b31b2d2eb", "SID43a83f9377887befd1962bc66cd43718", "SIDf00a426476fc74e00991ce62a53b772a", "SIDce6788777b26321e8a0cba61ac891c72", "SID25fa4a8a910fed014b6ce1ffa6f7803a", "SID86db1bb61d224821b529bf9205b1d1d3", "SID9a6e077fdb51fe3263c0e816c131df24", "SID8ea1fe1db51d44e3a8c4f1b6f4dd4da1", "SID12067a4cd365fc669977b032339f7a84", "SID2a04381ea83946988dbd79cdf9a58577", "SID7238a09cdcc1a1ee684ea0568dcd334a", "SID565c8928b28df8f6be714ba07e14a5c9", "SID0bf1d971b9874e3ab64cffe1a04e8295", "SID9980f4685d70d6d071b7a1301d8d7b73", "SID3d2059efb680f4a84535675ae6cbcdef", "SID24731b09ba01ea148a83f507390d8238", "SIDcacec7381311b60ff3cf72b7741b2764", "SID01051f8d17bd46a2b8bf674e4edd6b50", "SIDabe912ba00be8a2f339ae4da159d0721", "SID1be9330eae89482299779bba09fdfadc", "SID4ec0905dbd1974f93b44f16a76443219", "SID901d243c2c46456d9625acce7ccbef6d", "SID74b59f299a9408da3b32cb73324590d2", "SID1b2b23aa40fd1fda3c3629685989dd26", "SIDf2c0f1ce7dcd11ad13e44e3e35299a20", "SIDe9e664cbb94e40f88ec8da035fc25791", "SIDe7c9f9c8382cc41a30b98bdfebb2cc16", "SIDb04f415edcfd4ed3c4703cd2eb433b72", "SID32fa6de6ca8bcb9bfd31739fb544c82a", "SID60c422dfd17741b4951e18ff272d01e8", "SID92eca4819edda9c504784414e4eb449f", "SID69da74417af3ad1ec08bac6523aecf87", "SID1a7d4cf3af8d36fa283e1a03e7a56243", "SID6bb16995754758681dba4b8f1f3ab50d", "SID3aed7f558d8a5c6abb3aeb45d679db1e", "SIDa5b5bd993e8b05851548d834f1f84846", "SIDb0d64198c0c7a7a7fbc67f8ac339c83d", "SID8afab2556cf341c5712f1d288e6dd773", "SIDb534a1b8124740fe81c2cac7c52f170c", "SID6827ac607c754989a4a72107a3abd3ea", "SID333b0ba89e4344fdafac91322d51a523", "SIDef7c119ceee362c5573699ace4e8614d", "SIDa6d2dd7c06385f9c70ffb72dc38cf7cf", "SID3a7ccdb9f8150b2bf2cb782def44932a", "SID65f292aec0e147248e201ccd4cb64b3a", "SIDa24d7e75da4a43627d0d0f7312946740", "SIDfac47a1de118b7a0ccad0a33ea5ba777", "SIDb29b820a0f2d4394959e4ee5944bfcaf", "SIDc1bae57fc17a47e8be5fdb565898c4f3", "SID08f766cbde069f59481be60daafb141c", "SID49ec5dd4eceefc13943059346e7c472e", "SID5bdaa6ad144bab6d4164375472101ed2", "SIDb5f2921b2761c2f85d3d82897d6d306d", "SIDe7744d1a37cbae4068af64f45b896e7e", "SID4cae00d33de021904c8fc55c28a886ae", "SIDca1cdaf29a9365d6bf73a14c5a71eaa5", "SID2def68dcc9214d9e93bf71e95e8c24d1", "SID07902065dc006aa0a6b5f3494f692dd5", "SID57fb42d2ccd04e73ab25ab8ddb50b1f8", "SID6b05bf527f35449892df966a6fdb125b", "SIDf6047b1a99b06474d5ac6abc1be35965", "SIDe7adfe4283f931a5b67b69aee9130f35", "SID3e2a161aaf1ad6796dbf7344e78a1e39", "SID7cbbd367552c2d587fccaef426b75e69", "SID1e493f8747d305445d48755f783edbaa", "SID4154487d20a44979961d41590505acd4", "SID2109e70fc002069acbd46e12d191f97c", "SID85c02beec6c54dd5bf30bd8c4053f533", "SID2cd1482ea82245218780466604d95ed4", "SIDe1be8c576ad0460e9bf5bec1fe9c21f9", "SID57718991861112b82f3969bc8695a203", "SIDcbdaac327daa4c3f9ca1ca56323237c6", "SID4a93d62846257aaad7497ce6ac1f0217", "SIDd1bd9169a58e4eef9c651f1b8605b720", "SIDc0162671acc537a0d5a6a731940852ce", "SIDbf1c3e2997be4238b1d8b93f56ac9564", "SID4bd40dbe59c84032b260eaa0a9fe10be", "SID4115417cb5b38e59230c4760d831d525", "SID36c93ab8467cf30ad5144f02152d444a", "SIDbbd700149366bfc7bb977da49c676e04", "SID03e93dba1e98443f42437442f525812f", "SID1e67fef748964f2d959805df33958f2f", "SID393e3de4c00f406990952a5e5fafb02e", "SID215e18c382f012f5922d1f79afb50727", "SID2ce9f347be2066117f8595ffbbaaf7db", "SIDbb73d1c2cbd839bcd34b68f6fdeea0c0", "SIDd9dee2affd174cb6a55a926b5bc403ce", "SID6547adf8df924d43a500979455ea2ccd", "SID55b7c77f1ed9412db2ca4b8be853a6aa", "SIDbfe797d5197c409eb68bc29c9b8b8b07", "SID677c371aaf6cc475dba143976fd3cb1f", "SID4ec779a233c4476f99cc3fe481489564", "SID60a028c5e9f54d829a922647cd4e84b5", "SID5a8bd21070fe4b3a843abcf96c41add8", "SID1aaf0773a5eae82297c639a21da06971", "SID47e88f052e95bce81154bbbea3a8b18d", "SIDb08c97a47e28612245fa1737ede9b903", "SID24e926396b3a4bedbc2efad937b0780c", "SIDff946661af794bfa5d2d18ea5b14ead6", "SID654978a240254567a9e78d0d69e73daa", "SIDf5279a71289849ca9082ec4f78a12fa9", "SID6f725fdeae3b4ff38aea233d7b8f63ff", "SID25ec6c82b408683b3d822dac9d5f64ea", "SIDc60983e4b67509bad44fdbdbeed0e2a9", "SID92d9a99b5219e931ef195b2f21cca1d3", "SID46f76ab9ab144cd2ac6162167dcbc125", "SIDb511732a147f94d29f86a87fba1e3806", "SID602700a2f0b943d78e6a73128389e1c3", "SID1baf0d5b3babfdb9b2094209ffea1642", "SID16df0c75d9394556bd13276539cb5230", "SIDe435e7d2a3c34dfd8a75834c21a1cfd2", "SID23023064ab754940b54f61bc95cbeaac", "SID84e93fa9ccfb88969264ef3374b73510", "SIDfb7eece888f54365b5460bec73669102", "SIDfdb8a496bfca4ab2a6a8f1985b3b6345", "SIDfcb3b07701622b8693f0feddebc01c8c", "SIDd5e7377d848045a584e37ba54acc61e6", "SID82e5b6175a6545219d67d908fc7700a3", "SIDbaf469a64ab384a7bc6a1c32ee3c4c02", "SID0faeac8c6c83ed753a093c979b2777c5", "SID80e7396c09984563bd746e6625fb03a4", "SID9dd5116a4e0d49c284582e53e03a3690", "SIDce2f557a71ec4b6991d5b7fd2940ac9c", "SID8742eccaf908483fb20dae2d663a4660", "SID5d62e4f0deec4e5585a98c387b75a337", "SID9731997317a7475880ef366dae22e990", "SID38c0982803d63778e449c0c428e7782d", "SID2152ee14c3cc492996b591d63114a102"]

# 	print(redis_conn.llen("calls_wait_report_que"))
# 	print("====== now enqueue ======")
# 	for sid in sid_list:
# 		print(redis_conn.llen("calls_wait_report_que"))
# 		print("====== now enqueue ======")
# 		queue_data = {
# 			"sid":sid, # sid
#             "need_itag": 1, # 1: 配置邦秒配; 2: 配置不输出邦秒配
# 	    	"need_blank": 3, # 1: 展示静默列表（v3.0.0）；2: 展示静默度（v3.1.1）；3: 展示静默详情（融宝通v3.2.1）
#             "need_id": 1, #1: 配置三要素，2: 不配置三要素
#             "output_report": '1', #1: 配置催收，2: 不配置催收
#             "num":0,# 错误次数
# 			# "report_notify_url":'http://dev-nsm-api.dianhua.cn/crs_authen_notify.php',
# 			# "auth_restrict_key": 'auth_restrict_12_15094393043',
# 			# "auth_restrict_val": str(int(time.time())+60),
# 		}
# 		db["report"].delete_many({'sid':sid})
# 		redis_conn.lpush("calls_wait_report_que",json.dumps(queue_data))
# 		print("====== enqueue pass! ======")
# 		print(redis_conn.lrange("calls_wait_report_que",0,-1))


# def ones_in_queue():
#     sid = 'SID0376f582c00d440e8aac7d56bd1c2c4a'
#     print redis_conn.llen("calls_wait_report_notify")
#     print "====== now enqueue ======"
#     queue_data = {
#         "sid":sid,
#         "need_itag": '1',
#         "status_report": 2,
#         "report_notify_url":'http://dev-nsm-api.dianhua.cn/crs_authen_notify.php'
#     }
#     # db["report"].delete_many({'sid':sid})
#     redis_conn.lpush("calls_wait_report_que",json.dumps(queue_data))
#     print "====== enqueue pass! ======"
#     print
#     print redis_conn.lrange("calls_wait_report_que",0,-1)

# def push_call_log():
#     sid = 'SID72ea2817378844d2bef7d0710acf1bfe'
#     print redis_conn.llen("calls_wait_push_que")
#     print "====== now enqueue ======"
#     queue_data = {
# 		"status": 0,
# 		"message": "OK",
# 		"cid": "21",
# 		"sid": sid,
# 		"uid": "",
# 		"tel": "18228156217",
# 		"call_log_missing_month_list": [],
# 		"call_log_possibly_missing_month_list": [],
# 		"phone_bill_missing_month_list": [],
# 		"call_log_part_missing_month_list": [],
# 		"security_push_service": 0,
# 		"appsecret": "ba23d2d27feb2bd4ef248e35cb49accf85e61538a3e17ceb854db12b7377e862",
# 		"notify_url": "https://japi.cnsuning.com/fgeics/Dianhua/PostData.ajax?source=bmp",
# 		"need_itag": 1
# 	}
# 	# db["report"].delete_many({'sid':sid})
#     redis_conn.lpush("calls_wait_push_que",json.dumps(queue_data))
#     print "====== enqueue pass! ======"
#     print
#     print redis_conn.lrange("calls_wait_push_que",0,-1)

# def batch_in_queue():
#     sid_info = db["sid_info"]
#     res = sid_info.find({'status':0}).sort("_id",-1).limit(300)
#     sid_list = [x.get('sid') for x in res]
#     print sid_list
#     for each in sid_list:
#         db["report"].delete_many({'sid':each})
#         print "====== now enqueue:%s ======"%each
#         queue_data = {
#             "sid":each,
#             "output_report": '1',
#             "need_itag": '1',
#             "num": 0,
#             "need_blank": random.randint(1, 2),
#             # "report_notify_url":'http://dev-nsm-api.dianhua.cn/crs_authen_notify.php',
#             # "auth_restrict_key": 'auth_restrict_12_15094393043',
#             # "auth_restrict_val": str(int(time.time())+60),
#         }
#         redis_conn.lpush("calls_wait_report_que",json.dumps(queue_data))
#         print "====== enqueue pass! ======"

# def batch_select_in_queue():
#     sid_info = db["sid_info"]
#     res = sid_info.find({'end_time':{'$gt':1522684800,'$lt':1522771200}, 'status':0, 'status_report':{'$ne':0}},{'sid':1,'_id':0})
#     sid_list = [x.get('sid') for x in res]
#     print sid_list
#     for each in sid_list:
#         db["report"].delete_many({'sid':each})
#         print "====== now enqueue:%s ======"%each
#         queue_data = {
#             "sid":each,
#             "output_report":'1',
#             "num":0,
#             # "report_notify_url":'http://dev-nsm-api.dianhua.cn/crs_authen_notify.php',
#             # "auth_restrict_key": 'auth_restrict_12_15094393043',
#             # "auth_restrict_val": str(int(time.time())+60),
#         }
#         redis_conn.lpush("calls_wait_report_que",json.dumps(queue_data))
#         print "====== enqueue pass! ======"


# def output_select_call_log():
#     sid_info = db["sid_info"]
#     res = sid_info.find({'status': 0, 'tel_info.flow_type': "10010", "call_log_missing_month_list": [], "call_log_part_missing_month_list": [], "call_log_possibly_missing_month_list": []},{'sid': 1, '_id': 0}).sort("_id", -1).limit(1)
#     sid_list = [x.get('sid') for x in res]
#     print sid_list
#     data_list = list()
#     for i in sid_list:
#         data = list(db["call_log"].find({'sid': i}, {'_id': 0, 'tel': 1, 'call_tel': 1, 'call_time': 1, 'call_duration': 1, 'call_method': 1}))
#         data_list.extend(data)
#         # labels = ['tel','call_number', 'begin_time', 'call_duration', 'ticket_type']
#     df = pd.DataFrame(data_list)
#     df = df.rename(columns={"call_tel": "call_number", "call_time": "begin_time",
#                         "call_duration": "bill_times", "call_method": "ticket_type"})
#     df['ticket_type'] = df['ticket_type'].map(lambda x: '00' if u'主叫' in x else '01')
#     df['begin_time'] = df['begin_time'].map(lambda x: datetime.fromtimestamp(int(x)).strftime('%Y%m%d%H%M%S'))
#     df['called_tel'] = map(lambda x, y, z: x if z == '01' else y,
#                            df['tel'], df['call_number'], df['ticket_type'])
#     df['call_number2'] = map(lambda x, y, z: y if z == '01' else x,
#                            df['tel'], df['call_number'], df['ticket_type'])
#     import pdb; pdb.set_trace()
#     df.to_csv('call_log.csv', encoding='utf-8', index=False)
#         # import pdb; pdb.set_trace()

# def out_rpt_sid_info():
#     sid_info = db["sid_info"]
#     report = db["report"]
    
#     #cmcc = sid_info.find({'status': 0, 'tel_info.flow_type': '10086', 'status_report':0},{'sid':1, '_id':0}).sort("_id", -1).limit(10)
#     #cucc = sid_info.find({'status': 0, 'tel_info.flow_type': '10010', 'status_report':0},{'sid':1, '_id':0}).sort("_id", -1).limit(10)
#     #ctcc = sid_info.find({'status': 0, 'tel_info.flow_type': '10000', 'status_report':0},{'sid':1, '_id':0}).sort("_id", -1).limit(10)
#     #sid_list = [x.get('sid') for x in list(cmcc)+list(cucc)+list(ctcc)]
#     sid_list = []
#     #for i in ['移动', '联通', '电信']:
#     for i in ['电信']:
# 		#for j,k in enumerate([1,1,1,10]):
# 			#tmp = db['report'].find({'cuishou_risk_detection.detection_result':j, 'call_behavior.number_used.telecom': i, 'call_log_group_by_tel':{'$exists':True}, '$where':'this.call_log_group_by_tel.length<350'}).sort("_id", -1).limit(k)
# 		tmp = db['report'].find({'cuishou_risk_detection.detection_result':2, 'call_behavior.number_used.telecom': i, 'call_log_group_by_tel':{'$exists':True}, '$where':'this.call_log_group_by_tel.length<350'}).sort("_id", -1).limit(5)
# 		sid_list += list(tmp)
# 		print sid_list
#     sid_list = [x.get('sid') for x in sid_list]
#     #sid_list = ["SID2bb40e2382f34cfc92f5d8324ac063d8", "SIDdd621b2b90de4e7591961c46e8b42798", "SIDcc8e21db1f1147788af63845a427e8a8", "SIDe50dc7a46a8f4f32ad010ac03a1e9dad", "SID93ab6d123a394e0cadc39f790d5622aa"]
#     print sid_list
#     pat_tel = lambda x: x[:-4]+'*'*len(x[-4:]) if len(x)>5 else '*'*len(x)
#     pat_mix = lambda x: x[:1] + '*'*len(x[1:]) if (x and '运营商' not in x) else '***'
#     pat_open_date = lambda x: '运营商未透露'
#     for i in sid_list:
# 		print '正在插入：{}'.format(i)
# 		sid_info = db["sid_info"].find_one({'sid':i},{'_id':0, 'job_id':0})
# 		call_log = db["call_log"].find({'sid':i},{'_id':0})
# 		report = db['report'].find_one({'sid':i},{'_id':0})
# 		sid_info['cid'] = '306'
# 		sid = 'SID{}'.format(uuid.uuid4()).replace('-', '') 
# 		print 'new_sid:{}'.format(sid)
# 		df = pd.DataFrame(list(call_log))
# 		df['tel'] = df['tel'].map(pat_tel)
# 		df['call_tel'] = df['call_tel'].map(pat_tel)
# 		df['sid'] = df['sid'].map(lambda x:sid)
# 		tel_info = report.get('tel_info')
# 		if tel_info:
# 			report['tel_info']['full_name'] = pat_mix(tel_info.get('full_name'))
# 			report['tel_info']['id_card'] = pat_mix(tel_info.get('id_card'))
# 			report['tel_info']['open_date'] = pat_open_date(str(tel_info.get('open_date')))
# 			report['tel_info']['address'] = pat_mix(tel_info.get('address'))
# 			report['tel_info']['tel'] = pat_tel(tel_info.get('tel'))
# 		user_info = report.get('user_info')
# 		if  user_info:
# 			report['user_info']['user_idcard'] = pat_mix(user_info.get('user_idcard'))
# 			report['user_info']['user_address'] = pat_mix(user_info.get('user_address'))
# 			report['user_info']['user_name'] = pat_mix(user_info.get('user_name'))
# 		call_by_tel = report.get('call_log_group_by_tel')
# 		if call_by_tel:
# 			[ i.update({'format_tel':pat_tel(i.get('format_tel'))}) for i in call_by_tel]
# 			report['call_log_group_by_tel'] = call_by_tel
# 		contact = report.get('calls_sa_by_major_contact')
# 		if contact:
# 			[ i.update({'format_tel':pat_tel(i.get('format_tel'))}) for i in contact]
# 			report['calls_sa_by_major_contact'] = contact
# 		call_by_length = report.get('calls_sa_by_length')
# 		if call_by_length:
# 			[ i.update({'format_tel':pat_tel(i.get('format_tel'))}) for i in call_by_length]
# 			report['calls_sa_by_length'] = call_by_length
# 		call_by_times = report.get('calls_sa_by_times')
# 		if call_by_times:
# 			[ i.update({'format_tel':pat_tel(i.get('format_tel'))}) for i in call_by_times]
# 			report['calls_sa_by_times'] = call_by_times
# 		mergency_contact = report.get('mergency_contact')
# 		if mergency_contact:
# 			[ i.update({'format_tel':pat_tel(i.get('format_tel')),'contact_name':pat_mix(i.get('contact_name'))}) for i in mergency_contact]
# 			report['mergency_contact'] = mergency_contact
# 		call_behavior = report.get('call_behavior')
# 		if call_behavior:
# 			report['call_behavior']['number_used']['open_date'] = pat_open_date(str(call_behavior.get('number_used').get('open_date')))
# 			number_tags = call_behavior.get('number_tags')
# 			if number_tags:
# 				[ i.update({'tel':pat_tel(i.get('tel'))}) for i in number_tags]
# 				report['call_behavior']['number_tags'] = number_tags
# 		report['sid']=sid

# 		db_dev['report'].delete_many({'sid':sid})
# 		db_dev['call_log'].delete_many({'sid':sid})
# 		db_dev['sid_info'].delete_many({'sid':sid})
# 		sid_info['sid'] = sid
# 		db_dev['sid_info'].update({'sid':sid},sid_info, upsert=True)
# 		value = df.values.tolist()
# 		title = df.columns.tolist()
# 		call_log_tmp = map(lambda x:dict(zip(title,x)),value)
# 		with open('{}.json'.format(sid), 'w') as fp:
# 			json.dump(call_log_tmp, fp, indent=4, sort_keys=True)
# 		db_dev['call_log'].insert_many(call_log_tmp)
# 		db_dev['report'].update({'sid':sid},report, upsert=True)
# 		print "完成插入"


# def report_out_queue():
#     ret_json = redis_conn.rpop("calls_wait_report_que")
#     print ret_json,type(ret_json)
#     if not ret_json:
#         ret = json.loads(ret_json)
#         print ret, type(ret)
#     if ret_json:
#         print "====== now dequeue ======"
#         ret = json.loads(ret_json)
#         sid = ret.get("sid")
#         err_times = ret.get("num")
#         # 生成时间不超过5分钟
#         print "====== sid:%s ======"%sid

# def get_month(time_date):
# 	return datetime.fromtimestamp(int(time_date)).strftime('%Y%m')

# def change_call_log_month():
# 	for idx,i in enumerate(sid_list):
# 		print 'deal with : {}/{}'.format(idx,len(sid_list))
# 		data = db["call_log"].find({'sid':i})
# 		time.sleep(1)
# 		for call in data:
# 			#print len(data)
# 			print call
# 			db['call_log'].update({'_id':call.get('_id')},{'$set':{'month':get_month(call.get('call_time'))}})


# def read_queue_len():
#     ret_json = redis_conn.llen("calls_wait_report_que")
#     err_json = redis_conn.llen("error_report_que")
#     notify_json = redis_conn.llen("calls_wait_report_notify")
#     print redis_conn.lrange("calls_wait_report_que", 0, -1)
#     print ret_json
#     #print redis_conn.lrange("error_report_que", 0, -1)
#     print err_json
#     print notify_json

# if __name__ == '__main__':
#     #batch_in_queue()
#     #batch_select_in_queue()
#     #read_queue_len()
#     # for _ in xrange(5):
#         # #one_in_queue()
#     # report_out_queue()
#     #one_in_queue()
#     read_queue_len()
#     # output_select_call_log()
#     #out_rpt_sid_info()
# 	#change_call_log_month()
# 	push_call_log()
