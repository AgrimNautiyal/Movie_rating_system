import sqlite3

with sqlite3.connect('softwareproject.db') as con:
        cur =con.cursor()
        cur.execute('''SELECT* FROM User_Info''')
        rows = cur.fetchall()
print(rows)
