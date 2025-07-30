import tkinter as tk
from idlelib.configdialog import font_sample_text

janela = tk.Tk()                          # Cria uma janela
janela.title('central de Recadastro')
janela.geometry('600x400')

#adiconando a imagem a interface
fundo = tk.PhotoImage(file="ALT360_logo.png")
fundo_label = tk.Label(janela, image=fundo)
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)

def botao_clicado():                    # Função chamada ao clicar no botão
    label.config(text="FEITO ✅")




label = tk.Label(janela,text="Conecte o celular para executar o recadastro 🔃")  # Cria um rótulo com texto
font=("Arial", 20, "bold")



#estilizando o botão

botao = tk.Button(
    janela,
    text="RECADASTRO",
    command=botao_clicado,
    bg="#EF4036",   #cor do botao
    fg="white",     #cor da fonte
    font=("helvetica", 20, "bold"),     #escolha da fonte
    relief="groove",    #borda do botao
    bd =3,  #Espessura da borda
    padx=10,    #padding horizontal interno
    pady=10,     #padding vertical interno
    width=12, height=1 #se eu tiver que explicar isso eu prefiro botar meu teclado no rabo
)

botao.pack(side="bottom", pady=50) #posicionamento empilhando automaticamente


botao.pack()                               # Adiciona o botão à janela

janela.mainloop()                          # Inicia a interface