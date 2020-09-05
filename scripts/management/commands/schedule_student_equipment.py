import pymysql
import requests
import pytz
from datetime import datetime

MYSQL_CONFIG = {
    'database': 'lingoacedb_snapshot',
    'user': 'datawarehouse',
    'password': '9QRrwR2C*ur&1[}2h-[Z',
    'host': '192.168.3.237',
    'port': 3306
}


class Database(object):

    def __init__(self):
        self.connection = pymysql.connect(**MYSQL_CONFIG)

    def get_cursor(self):
        return self.connection.cursor()

    def query_sql(self, sql):

        cursor = self.get_cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_sql(self, sql):
        cursor = self.get_cursor()
        try:
            result = cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            print('execute sql {} error, e={}'.format(sql, e))
            self.connection.rollback()
            return None
        return result

    def close(self):
        self.connection.close()


tk_equipment_url = 'https://global.talk-cloud.net/WebAPI/getequipment'
authkey = 'ex5lZksGvEmoeC1m'

def get_tk_equipment(tk_class_id):

    params = {
        'key': authkey,
        'serial': tk_class_id
    }
    result = requests.get(tk_equipment_url, params=params)
    res = result.json()
    if res.get('result'):
        print('获取{}学生上课设备信息失败'.format(tk_class_id))
        return None
    return res.get('data')

def schedule_student_equipment():

    start_date = '2020-07-08'
    now_time = datetime.now(tz=pytz.UTC)
    db = Database()

    virtual_class_info_sql = '''select id, tk_class_id from classroom_virtualclass_info where DATE(CONVERT_TZ(start_time, '+00:00', '+08:00'))>='{}' and id>=8382654598010468 and id < 8998617042627400 and status in(3,4)  order by DATE(CONVERT_TZ(start_time, '+00:00', '+08:00'))'''.format(start_date)
    result = db.query_sql(virtual_class_info_sql)
    for r in result:
        virtual_class_id = r[0]
        tk_class_id = r[1]
        delete_virtual_class_sql = '''delete from schedule_student_equipment where virtual_class_id={}'''.format(virtual_class_id)
        db.execute_sql(delete_virtual_class_sql)
        if not tk_class_id:
            continue
        data = get_tk_equipment(tk_class_id)
        if not data:
            continue
        for d in data:
            role = d.get('peerrole')
            if role != '2':
                continue
            try:
                student_user_id = int(d.get('peerid'))
            except:
                print('{}不是正常的学生id'.format(d.get('peerid')))
                continue

            insert_schedule_student_equipment_sql = '''insert into schedule_student_equipment(
            virtual_class_id, student_user_id, ip, country, region, city, osversion, devicemodel, cpuarchitecture, sdkversion, sdkdate, browsername, connecttime, create_time, update_time)
            values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                virtual_class_id, student_user_id, d.get('ip', ''), d.get('country', ''), d.get('region', ''), d.get('city', ''),
                d.get('osversion', ''), d.get('devicemodel', ''), d.get('cpuarchitecture', ''), d.get('sdkversion', ''), d.get('sdkdate', ''),
                d.get('browsername', ''), d.get('connecttime', ''), now_time.strftime('%Y-%m-%d %H:%M:%S'), now_time.strftime('%Y-%m-%d %H:%M:%S')
            )
            insert_result = db.execute_sql(insert_schedule_student_equipment_sql)
            if not insert_result:
                print('{} 执行失败'.format(insert_schedule_student_equipment_sql))
    db.close()


if __name__ == '__main__':
    schedule_student_equipment()