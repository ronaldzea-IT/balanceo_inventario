import openpyxl, json, os
from datetime import datetime

print("Iniciando procesamiento stock externo...")
BASE = os.path.dirname(os.path.abspath(__file__))
ruta   = os.path.join(BASE, "StockExterno.xlsx")
salida = os.path.join(BASE, "stock_externo_cache.json")

COLS_BUSCAR = ["sucursal", "co_art", "articulo", "existencia", "costo", "prov"]

wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
ws = wb.active

idx = {}
encabezado_leido = False
resumen = {}  # (sucursal, sku, desc, prov) -> [sum_exist, sum_ponderado]
filas_procesadas = 0

for fila in ws.iter_rows(values_only=True):
    if not encabezado_leido:
        for i, cell in enumerate(fila):
            if cell is not None:
                cl = str(cell).lower().strip()
                for col in COLS_BUSCAR:
                    if cl == col:
                        idx[col] = i
        encabezado_leido = True
        print(f"Columnas encontradas: {idx}")
        continue

    try:
        suc   = str(fila[idx["sucursal"]]).strip().upper() if fila[idx["sucursal"]] is not None else ""
        sku   = str(fila[idx["co_art"]]).strip()           if fila[idx["co_art"]]   is not None else ""
        desc  = str(fila[idx["articulo"]]).split("*")[0].strip() if fila[idx["articulo"]] is not None else ""
        exist = float(fila[idx["existencia"]] or 0)
        costo = float(fila[idx["costo"]]      or 0) if "costo" in idx else 0.0
        prov  = str(fila[idx["prov"]]).strip()       if "prov" in idx and fila[idx["prov"]] is not None else ""

        if not sku or sku == "None" or not suc:
            continue

        k = (suc, sku, desc, prov)
        if k in resumen:
            resumen[k][0] += exist
            resumen[k][1] += exist * costo
        else:
            resumen[k] = [exist, exist * costo]

        filas_procesadas += 1
        if filas_procesadas % 5000 == 0:
            print(f"  Filas procesadas: {filas_procesadas}")
    except Exception as e:
        continue

wb.close()

print(f"Construyendo JSON con {len(resumen)} registros...")
registros = []
for (suc, sku, desc, prov), v in resumen.items():
    exist = v[0]
    costo_pond = round(v[1] / exist, 4) if exist > 0 else 0.0
    costo_inv  = round(costo_pond * exist, 2)
    registros.append({
        "sucursal":     suc,
        "sku":          sku,
        "descripcion":  desc,
        "existencia":   exist,
        "transito":     0.0,
        "comprometido": 0.0,
        "stock_disp":   exist,
        "costo":        costo_pond,
        "costo_inv":    costo_inv,
        "co_prov":      prov,
        "fuente":       "excel"
    })

with open(salida, "w", encoding="utf-8") as f:
    json.dump({"registros": registros, "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")}, f, ensure_ascii=False)

print(f"LISTO. stock_externo_cache.json generado con {len(registros)} registros.")
