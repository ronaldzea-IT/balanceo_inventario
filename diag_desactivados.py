# diag_desactivados.py v2 - replica la query normalizada de app.py
import json
from config import get_connection

with open("articulos_desactivados.json", encoding="utf-8") as f:
    items = json.load(f)["items"]
desact = set(tuple(x) for x in items)
print(f"Desactivados en JSON: {len(desact)}")

conn = get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT DISTINCT
        RTRIM(LEFT(s.co_alma, 2)) AS sucursal,
        RTRIM(s.co_art)           AS sku
    FROM dbo.saStockAlmacen s
    WHERE RTRIM(s.co_alma) != '9999'
""")
rows = cur.fetchall()
print(f"Combos distintos (normalizados) en BD: {len(rows)}")
print("Muestra BD:", [(repr(suc), repr(sku)) for suc, sku in rows[:3]])

bd_set = set((sku, suc) for suc, sku in rows)
match = desact & bd_set
print(f"Match JSON vs BD: {len(match)}")

# Los que NO emparejan: ver 5 ejemplos con repr
no_match = list(desact - bd_set)[:5]
print("Ejemplos de JSON sin match:", [(repr(a), repr(s)) for a, s in no_match])

# Sucursales presentes en cada lado
print("Sucursales BD:", sorted(set(s for _, s in bd_set)))
print("Sucursales JSON:", sorted(set(s for _, s in desact)))
cur.close(); conn.close()