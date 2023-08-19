import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import *
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox
import os

import customtkinter
from frames.frames import topFrame
#
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # instancia de frame | Ventana principal
        self.my_frame = topFrame(self)
        self.my_frame.grid(row=0, column=0, sticky="nsew")

        self.titleApp = "Block de Rimas"
        self.titleFile = ["Nuevo archivo"]
        self.titleDefault = f"{self.titleApp}       |       {self.titleFile}"

        # configure system
        # self.minsize(1150, 550)
        self.title(f"{self.titleDefault}")
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        self.geometry("600x700") # Tamaño ventana predeterminado
        self.protocol("WM_DELETE_WINDOW", self.onClosing) # funcion al cerrar la ventana
        self.openFile_initialDir = "C:/Users/jeiso/OneDrive/Escritorio"
    
        # -------------- BARRA DE MENU ------------ Start
        menuBar = tk.Menu(self)

        m1 = tk.Menu(menuBar, tearoff=0)
        m1.add_command(label="Abrir", command=self.openFile)
        m1.add_command(label="Guardar", command=lambda:self.saveFile(isClosing=False, isOpening=False, isSaving=True))
        m1.add_separator()
        m1.add_command(label="Salir", command= lambda: self.onClosing())
        self.config(menu=menuBar)
        menuBar.add_cascade(label="Archivo", menu=m1)

        m2 = tk.Menu(menuBar, tearoff=0)
        m2.add_command(
            label="Tema Claro",
            command=lambda: self.change_appearance_mode_event("Light"),
        )
        m2.add_command(
            label="Tema Oscuro",
            command=lambda: self.change_appearance_mode_event("Dark"),
        )
        self.config(menu=menuBar)
        menuBar.add_cascade(label="Editar", menu=m2)

        m3 = tk.Menu(menuBar, tearoff=0)
        m3.add_command(label="Ayuda!")
        self.config(menu=menuBar)
        menuBar.add_cascade(label="Help", menu=m3)
        # -------------- BARRA DE MENU ------------ End

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def openFile(self):
        # limpiar textBoxWrite
        # Si el contenido actual de textBoxWhite es mas de "1" caracter
        if len(self.my_frame.textBoxWrite.get("1.0", "end")) > 1:
            # Si el contenido del ultimo archivo es exactamente igual al contenido actual de textBoxWhite
            # [:-1] | Elimina el santo de linea agregado por "textBoxWhrite al cargar un nuevo archvo"
            if  self.contenidoCopy == self.my_frame.textBoxWrite.get("1.0", "end")[:-1]:
                # entonces limpia la ventana y carga un nuevo archivo
                self.my_frame.textBoxWrite.delete("1.0", "end")
            else:
                #self.saveFile(isClosing=False, isOpening=True)
                self.windowclosep("Abrir nuevo archivo", "¿Desea guardar los cambios del archivo actual?", isClosingX=False, isOpeningX=True, isSavingX=False)

        filetypes = (
            ('Documento de texto', '*.txt'),
            ('Todos los archivos', '*.*')
        )

        selectFile = fd.askopenfilename(
            title='Abrir archivo',
            initialdir=self.openFile_initialDir,
            filetypes=filetypes
            )

        def getTitleFile(filePach:str):
            fileNameFull = os.path.basename(filePach.name)
            fileName = fileNameFull.replace(".txt", "")
            return fileName, fileNameFull

        try:
        # Abrir y leer archivo
            with open(selectFile, "r+") as reader:
                # Establece el nombre del archivo en la ventana
                self.titleFile = getTitleFile(reader)
                self.title(f"{self.titleApp}        |       {self.titleFile[0]}")
 
                contenido = reader.read()
                self.contenidoCopy = contenido # *** 
                self.my_frame.textBoxWrite.insert("0.0", contenido)
                self.my_frame.sincronizaTexto()
            #     CTkMessagebox(title="Error", message="Admitidos solo archivos con extensión '.txt'", icon="cancel")
        except FileNotFoundError:
            print("No ha seleccionado ningun archivo")
    
    def saveFile(self, isClosing:bool, isOpening:bool, isSaving:bool):
        fileSave = fd.asksaveasfile(
            title='Guardar',
            initialdir=self.openFile_initialDir,
            initialfile=self.titleFile[0],
            filetypes=[("txt file", ".txt")],defaultextension=".txt")
        
        if isClosing == True:
            # Contenido del textBoxWrite actual antes de cerrar
            contenido = self.my_frame.textBoxWrite.get("1.0", "end")
            with open(f"{fileSave.name}", "w", encoding="utf-8") as writing:
                writing.write(contenido)
                self.destroy()
        elif isOpening == True:
            # Contenido del textBoxWrite actual antes de cerrar
            contenido = self.my_frame.textBoxWrite.get("1.0", "end")
            with open(f"{fileSave.name}", "w", encoding="utf-8") as writing:
                writing.write(contenido)
        elif isSaving == True:
            # Contenido del textBoxWrite actual antes de guardar
            contenido = self.my_frame.textBoxWrite.get("1.0", "end")
            with open(f"{fileSave.name}", "w", encoding="utf-8") as writing:
                writing.write(contenido)
                self.contenidoCopy = contenido

        
    
    def onClosing(self):
        """
        cuadro de dialogo personalizado con biblioteca
        """
        boxWriteContent = self.my_frame.textBoxWrite.get("1.0", "end")
        # Borra el ultimo salto de linea agregado por el programa 
        boxWriteContent = boxWriteContent[:-1]
        
        try:
            if boxWriteContent == self.contenidoCopy:
                # si son exactamente iguales, entonces no hay modificacion y se puede cerrar sin perder info
                self.destroy()
            else:
                self.windowclosep("Salir", "¿Quieres guardar los cambios del archivo?", isClosingX=True, isOpeningX=False, isSavingX=False)
        except:
            if len(boxWriteContent) > 0:
                self.windowclosep("Salir", "¿Quieres guardar los cambios del archivo?", isClosingX=True, isOpeningX=False, isSavingX=False)
            elif len(boxWriteContent) == 0:
                self.destroy()

    def windowclosep(self, title:str, msgText:str, isClosingX:bool, isOpeningX:bool, isSavingX:bool):
            boxMsg = CTkMessagebox(title=title, message=msgText,
                    option_1="Cancel", option_2="No guardar", option_3="Guardar", button_color="#ffffff")
            response = boxMsg.get()
            if response=="Guardar":
                self.saveFile(isClosing=isClosingX, isOpening=isOpeningX, isSaving=isSavingX)
            elif response=="No guardar":
                if isOpeningX == True:
                    self.my_frame.textBoxWrite.delete("1.0", "end")
                else:
                    self.destroy()
            elif response=="Cancel":
                pass
            else:
                pass

app = App()
app.mainloop()
