import sqlite3
import os, sys
import glob, random
from datetime import datetime, timedelta

def db_generate(db_name, vacuum_mode, rows):
    data = []
    sample = ('111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111', '111111111111111111111111')
    
    for i in range(0,rows):
        data.append(sample)
        
    if os.path.exists(db_name):
        os.remove(db_name)

    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    cur.execute(f'PRAGMA auto_vacuum={vacuum_mode}')
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("CREATE TABLE test (AA TEXT, BB TEXT, CC TEXT, DD TEXT, EE TEXT, FF TEXT)")
    sql = "INSERT INTO test (AA, BB, CC, DD, EE, FF) VALUES (?, ?, ?, ?, ?, ?)"
    cur.executemany(sql, data)
    con.commit()
    con.close()

def data_rand_delete(db_name, delete_row):
    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    total_row = cur.execute("SELECT COUNT(*) FROM test").fetchone()[0]
    delete_list = random.sample(range(1, total_row), delete_row)
    delete_list = [[i] for i in (delete_list)]
    
    sql = "DELETE FROM test WHERE rowid=?"
    cur.executemany(sql, delete_list)
    con.commit() 
    con.close()

def vacuum(db_name):
    con = sqlite3.connect(db_name, check_same_thread=False)
    cur = con.cursor()
    cur.execute("VACUUM")
    con.commit()
    con.close()
    
def main():
    n = int(input("1. SAMPLE Generate 2. VACUUM NONE 3. VACUUM FULL 4. VACUUM INCR\n Select Case :"))

    if n == 1: # KU-DBF-AM-02-AV-SAMPLE.sqlite
        db_generate('KU-DBF-AM-02-AV-SAMPLE.sqlite', 0, 2000)
        
    elif n == 2: # KU-DBF-AM-02-AV-NONE.sqlite
        db_generate('KU-DBF-AM-02-AV-NONE.sqlite', '0', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-NONE.sqlite', 100)
        
    elif n == 3: # KU-DBF-AM-02-AV-FULL.sqlite
        db_generate('KU-DBF-AM-02-AV-FULL.sqlite', '1', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-FULL.sqlite', 100)
        vacuum('KU-DBF-AM-02-AV-FULL.sqlite')

    elif n == 4: # KU-DBF-AM-02-AV-INCR.sqlite
        db_generate('KU-DBF-AM-02-AV-INCR.sqlite', '2', 2000)
        for i in range(0, 10):
            data_rand_delete('KU-DBF-AM-02-AV-INCR.sqlite', 100)
        vacuum('KU-DBF-AM-02-AV-INCR.sqlite')

if __name__ == '__main__':
    main()
