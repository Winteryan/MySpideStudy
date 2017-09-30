import pymysql
conn = pymysql.connect(port=3306,
                        user='root',
                        password='123456',
                        db='lucenetest',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute("SELECT * FROM person")
print(cur.fetchall())
cur.close()
conn.close()