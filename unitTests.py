import pymysql.cursors

db_connect = pymysql.connect(host="localhost", user="root", password="", db="patientivdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
cursor = db_connect.cursor()

sql = "CREATE TABLE IF NOT EXISTS `unit_tests` (id int(11) NOT NULL AUTO_INCREMENT,name varchar(255) COLLATE utf8_bin NOT NULL,weight DEC(11) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
cursor.execute(sql)

def unitTestCreate():
    sql = "insert into unit_tests values (1,'Bobby','22');"
    cursor.execute(sql)

def unitTestRead():
    sql = "select * from unit_tests where id = 1;"
    cursor.execute(sql)
    received_info_dict = cursor.fetchall()
    received_info_string = ','.join(str(v) for v in received_info_dict)
    print(received_info_string)
    return received_info_string

def unitTestPreUpdate():
    sql = "insert into unit_tests values ('','Toby','22');"
    cursor.execute(sql)
    
def unitTestPostUpdate():
    sql = "update top (1) unit_tests set name = 'Tony' where name = '';"
    cursor.execute(sql)
    sql = "select * from unit_tests where id = 2;"
    cursor.execute(sql)
    received_info_dict = cursor.fetchall()
    received_info_string = ','.join(str(v) for v in received_info_dict)
    return received_info_string
unitTestCreate()
unitTestRead()