import sqlite3
import os
from PyQt5.QtSql import QSqlDatabase
import pandas as pd
import csv

def databaseOperate(current_status):
    db = QSqlDatabase.addDatabase('QSQLITE')
    conn = sqlite3.connect("./database/baosteel.db")
    cur = conn.cursor()
    # cur.execute('CREATE TABLE BandSteel(Filename TEXT, status INTERGER)')
    # command1 = 'INSERT INTO BandSteel VALUES("' + filename + '",' + str(status) + ')'
    result = cur.execute('select * from data order by  time desc limit 0, 1') #选择最新的一行
    result = result.fetchall()
    # print(result[0])
    with open("./database/database.csv", "a+", newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='unix')

        # 先写入columns_name
        writer.writerow([result[0][1], result[0][0], current_status])

    #if not os.path.exists("./database/FinalDatabase.db"):
    connect = sqlite3.connect("./database/updateDatabase.db")
    cur2 = connect.cursor()
    # try:
    #     cur2.execute('create table data(id text, get_time text, status text)')
    # except:
    # '''insert语句 把一个新的行插入到表中'''
    cur2.execute("insert into data (id, get_time, status) values(?, ?, ?);", (result[0][1], result[0][0], current_status))
    # cur2.commit()
        # cur2.execute('insert into data (id, get_time, status) values(result[1], result[0], current_status)')
    # print(result)
    # for data in result:
    #     print(data)
    connect.close()
    #cur2.close()
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # filename = 'abc'
    # status = 1
    # command1 = 'INSERT INTO Student VALUES("' + filename + '",' + str(status) + ')'
    # print(command1)
    databaseOperate('ok')