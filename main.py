import tkinter as tk

import customtkinter
from frames.frames import topFrame
#
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(1150, 550)
        self.maxsize(1150, 1000)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.title("Block de Rimas")

        # instancia de frame
        self.my_frame = topFrame(self)
        self.my_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        """
        self.botonPrueba = customtkinter.CTkButton(
            self, corner_radius=5, command=lambda: self.sincronizaTexto()
        )
        self.botonPrueba.grid(row=1, column=0, padx=50, pady=10, sticky="sew")
        """
        
        # -------------- BARRA DE MENU ------------ Start
        menu_bar = tk.Menu(self)
        m1 = tk.Menu(menu_bar, tearoff=0)
        m1.add_command(label="Abrir archivo")
        m1.add_command(label="Guardar archivo")
        m1.add_separator()
        m1.add_command(label="Salir")
        self.config(menu=menu_bar)

        menu_bar.add_cascade(label="Archivo", menu=m1)
        m2 = tk.Menu(menu_bar, tearoff=0)
        # m2.add_command(label="Light theme",command=lambda : self.theme_selection(0))
        m2.add_command(
            label="Tema Claro",
            command=lambda: self.change_appearance_mode_event("Light"),
        )
        m2.add_command(
            label="Tema Oscuro",
            command=lambda: self.change_appearance_mode_event("Dark"),
        )
        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Opciones", menu=m2)

        m3 = tk.Menu(menu_bar, tearoff=0)
        m3.add_command(label="Ayuda!")
        self.config(menu=menu_bar)
        menu_bar.add_cascade(label="Help", menu=m3)
        # -------------- BARRA DE MENU ------------ End

    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


app = App()
app.mainloop()
