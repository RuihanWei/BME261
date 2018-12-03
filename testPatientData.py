import pytest
import unittest
import pymysql
import io
from unitTests import unitTestCreate
from unitTests import unitTestPostUpdate
import mock

db_connect = pymysql.connect(host="localhost", user="root", password="", db="patientivdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
cursor = db_connect.cursor()

#@mock.patch('builtins.input', side_effect=['weightToArd', '2'])
def test_read_patient():
    sql = "select * from unit_tests where id = 1;"
    cursor.execute(sql)
    received_info_dict = cursor.fetchall()
    received_info_string = ','.join(str(v) for v in received_info_dict)
    assert received_info_string in "{'id': 1, 'name': 'Bobby', 'weight': Decimal('22')}"