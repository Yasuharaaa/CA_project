import sqlite3

def databaseOperate(filename, status):
    conn = sqlite3.connect("./database/test.db3")
    cur = conn.cursor()
    #cur.execute('CREATE TABLE BandSteel(Filename TEXT, status INTERGER)')
    command1 = 'INSERT INTO BandSteel VALUES("' + filename + '",' + str(status) + ')'
    cur.execute(command1)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # filename = 'abc'
    # status = 1
    # command1 = 'INSERT INTO Student VALUES("' + filename + '",' + str(status) + ')'
    # print(command1)
    databaseOperate('abc', 1)