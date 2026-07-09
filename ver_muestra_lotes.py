from config import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT TOP 15
        RTRIM(co_alma) AS sucursal,
        RTRIM(co_art)  AS sku,
        numero_lote,
        fecha_expiracion,
        stock_actual
    FROM saLoteEntrada
    WHERE stock_actual > 0
      AND fecha_expiracion IS NOT NULL
    ORDER BY fecha_expiracion ASC
""")
for r in cur.fetchall():
    print(r)

cur.execute("""
    SELECT COUNT(*) FROM saLoteEntrada
    WHERE stock_actual > 0 AND fecha_expiracion IS NOT NULL
""")
print("\nTotal registros con stock y vencimiento:", cur.fetchone()[0])

conn.close()
