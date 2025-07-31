
import tkinter as tk
from idlelib.configdialog import font_sample_text
from threading import Thread
from drivers.mult_drivers import iniciar_ambiente_para_todos, rodar_automacao
drivers_services = []
from concurrent.futures import ThreadPoolExecutor, as_completed

janela = tk.Tk()                          # Cria uma janela
janela.title('central de Recadastro')
janela.geometry('600x400')

container = tk.Frame(janela, bg="#f0f0f0")
container.place(relx=0.5, rely=0.5, anchor="center")

#adiconando a imagem a interface
fundo = tk.PhotoImage(file="ALT360_logo.png")
logo = tk.Label(container, image=fundo, bg="#f0f0f0")
logo.grid(row=1, column=0, columnspan=2, pady=(0, 20))

#aparencia dos botoes
aparencia_botao= {
    "bg": "#EF4036",   #cor do botao
    "fg":"white",     #cor da fonte
    "font":("helvetica", 10, "bold"),     #escolha da fonte
    "relief":"groove",    #borda do botao
}

#aparencia LOG

aparencia_LOG ={
    "fg":"black",
    "font":("Arial", 20, "italic"),


}

def executar():
    label.config(text="WHATSAPP")

    def tarefa():
        global drivers_services
        if not drivers_services:
            drivers_services=iniciar_ambiente_para_todos()
        driver = drivers_services[0][0]
        rodar_automacao(driver)
        Thread(target=tarefa).start()


def executartd ():
    label.config(text="BUSSINESS")



def wireless():
    label.config(text="CONECTANDO 📡")
def verificarsf ():
    label.config(text="VERIFICANDO🔍")
def limpar():  # Função chamada ao clicar no botão
        label.config(text="LIMPO 🗑️")



label = tk.Label(container,text="Conecte o celular para executar o recadastro 🔃")  # Cria um rótulo com texto
label.grid (row=0, column=0, columnspan=2, pady=(10,20))




#estilizando o botão

BTexec = tk.Button(
    container,
    text="WHATSAPP",
    command=executar,
    **aparencia_botao
)
BTexec.grid(row=2, column=0, padx=10, pady=5)

BTexectd = tk.Button(
    container,
    text="BUSSINESS",
    command=executartd,
    **aparencia_botao
)
BTexectd.grid(row=2, column=1, padx=10, pady=5)

BTwireless = tk.Button (
    container,
    text ="WIRELESS",
    command=wireless,
    **aparencia_botao
)
BTwireless.grid(row=3, column=0, padx=10, pady=5)

BTverificar = tk.Button (container,
    text="VERIFICAR",
    command=verificarsf,
    **aparencia_botao
)
BTverificar.grid(row=3, column=1, padx=10, pady=5)

BTlimpar = tk.Button (container,
    text="LIMPAR",
    command=limpar,
    **aparencia_botao)
BTlimpar.grid(row=4, column=0, columnspan=2, pady=(15, 10))

#adiconando um LOG para a interface

from tkinter.scrolledtext import ScrolledText
log_area=ScrolledText(container, height=10, width=60, state='disabled', bg="#f0f0f0")
log_area.grid(row=5, column=0, columnspan=2, pady=(20,15))

import sys

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, message)
        self.widget.configure(state='disabled')
        self.widget.see(tk.END)

    def flush(self):
        pass

sys.stdout = TextRedirector(log_area)
sys.stderr = TextRedirector(log_area)



janela.mainloop()                          # Inicia a interface


container = tk.Frame(janela, bg="#f0f0f0")
container.place(relx=0.5, rely=0.5, anchor="center")

#adiconando a imagem a interface
fundo = tk.PhotoImage(file="ALT360_logo.png")
logo = tk.Label(container, image=fundo, bg="#f0f0f0")
logo.grid(row=1, column=0, columnspan=2, pady=(0, 20))

#aparencia dos botoes
aparencia_botao= {
    "bg": "#EF4036",   #cor do botao
    "fg":"white",     #cor da fonte
    "font":("helvetica", 10, "bold"),     #escolha da fonte
    "relief":"groove",    #borda do botao
}

#aparencia LOG

aparencia_LOG ={
    "fg":"black",
    "font":("Arial", 20, "italic"),


}

def executar():
    label.config(text="WHATSAPP")

    def tarefa():
        global drivers_services
        if not drivers_services:
            drivers_services=iniciar_ambiente_para_todos()
        driver = drivers_services[0][0]
        rodar_automacao(driver)
        Thread(target=tarefa).start()


def executartd ():
    label.config(text="BUSSINESS")



def wireless():
    label.config(text="CONECTANDO 📡")
def verificarsf ():
    label.config(text="VERIFICANDO🔍")
def limpar():  # Função chamada ao clicar no botão
        label.config(text="LIMPO 🗑️")



label = tk.Label(container,text="Conecte o celular para executar o recadastro 🔃")  # Cria um rótulo com texto
label.grid (row=0, column=0, columnspan=2, pady=(10,20))




#estilizando o botão

BTexec = tk.Button(
    container,
    text="WHATSAPP",
    command=executar,
    **aparencia_botao
)
BTexec.grid(row=2, column=0, padx=10, pady=5)

BTexectd = tk.Button(
    container,
    text="BUSSINESS",
    command=executartd,
    **aparencia_botao
)
BTexectd.grid(row=2, column=1, padx=10, pady=5)

BTwireless = tk.Button (
    container,
    text ="WIRELESS",
    command=wireless,
    **aparencia_botao
)
BTwireless.grid(row=3, column=0, padx=10, pady=5)

BTverificar = tk.Button (container,
    text="VERIFICAR",
    command=verificarsf,
    **aparencia_botao
)
BTverificar.grid(row=3, column=1, padx=10, pady=5)

BTlimpar = tk.Button (container,
    text="LIMPAR",
    command=limpar,
    **aparencia_botao)
BTlimpar.grid(row=4, column=0, columnspan=2, pady=(15, 10))




janela.mainloop()                          # Inicia a interface

