# -*- coding: utf-8 -*-
import time
import hashlib
import traceback
import pandas as pd

# 配置
mapping = {
    "cy": [(1, 7), (4, 5)],  # 餐饮（测试）
    # "cy": [(1, 187432), (4, 220703)],  # 餐饮
    "cs": [(2, 48732), (5, 22389), (7, 72084), (8, -1)],  # 催收
    "ys": [(3, 193302), (6, -1)]  # 疑似催收
}


def format_tel(tel):
    if isinstance(tel, str):
        return ''.join(i for i in tel if i.isdigit())
    else:
        return None


def phone_encode(string, method="md5_sha1"):
    try:
        if not string:
            return None
        if 'md5' in method:
            m = hashlib.md5()
            m.update(string.encode(encoding='utf-8'))
            string = m.hexdigest()
            string = string[0:32]
        if 'sha1' in method:
            s = hashlib.sha1()
            s.update(string.encode(encoding='utf-8').upper())
            string = s.hexdigest().upper()
        return string
    except:
        print(traceback.format_exc())
        return None


def cuishou_db_typed(cuishou_file, canyin_file, new_cuishou_db_file):
    try:
        cuishou = pd.read_csv(cuishou_file, header=None, names=['tel', 'type'])
        cs = cuishou[cuishou.type == 1].reset_index(drop=True)
        ys = cuishou[cuishou.type == 2].reset_index(drop=True)
        cy = pd.read_csv(canyin_file, header=None, names=['tel'], dtype=str)
        cy['tel'] = cy.tel.map(format_tel).map(phone_encode)
        cy = cy.dropna().reset_index(drop=True)
        cy['type'] = pd.Series([], dtype=object)
        for types, item in mapping.items():
            tmp = 0
            for k, v in item:
                if v != -1:
                    eval(types).loc[tmp: tmp + v - 1, 'type'] = int(k)
                else:
                    eval(types).loc[tmp:, 'type'] = int(k)
                tmp += v
        cy = cy.dropna()
        df = cy.append(cs).append(ys)
        df.sort_values('type').to_csv('new_cuishou_db', index=False, header=False)
        return df
    except:
        print(traceback.format_exc())
        return None


def main():
    st = time.time()
    df = cuishou_db_typed('cuishou_db', 'canyin.tel', 'new_cuishou_db')
    print(time.time() - st)
    print(df.groupby('type').count())


if __name__ == "__main__":
    main()
