import tkinter as tk
from tkinter import ttk
from kakebo.vistas import Input, DateInput



root = tk.Tk()
#root.pack_propagate()

marco = tk.Frame(root, width= 200, height=80, background="red")
marco.pack()
#marco.pack_propagate()
lblFecha = tk.Label(marco, text="Fecha:", anchor=tk.NW)
lblFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
varFecha = tk.StringVar()
inpFecha = tk.Entry(marco, textvariable=varFecha)
inpFecha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

i1 = Input(root, "Primer Input", 250, 60)
i1.pack(side=tk.TOP)

i2 = Input(root, "Segundo Input", 250, 60)
i2.pack(side=tk.TOP)

di = DateInput(root, 250, 35)
di.pack(side=tk.TOP)

root.mainloop()