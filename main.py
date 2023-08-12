import tkinter as tk

import customtkinter

#
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Constantes
        self.ancho = 430
        self.alto = 500

        # Box input
        self.textboxWrite = customtkinter.CTkTextbox(
            self, width=self.ancho, height=self.alto, corner_radius=5
        )
        self.textboxWrite.grid(row=0, column=0)
        self.textboxWrite.insert("0.0", "Some example text!\n" * 10)

        # Box ouput
        self.textboxRead = customtkinter.CTkTextbox(
            self, width=self.ancho, height=self.alto, corner_radius=5
        )
        self.textboxRead.grid(row=0, column=1, padx=(20, 0))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(900, 550)
        self.maxsize(900, 1000)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.title("Block de Rimas")

        self.my_frame = MyFrame(self)
        self.my_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.botonPrueba = customtkinter.CTkButton(
            self, corner_radius=5, command=lambda: self.sincronizaTexto()
        )
        self.botonPrueba.grid(row=1, column=0, padx=50, pady=10, sticky="sew")

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

    def sincronizaTexto(self):
        # TextBox derecha = Read
        # TextBox izquierda = Write

        """
        configure(state="normal") = Write and read
        configure(state="disabled") = Only read

        delete('1.0',"end")
        metodo('line.caracter', 'endline')
        """
        self.my_frame.textboxRead.configure(state="normal")
        text = self.my_frame.textboxWrite.get("1.0", "end")
        self.my_frame.textboxRead.delete("1.0", "end")
        self.my_frame.textboxRead.insert("0.0", text)
        self.my_frame.textboxRead.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


app = App()
app.mainloop()
