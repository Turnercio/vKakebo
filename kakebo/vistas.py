import tkinter as tk
from tkinter import ttk
from datetime import date
from kakebo import WIDTH, PAD_DEFAULT
from kakebo.modelos import CategoriaGastos

class Input(tk.Frame):
    def __init__(self, parent, labelText, W, H):
        super().__init__(parent, width=W, height=H)
        self.pack_propagate(False)
        lbl = tk.Label(self, text=labelText, anchor=tk.W, width=10)
        lbl.pack(side=tk.LEFT)

        self.caja_input = tk.Entry(self)
        self.caja_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def bind(self, event_type, callback):
        print("ksks")
        self.caja_input.bind(event_type, callback)

        
class NumberInput(Input):
    def __init__(self, parent, labelText, W, H):
        super().__init__(parent, labelText, W, H)

        validate_input = self.register(self.__validate_input)
        self.caja_input.config(validate="key", validatecommand=(validate_input, "%P"))

    def __validate_input(self, candidato):

        if candidato in ("", "-"):
            return True
       
        try:
            float(candidato)
            return True
        except ValueError:
            return False
    @property
    def value(self):
        if self.caja_input.get() in ("", "-"):       
            None
        else:
            return float(self.caja_input.get())
        
        """
        1. Evaluar si se puede convertir en flotante. si no devolvemos false
        2. Si es valcio debe devolver true
        """

class selectInput(tk.Frame):
    def __init__(self, parent, labelText, W, H, options):
        super().__init__(parent, width=W, height=H)
        self.pack_propagate(False)
         
        tk.Label(self, text=labelText, anchor=tk.W, width=10).pack(side=tk.LEFT)

        self.selected = tk.StringVar()
        valores_opciones = []
        for cadena in options:
            valores_opciones.append(cadena.name)

        self.caja_input = ttk.Combobox(self, values=valores_opciones,
                                       textvariable=self.selected,
                                       state="readonly")
        self.caja_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class DateInput(tk.Frame):
    def __init__(self, parent, W, H, text="Fecha:"):
        super().__init__(parent, width=W, height=H)
        self.pack_propagate(False)
        
        self.fecha = date.today()
        
        lbl = tk.Label(self, text=text, width=10, anchor=tk.W)
        lbl.pack(side=tk.LEFT)
       
        validate_day = self.register(self.__validate_day)
        self.dayEntry = tk.Entry(self, width=2, validate="key", 
                                 validatecommand=(validate_day, "%P"))
        self.dayEntry.pack(side=tk.LEFT)
        #self.dayEntry.insert(0, f"{self.fecha.day:02d}")
        
        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)
        
        validate_month = self.register(self.__validate_month)
        self.monthEntry = tk.Entry(self, width=2, state=tk.DISABLED,
                                   validate="key",
                                   validatecommand=(validate_month, "%P"))
        self.monthEntry.pack(side=tk.LEFT)
        #monthEntry.insert(0, f"{self.fecha.month:02d}")
        
        lbl = tk.Label(self, text="/", width=3)
        lbl.pack(side=tk.LEFT)
        
        validate_year = self.register(self.__validate_year)
        self.yearEntry = tk.Entry(self, width=4, state=tk.DISABLED,
                                  validate="key",
                                  validatecommand=(validate_year, "%P"))
        self.yearEntry.pack(side=tk.LEFT)
        #yearVar.insert(0, self.fecha.year)
        
    def __validate_day(self, candidato):

        """
        0. Siempre la fecha en blanco.
        1. comprobar que candidato es un entero, si no lo es devolver false
        2. Obligamos a rellenar de forma secuencial. 
        3. Aceptamos valores entre 1 y 31
            3.1 debemos habilitar el mes
        4. Si el campo esta vacio debemos deshabilitar mes y año
        """
        print("por aqui pasa", (candidato))
        
        if not candidato.isdigit() and candidato != "":
            return False 

        if candidato == "":
            self.monthEntry.config(state=tk.DISABLED)
            return True
        
        if int(candidato) > 0 and int(candidato) < 32:
            self.monthEntry.config(state=tk.NORMAL)
            return True
        else:
            return False

    def __validate_month(self, candidato):
        """
        0. El mes empieza en blanco
        1. comprobar que es un entero, si no lo es devolver false
        2. El mes tiene que ser compatible con el dia introducido o devolver false y, logicamente entre 1 y 12
        3. Habilitamos año si el campo no esta vacio
        """
        
        if not candidato.isdigit() and candidato != "":
            return False 
        
        if candidato == "":
            self.yearEntry.config(state=tk.DISABLED)
            return True
        
        try:
            date(2000, int(candidato), int(self.dayEntry.get()))
            self.yearEntry.config(state=tk.NORMAL)
            return True
        except ValueError:
            return False
        
    def __validate_year(self, candidato):
        """
        0. El año empieza en blanco
        1. comprobar que es un entero, si no lo es devolver false
        2. comprobar el año con el mes y el dia introducidos solo si el año tiene longitud 4
        
        """
        if not candidato.isdigit() and candidato != "":
            return False 
        
        if len(candidato) < 4:
            return True
        
        try:
            date(int(candidato), int(self.monthEntry.get()), int(self.dayEntry.get()))
            return True
        except ValueError:
            return False
        
        return True


class FormMovimiento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=WIDTH, height=250, padx=PAD_DEFAULT, pady=PAD_DEFAULT)
        self.pack_propagate(False)
        
        self.fecha = DateInput(self, 550, 40 )
        self.fecha.pack(side=tk.TOP)

        self.concepto = Input(self, "Concepto", WIDTH, 40)
        self.concepto.pack(side=tk.TOP)

        self.cantidad = NumberInput(self, "Cantidad", WIDTH, 40)
        self.cantidad.pack(side=tk.TOP)
        self.cantidad.bind("<Key>", self.__control_categoria)

        self.categoria = selectInput(self, "Categoria", WIDTH, 40, CategoriaGastos)
        self.categoria.pack(side=tk.TOP)

        fr = tk.Frame(self, pady=PAD_DEFAULT, height=40)
        fr.pack(side=tk.TOP, expand=True, fill=tk.X)

        btnCancelar = tk.Button(fr, text="Cancelar")
        btnCancelar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        btnAceptar = tk.Button(fr, text="Aceptar")
        btnAceptar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def __control_categoria(self, evento):
        print(self.cantidad.value)