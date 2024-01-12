#!/usr/bin/env python3

import scraper
import dbmanager

results = scraper.get_feed()
db_file = "database\database"
conn = dbmanager.create_connection(db_file)
with conn:
    for rec in results:
        dbmanager.create_record(conn, rec.format_as_tuple())

conn.close()
