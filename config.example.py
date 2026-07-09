"""
Plantilla de configuracion. Copia este archivo como config.py
y coloca las credenciales reales. config.py NUNCA se sube a GitHub.
"""
import pyodbc

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=TU_SERVIDOR_AQUI;"
        "DATABASE=TU_BASE_DE_DATOS_AQUI;"
        "UID=TU_USUARIO_AQUI;"
        "PWD=TU_CONTRASENA_AQUI;"
    )
    return pyodbc.connect(conn_str)
