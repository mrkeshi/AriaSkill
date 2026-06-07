import sqlite3,sys
p='d:/AriaSkill/AriaSkill/BackCode/db.sqlite3'
try:
    conn=sqlite3.connect(p)
    cur=conn.cursor()
    cur.execute("PRAGMA table_info('projects_project')")
    cols=cur.fetchall()
    print('COLUMNS:')
    for c in cols:
        print(c)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects_project'")
    print('\nTABLE EXISTS:', cur.fetchall())
except Exception as e:
    print('ERROR',e)
    sys.exit(1)
finally:
    try: conn.close()
    except: pass
