"""
1. crear un dao y comprobar que:
    1.1 Tiene una ruta de fichero fijada a un fichero csv
    1.2 El fichero csv tiene que ser vacio pero tener una fila de cabecera

2. Guardar un ingreso y un gasto
    2.1 El fichero contiene las filas adecuadas, 1 de cabecera y una de ingreso y otra de gasto
            (crear metodo grabar)

3. leer datos del fichero con un DAO:
    3.1 Preparar un fichero con datos
    3.2 Leer esos datos con el DAO
    3.3 Comprobar que nos ha creado tantos movimientos (ingreso o gastos) como hay
"""

from kakebo.modelos import Ingreso, Gasto, categoria_gastos, Dao_CSV, Dao_sqlite
from datetime import date
import os
import sqlite3

RUTA_SQLITE = "datos/movimientos_test.db"


def borrar_fichero(path):
    if os.path.exists(path):
        os.remove(path)

def borrar_movimientos_sqlite():
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "DELETE FROM movimientos;"
    cur.execute(query)
    con.commit()
    con.close()  

def test_crear_dao_csv():
    ruta = "datos/test_ movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao_CSV(ruta)
    assert dao.ruta == ruta

    with open(ruta, "r") as f:
        cabecera  = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_ingreso_y_gasto_csv():
    ruta = "datos/test_ movimientos.csv"   
    borrar_fichero(ruta)     
    dao = Dao_CSV(ruta)
    ing = Ingreso("Concepto", date(1988, 12, 31), 12.34)
    dao.grabar(ing)
    gasto = Gasto("Gasto conceptual", date(2000, 1, 1), 23.45, categoria_gastos.EXTRAS)
    dao.grabar(gasto)

    with open(ruta, "r") as f:
        f.readline()
        registro = f.readline()
        assert registro == "Concepto,1988-12-31,12.34,\n"
        registro = f.readline()
        assert registro == "Gasto conceptual,2000-01-01,23.45,4\n"
        registro = f.readline()
        assert registro == ""

def test_leer_ingreso_y_gasto_csv():
    ruta = "datos/test_ movimientos.csv"   
    with open(ruta, "w", newline="")as f:
        f.write("concepto,fecha,cantidad,categoria\n")
        f.write("Ingreso,1999-12-31,12.34,\n")
        f.write("Gasto,1999-01-01,45.0,4\n")

    dao = Dao_CSV(ruta)
    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("Ingreso", date(1999, 12, 31), 12.34)
    
    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Gasto", date(1999, 1, 1), 45.0, categoria_gastos.EXTRAS)
    
    movimiento3 = dao.leer()
    assert movimiento3 is None
  

def test_crear_dao_sqlite():
    ruta = RUTA_SQLITE
    dao = Dao_sqlite(ruta)

    assert dao.ruta == ruta

def test_leer_dao_sqlite():
    #preparar la tabla movimientos como toca, borrar e insertar un ingreso y un gasto

    borrar_movimientos_sqlite()
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()
    query = "INSERT INTO movimientos (ID, tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?)"

    cur.executemany(query, ((1, "I", "Un ingreso cualquiera", date(2024, 5, 14), 100, None), (2, "G", "Gasto sorpresa", date(2024, 5, 1), 123, 3)))
    
    con.commit()
    con.close()
    
    dao = Dao_sqlite(RUTA_SQLITE)
    movimiento = dao.leer(1)
    assert movimiento == Ingreso("Un ingreso cualquiera", date(2024, 5, 14), 100)
    
    movimiento = dao.leer(2)
    assert movimiento == Gasto("Gasto sorpresa", date(2024, 5, 1), 123, categoria_gastos.OCIO_VICIO)

def test_grabar_sqlite():
    
    borrar_movimientos_sqlite()
    
    ing = Ingreso ("Un concepto cualquiera", date(1990, 1, 1), 123)
    dao = Dao_sqlite(RUTA_SQLITE)
    dao.grabar(ing)
    
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()
   
    query = "SELECT ID, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos order by ID desc;"
    res = cur.execute(query)   
    fila = res.fetchone()
    con.close()
    
    
    assert fila[1] == "I"
    assert fila[2] == "Un concepto cualquiera"
    assert fila[3] == "1990-01-01"
    assert fila[4] == 123.0
    assert fila[5] == None



def test_update_sqlite():

    borrar_movimientos_sqlite()
    con = sqlite3.connect(RUTA_SQLITE)
    cur = con.cursor()

    query = "INSERT INTO movimientos (ID, tipo_movimiento, concepto, fecha, cantidad) VALUES (1, 'I', 'concepto original', '0001-01-01', 0.1)"
    cur.execute(query)
    con.commit()
    con.close()

    dao = Dao_sqlite(RUTA_SQLITE)

    movimiento = dao.leer(1)
    movimiento.concepto = "Concepto cambiado"
    movimiento.fecha = "2024-01-04"
    movimiento.cantidad = 32

    dao.grabar(movimiento)

    #comprobar la modificacion

    modificado = dao.leer(1)

    assert isinstance(modificado, Ingreso) 
    assert modificado.concepto == "Concepto cambiado"
    assert modificado.fecha == date(2024, 1, 4)
    assert modificado.cantidad == 32.0