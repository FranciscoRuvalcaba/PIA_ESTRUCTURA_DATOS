import sys
import sqlite3
from sqlite3 import Error

try:
    with sqlite3.connect("BD.db") as conn:
        micursor = conn.cursor()
        micursor.execute("CREATE TABLE IF NOT EXISTS Venta (Folio INTEGER PRIMARY KEY, Fecha TEXT NOT NULL );")
        micursor.execute("CREATE TABLE IF NOT EXISTS Detalle (Venta INTEGER, Descripcion TEXT NOT NULL, Cantidad INTEGER, Precio_Unitario REAL, FOREIGN KEY (Venta) REFERENCES Venta(Folio));")
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    