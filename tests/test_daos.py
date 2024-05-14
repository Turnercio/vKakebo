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

from kakebo.modelos import Ingreso, Gasto, categoria_gastos, Dao
from datetime import date
import os

def borrar_fichero(path):
    if os.path.exists(path):
        os.remove(path)

def test_crear_dao():
    ruta = "datos/test_ movimientos.csv"
    borrar_fichero(ruta)
    dao = Dao(ruta)
    assert dao.ruta == ruta

    with open(ruta, "r") as f:
        cabecera  = f.readline()
        assert cabecera == "concepto,fecha,cantidad,categoria\n"
        registro = f.readline()
        assert registro == ""

def test_guardar_ingreso_y_gasto():
    ruta = "datos/test_ movimientos.csv"   
    borrar_fichero(ruta)     
    dao = Dao(ruta)
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

def test_leer_ingreso_y_gasto():
    ruta = "datos/test_ movimientos.csv"   
    with open(ruta, "w", newline="")as f:
        f.write("concepto,fecha,cantidad,categoria\n")
        f.write("Ingreso,1999-12-31,12.34,\n")
        f.write("Gasto,1999-01-01,45.0,4\n")

    dao = Dao(ruta)
    movimiento1 = dao.leer()
    assert movimiento1 == Ingreso("Ingreso", date(1999, 12, 31), 12.34)
    
    movimiento2 = dao.leer()
    assert movimiento2 == Gasto("Gasto", date(1999, 1, 1), 45.0, categoria_gastos.EXTRAS)
    
    movimiento3 = dao.leer()
    assert movimiento3 is None
  