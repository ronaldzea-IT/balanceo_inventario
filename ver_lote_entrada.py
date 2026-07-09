from config import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'saLoteEntrada'
    ORDER BY ORDINAL_POSITION
""")
for r in cur.fetchall():
    print(r)
conn.close()
