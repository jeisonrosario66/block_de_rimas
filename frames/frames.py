import tkinter as tk

import customtkinter

class topFrame(customtkinter.CTkFrame):
    """Frame principal, sera renderizado desde "./main.py"

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Constantes
        self.ancho = 430
        self.alto = 500

        # ------------------------- Box input texto ------------------------------ start
        # **kwargs: Necesario para lograr la sincronizacion con el "scrollbar"
        # activate_scrollbars=False: desactiva el "scrollbar" integrado de este frame
        self.textBoxWrite = customtkinter.CTkTextbox(
            self, **kwargs, width=self.ancho, height=self.alto, corner_radius=5, activate_scrollbars=False
        )
        self.textBoxWrite.grid(row=0, column=0)
        self.textBoxWrite.insert("0.0", "Some example text!\n" * 50)
        # Evento: cada vez que se suelta cualquier tecla -> Ejecuta funcion
        self.textBoxWrite.bind("<KeyRelease>", self.sincronizaTexto)
        # ------------------------- Box input texto ------------------------------ end
        
        # ------------------------- Box oupot texto ------------------------------ start
        # Box ouput texto analizado (Por implementar mejor)
        # textReadStart: almacena el conteneido de textBoxWrite al inico del programa
        textReadStart = self.textBoxWrite.get("1.0", "end")
        self.textBoxRead = customtkinter.CTkTextbox(
            self, **kwargs , width=self.ancho, height=self.alto, corner_radius=5, activate_scrollbars=False
        )
        self.textBoxRead.grid(row=0, column=1, padx=(20, 20))
        # Inserta el contenido inicial de textBoxWrite en textBoxRead
        self.textBoxRead.insert("0.0", textReadStart)
        # Desactiva la edicion de textBoxRead
        self.textBoxRead.configure(state="disabled")
        # ------------------------- Box oupot texto ------------------------------ end

        # ------------------------- Box analisis texto ------------------------------ start
        # Box analisis (Temporal)
        self.boxAnalisis = customtkinter.CTkTextbox(
            self, width=180, height=self.alto, corner_radius=5, activate_scrollbars=False
        )
        self.boxAnalisis.grid(row=0, column=2)
        self.boxAnalisis.configure(state="disable")
        # ------------------------- Box analisis texto ------------------------------ end
        
        # ------------------------- scrollbarSync sincronizada ------------------------------ start
        self.scrollbarSync = customtkinter.CTkScrollbar(self)
        self.scrollbarSync.grid(row=0, column=3, sticky="ns")
        """
        scrollbarSync config
        Esta parte es fundamental para que el scrollbarSync sea uno para los "CTkTextBox"
        - scrollbarSync.configure: Relaciona la scrollbarSync con un evento
        - textBoxXXXX.configure: Realaciona el movimiento del scroll dentro del widget "CTkTextBox" con un evento
        """
        self.scrollbarSync.configure(command = self.on_scrollbar)
        self.textBoxWrite.configure(yscrollcommand=self.on_textscroll)
        self.textBoxRead.configure(yscrollcommand=self.on_textscroll)
        # ------------------------- scrollbarSync sincronizada ------------------------------ end

    def sincronizaTexto(self, *args, event=None):
        """
        TextBox derecha = Read
        TextBox izquierda = Write

        configure(state="normal") = Write and read
        configure(state="disabled") = Only read

        delete('1.0',"end")
        metodo('line.caracter', 'endline')
        """
        textTemp = self.textBoxWrite.get("1.0", "end")
        self.textBoxRead.configure(state="normal")
        self.textBoxRead.delete("1.0", "end")
        self.textBoxRead.insert("0.0", textTemp)
        self.textBoxRead.configure(state="disabled")   
        

        """
        ** self.on_scrollbar('moveto', self.yviewPosicion): es algo peculiar y confuso

        debido a estos dos metodos
            self.textBoxRead.delete("1.0", "end")
            self.textBoxRead.insert("0.0", textTemp)
        donde se elimina todo el contenido del "CTkTextBox" y de vuelve a insertar inmediatamente despues de cualquir modificacion o tecla presionada
        cada que esto sucedia la scrollbar volvia a inicio ('moveto', 0.0) y esto no es deaseado

        y con este metodo lo soluciono, ¿como?
        cada vez que se llama a esta funcion "sincronizaTexto"
        se elimina y se inserta todo el contenido y vuelve a la ultima posicion del scrollbar que fue almacenada en "yviewPosicion"
        """

        self.analisis(textTemp)
        self.on_scrollbar('moveto', self.yviewPosicion)

    def analisis(self, textTemp): # Temporal
        self.boxAnalisis.configure(state="normal")

        # Lista almacena el contenido de textBoxWrite linea a linea
        listTemp = textTemp.splitlines()
        self.boxAnalisis.delete("1.0", "end")
        for line in reversed(range(len(listTemp))):
            # lineSplit = line.split()
            conten = (f"line {line+1}\n")

            self.boxAnalisis.insert("0.0", conten)

        self.boxAnalisis.configure(state="disable")

    def on_scrollbar(self, *args, event=None):
        # textBoxXXXX.yview(*args): sincroniza los "CTkTextBox" con el mismo "yview"
        self.textBoxWrite.yview(*args)
        self.textBoxRead.yview(*args)
        self.boxAnalisis.yview(*args)

        """
        "args": devueve una tupla (moveto, fload)
        estos valores indican la altura de la scrollbar. Su posicion entre 0.0 y 0.6 aprox
        float(args[1]) = x.xxxxxxxxxx | almacena la ultima posicion que tuvo la scrollbar
        """
        self.yviewPosicion = float(args[1])

    def on_textscroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel
        is moved on a text widget'''
        self.scrollbarSync.set(*args)
        self.on_scrollbar('moveto', args[0])
        # print(" READ: ",*args[0])
        # print("--------------------")