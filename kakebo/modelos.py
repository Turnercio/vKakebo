from datetime import date
from enum import Enum
import csv
import os
import sqlite3

class Movimiento:
    def __init__(self, concepto, fecha, cantidad, id = None):
        self.concepto = concepto
        self.fecha = fecha
        self.cantidad = cantidad
        self.id = id

        self.validar_tipos()
        self.validar_inputs()
        
    def validar_tipos(self):
        if not isinstance(self.concepto, str):
            raise TypeError("Concepto debe ser cadena de texto.")

        if not isinstance(self.fecha, date):
            raise TypeError("Fecha debe ser de tipo date.")
        
        if not (isinstance(self.cantidad, float) or isinstance(self.cantidad, int)):
            raise TypeError("Cantidad debe ser numerica.")

    def validar_inputs(self):
        if self.cantidad == 0:
            raise ValueError("La cantidad no puede ser 0")
        if len(self.concepto) < 5:
            raise ValueError("El concepto no puede estar vacio, o menor de 5 caracteres")   
        if self.fecha > date.today():
            raise ValueError("La fecha no puede ser posterior al dia de hoy")      
        
    def __repr__(self):
        return f"Movimiento: {self.fecha} {self.concepto} {self.cantidad:.2f}"

class Ingreso(Movimiento):     
    def __repr__(self):
        return f"Ingreso: {self.fecha} {self.concepto} {self.cantidad:.2f}"
        
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
         
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha

class Gasto(Movimiento):
    def __init__(self, concepto, fecha, cantidad, categoria, id = None):
        super().__init__(concepto, fecha, cantidad, id)

        self.categoria = categoria
        self.validar_categoria()

    def validar_categoria(self):
        if not isinstance(self.categoria, categoria_gastos):
            raise TypeError("Categoria debe ser categoria_gastos.")
        
    def __repr__(self):
        return f"Gasto ({self.categoria.name:30s}): {self.fecha} {self.concepto} {self.cantidad:.2f}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
         
        return self.concepto == other.concepto and self.cantidad == other.cantidad and self.fecha == other.fecha and self.categoria == other.categoria

class categoria_gastos(Enum):

    NECESIDAD = 1
    CULTURA = 2
    OCIO_VICIO = 3
    EXTRAS = 4

class Dao_CSV:
    def __init__(self, ruta):
        self.ruta = ruta
        if not os.path.exists(self.ruta):
            with open(self.ruta, "w", newline="") as f:
                f.write("concepto,fecha,cantidad,categoria\n")

        self.puntero_lectura = 0

    def grabar(self, movimiento):
        with open(self.ruta, "a", newline="") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"')       

            if isinstance(movimiento, Ingreso):
                #f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},\n")
                writer.writerow([movimiento.concepto, movimiento.fecha, movimiento.cantidad, ""])
            elif isinstance(movimiento, Gasto):
               # f.write(f"{movimiento.concepto},{movimiento.fecha},{movimiento.cantidad},{movimiento.categoria.value}\n")
                writer.writerow([movimiento.concepto, movimiento.fecha, movimiento.cantidad, movimiento.categoria.value])
            

    def leer(self):
        with open(self.ruta, "r") as f:
            reader = csv.DictReader(f)
            contador = 0
            for registro in reader:
                if registro["categoria"] == "":
                    #instanciar ingreso con los datos de registro
                    variable = Ingreso(registro["concepto"], date.fromisoformat(registro["fecha"]), float(registro["cantidad"]))
                elif registro["categoria"] in [str(cat.value) for cat in categoria_gastos]:
                    #instanciar gasto con los datos de registro
                    variable = Gasto(registro["concepto"], date.fromisoformat(registro["fecha"]), float(registro["cantidad"]), categoria_gastos(int(registro["categoria"])))
                if contador == self.puntero_lectura:
                    self.puntero_lectura += 1
                    return variable
                contador +=1
            return None
        
class Dao_sqlite:
    def __init__(self, ruta):
        self.ruta = ruta
        
    def leer(self, ID):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()
        
        query = "SELECT ID, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos WHERE ID = ?"
        
        res = cur.execute(query, (ID, ))
        valores = res.fetchone()
        con.close()
        
        if valores:
            if valores[1] == "I":
                return Ingreso(valores[2], date.fromisoformat(valores[3]), valores[4], valores [0])

            elif valores[1] =="G":
                return Gasto(valores[2], date.fromisoformat(valores[3]), valores[4], categoria_gastos(valores[5]), valores [0])

            
        return None
    
    
    def grabar(self, movimiento):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        if isinstance (movimiento, Ingreso):
            tipo_movimiento = "I"
            categoria = None
        elif isinstance (movimiento, Gasto):
            tipo_movimiento = "G"
            categoria = movimiento.categoria.value
        

        if movimiento.id is None:
            query = "INSERT INTO movimientos (tipo_movimiento, concepto, fecha, cantidad, categoria) VALUES (?, ?, ?, ?, ?)"
            
            #cur.execute(query, ("G", "Pienso para Ron", "2024-05-14", 40, 1))           
            cur.execute(query, (tipo_movimiento, movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria))
        
        else:

            query = "UPDATE movimientos SET concepto = ?, fecha = ?, cantidad = ?, categoria = ? WHERE id = ?"
            cur.execute(query, (movimiento.concepto, movimiento.fecha, movimiento.cantidad, categoria, movimiento.id))

        con.commit()
        con.close()

    def leer_todo(self):
        con = sqlite3.connect(self.ruta)
        cur = con.cursor()

        query = "SELECT id, tipo_movimiento, concepto, fecha, cantidad, categoria FROM movimientos"

        res = cur.execute(query)
        valores = res.fetchall()
        con.close()

        lista_completa = []
        for valor in valores:
            if valor[1] == "I":
                lista_completa.append(Ingreso(valor[2], date.fromisoformat(valor[3]), valor[4], valor[0]))

            elif valor[1] == "G":
                lista_completa.append(Gasto(valor[2], date.fromisoformat(valor[3]), valor[4], categoria_gastos(valor[5]), valor[0]))

        return lista_completa
            