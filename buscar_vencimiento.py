from config import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME LIKE '%venc%' OR COLUMN_NAME LIKE '%lote%'
    ORDER BY TABLE_NAME, COLUMN_NAME
""")
for r in cur.fetchall():
    print(r)
conn.close()
