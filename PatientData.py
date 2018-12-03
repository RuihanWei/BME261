import pymysql.cursors
import serial

db_connect = pymysql.connect(host="localhost", user="root", password="", db="patientivdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

with db_connect.cursor() as cursor:
    sql = "CREATE TABLE IF NOT EXISTS `patients` (id int(11) NOT NULL AUTO_INCREMENT,name varchar(255) COLLATE utf8_bin NOT NULL,weight DEC(11) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    
    cursor.execute(sql)
    
cursor = db_connect.cursor()

def nurseIO():
    user_objective = input("Please enter one of the following objectives with patient data: create (new), read (observe), update (edit) or weightToArd (send patient weight from Python to Arduino): ")
    
    while(user_objective != 'create' and user_objective != 'read' and user_objective != 'update' and user_objective != 'weightToArd'):
        print("Sorry, that was not a valid option. Please try again.")
        user_objective = input("Please enter one of the following objectives with patient data: create (new), read (observe) or update (edit) or weightToArd (send patient weight from Python to Arduino): ")
    
    if(user_objective == "create"):
        new_name = input("Please enter the new patient's name: ")
        new_weight = input("Please enter the new patient's weight: ")
        sql = "insert into patients VALUES (''," + "\'" + new_name + "\'" + ", " + "\'" + new_weight + "\'" + ");"
        cursor.execute(sql)
    elif(user_objective == "weightToArd"):
        patient_id = int(input("Please enter the id of the patient you are trying to look up: "))
        sql = "select count(*) from patients"
        cursor.execute(sql)
        count_dict = cursor.fetchall()
        count_string = ','.join(str(v) for v in count_dict)
        print(count_string)
        count_string_parsers = []
        for i in range(len(count_string)):
            if count_string[i] == ':':
                count_string_parsers.append(i)
            if count_string[i] == '}':
                count_string_parsers.append(i)
        print(count_string_parsers)
        rows_in_patients = int(count_string[(count_string_parsers[0] + 1):count_string_parsers[1]])
        print(rows_in_patients)
        while(patient_id > rows_in_patients):
            print("Sorry, that was not a valid id. Please try again.")
            patient_id = int(input("Please enter one of the following objectives with patient data: create (new), read (observe) or update (edit): "))
        
        sql = "select * from patients where id =" + str(patient_id) + ";"
        cursor.execute(sql)
        desired_patient_weight = cursor.fetchall()
        desired_patient_weight_string = ','.join(str(v) for v in desired_patient_weight)
        print(desired_patient_weight_string)
        desired_patient_parsers = []
        for i in range(len(desired_patient_weight_string)):
            if(desired_patient_weight_string[i]== "("):
                desired_patient_parsers.append(i)
            if(desired_patient_weight_string[i] == ")"):
                desired_patient_parsers.append(i)
        print(desired_patient_parsers)
        weight_to_send = int(desired_patient_weight_string[(desired_patient_parsers[0] + 2):desired_patient_parsers[1]-1])
        print(weight_to_send)
        
        arduinoData = serial.Serial('COM16', 9600)
        
        print("sending start")
        
        def led_on():
            arduinoData.write(weight_to_send)
        
        led_on()
        print("sending end")

nurseIO()

def unitTestCreate():
    sql = "CREATE TABLE IF NOT EXISTS `unit_tests` (id int(11) NOT NULL AUTO_INCREMENT,name varchar(255) COLLATE utf8_bin NOT NULL,weight DEC(11) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;"
    cursor.execute(sql)    
    sql = "insert into unit_tests values ('','Bobby','22');"
    cursor.execute(sql)

def unitTestRead():
    sql = "select * from unit_tests where id = 1;"
    cursor.execute(sql)
    received_info_dict = cursor.fetchall()
    received_info_string = ','.join(str(v) for v in received_info_dict)
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

db_connect.commit()

db_connect.close()