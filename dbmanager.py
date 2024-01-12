#!/usr/bin/env python3

import sqlite3
# db_file = 'home/Kiermasz/projects/station/enviro.db'
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn
    
def create_record(conn, record):
    sql = ''' INSERT INTO galaxus(timestamp,event_type,product,supplier,price,location,url,description)
				VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, record)
    conn.commit()
    return cur.lastrowid

def lookup_last_records(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM galaxus")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows