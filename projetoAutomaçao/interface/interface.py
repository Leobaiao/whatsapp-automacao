import tkinter as tk
from idlelib.configdialog import font_sample_text

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
    "width":12,
    "height":1
}

def executar():
    label.config(text="EXECUTANDO")
def executarTD ():
    label.config(text="EXECUTANDO TODOS")
def wireless():
    label.config(text="CONECTANDO 📡")
def verificarSF ():
    label.config(text="VERIFICANDO🔍")
def limpar():  # Função chamada ao clicar no botão
        label.config(text="LIMPO ✅")


label = tk.Label(container,text="Conecte o celular para executar o recadastro 🔃")  # Cria um rótulo com texto
label.grid (row=0, column=0, columnspan=2, pady=(10,20))




#estilizando o botão

BTexec = tk.Button(
    container,
    text="EXECUTAR",
    command=executar,
    **aparencia_botao
)
BTexec.grid(row=2, column=0, padx=10, pady=5)

BTexecTD = tk.Button(
    container,
    text="EX. TUDO",
    command=executarTD,
    **aparencia_botao
)
BTexecTD.grid(row=2, column=1, padx=10, pady=5)

BTwireless = tk.Button (
    container,
    text ="WIRELESS",
    command=wireless,
    **aparencia_botao
)
BTwireless.grid(row=3, column=0, padx=10, pady=5)

BTverificar = tk.Button (container,
    text="VERIFICAR",
    command=verificarSF,
    **aparencia_botao
)
BTverificar.grid(row=3, column=1, padx=10, pady=5)

BTlimpar = tk.Button (container,
    text="LIMPAR",
    command=limpar,
    **aparencia_botao)
BTlimpar.grid(row=4, column=0, columnspan=2, pady=(15, 10))






janela.mainloop()                          # Inicia a interface