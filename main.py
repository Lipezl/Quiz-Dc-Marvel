import tkinter as tk
from tkinter import messagebox, ttk #import usado para aparecer uma mensagem na tela, quando chamado
from tkinter import PhotoImage #import do PhotoImage, para usar imagens na interface
from questions_quiz.quiz_marvel import quiz_marvel #import do arquivo do quiz da marvel
from questions_quiz.quiz_dc import quiz_dc #import do arquivo do quiz da dc
import json_data.login #import do arquivo de login

def definir_cor_de_fundo(frame, cor): #Função para colocar cor nos frames
    style = ttk.Style()
    style.configure("EstiloFrame.TFrame", background=cor)
    frame.config(style="EstiloFrame.TFrame")

def registro(): #Função para guardar os registros
    email = entry_email.get()
    senha = entry_senha.get()
    json_data.login.registro(email, senha)

def escolha1(botao): 
    #Se o usuario escolher a DC, vai tirar a tela2, e ir para tela_dc
    if botao == "DC":
        print("O usuário escolheu DC!")
        tela2.pack_forget()
        tela_dc.pack(fill="both")
        quizdc = tk.Label(tela_dc, text="Iniciar Quiz da DC:", anchor="center", font=("Helvetica", 20, "bold"))
        quizdc.pack(padx=10, pady=10, side="top")
        #botão para iniciar o quiz da DC
        botaoquizdc = tk.Button(tela_dc, text="Começar", font=("Arial", 18), command=lambda: onedc())
        botaoquizdc.pack()

    #Se não se o usuario escolher marvel, sai da tela2 e vai para tela_marvel
    elif botao == "Marvel":
        print("O usuário escolheu Marvel!")
        tela2.pack_forget() #para a tela 2 sair da janela
        tela_marvel.pack() #para entrar a tela da marvel

        quizmarvel = tk.Label(tela_marvel, text="Iniciar Quiz da Marvel:", anchor="center", font=("Arial", 16))
        quizmarvel.pack(padx=10, pady=10, side="top")
        #Botão para iniciar o quiz da Marvel
        botaoquizmarvel = tk.Button(tela_marvel, text="Começar", font=("Arial", 18), command=lambda: onemarvel())
        botaoquizmarvel.pack()

def mostrar_tela1():
    tela2.pack_forget()  # Oculta a tela 2
    tela1.pack()

def mostrar_tela2():
    tela1.pack_forget()  # Oculta a tela 1
    tela2.pack()

def questao_marvel(): #funcao para apresentar o enunciado da questao e as alternativas (marvel)

    question_marvel = quiz_marvel[questao_atual_marvel] #vai pegar a lista do outro arquivo, e a questao atual indica o indice que deve ir na lista

    q1.config(text=question_marvel["questao"]) #vai pegar o enunciado da questao que for de acordo com o indice pego 

    alternativas = question_marvel["alternativas"] #vai pegar as alternativas desse indice

    for i in range(4): #Esse for vai criar os botões de acordo com as alternativas da questão
        choice_btns_marvel[i].config(text=alternativas[i], state="normal")

    feedback_label_marvel.config(text="") #feedback: (correto/incorreto), mas só vai aparecer quando o usuario clicar em alguma alternativa

    proximo_btn_marvel.config(state="disabled") #inicialmente o botao de proximo estara desabilitado, só vai habilitar quando clicar em alguma alternativa

def altcorreta_marvel(escolha):
    question = quiz_marvel[questao_atual_marvel] #vai pegar o indice de acordo com a questao atual
    escolha_correta_marvel = choice_btns_marvel[escolha].cget("text") 

    #Checa se a escolha do usuario foi a correta
    if escolha_correta_marvel == question["correta"]:
        global score_marvel
        score_marvel += 1 #se for correta, aumenta 1 no score
        score_label_marvel.config(text="Score: {}/{}".format(score_marvel, len(quiz_marvel))) #ajusta o numero de acertos no score
        feedback_label_marvel.config(text="Correto!", foreground="green")
    else:
        feedback_label_marvel.config(text="Incorreto!", foreground="red")

    #ao usuario escolher, desabilita todos botões
    for button in choice_btns_marvel:
        button.config(state="disabled")
    proximo_btn_marvel.config(state="normal") #habilita o botão para ir para o próximo

def next_marvel():
    global questao_atual_marvel
    questao_atual_marvel += 1 #aumenta 1 quando a funcao for chamada

    #Se o numero da questao for menor que os elementos da lista do arquivo quiz_marvel, vai apresentar a proxima questao
    if questao_atual_marvel < len(quiz_marvel):
        questao_marvel()

    #Se não, quer dizer que acabou as questoes
    else:
        #apresenta uma nova tela, indicando qual foi seu score
        messagebox.showinfo("Quiz Completado",
                            "Quiz Completado! Pontuação: {}/{}".format(score_marvel, len(quiz_marvel)))
        #Ao usuario clicar no botao, a janela vai ser fechada
        janela.destroy()

def onemarvel():
    #o global foi usado para deixar todas essas variaveis utilizaveis fora da funcao
    global q1, button_marvel, choice_btns_marvel, feedback_label_marvel, score_marvel, score_label_marvel, proximo_btn_marvel

    tela_marvel.pack_forget() #sair dessa tela
    telamarvel1.pack() #para entrar a dela da marvel1
    definir_cor_de_fundo(telamarvel1, "#fe9d97")

    #Label do enunciado da questao
    q1 = ttk.Label(telamarvel1, anchor='center', wraplength=500, padding=10, font=("Helvetica", 22, "bold"))
    q1.pack(pady=10)

    #lista dos botoes (marvel)
    choice_btns_marvel = []

    #For utilizado para criar os botoes
    for i in range(4):
        button_marvel = ttk.Button(telamarvel1, command=lambda i=i: altcorreta_marvel(i))
        button_marvel.pack(pady=5)
        choice_btns_marvel.append(button_marvel) #todo botao é adicionado na lista

    #label do feedback (correto / incorreto)
    feedback_label_marvel = ttk.Label(telamarvel1, anchor="center", padding=10, font=("Helvetica", "14", "bold"), background="#fe9d97" )
    feedback_label_marvel.pack(pady=10)

    score_marvel = 0 #iniciando a variavel score
    #criando o label do score, que aparecera em baixo das alternativas
    score_label_marvel = ttk.Label(telamarvel1, text="Score 0/{}".format(len(quiz_marvel)), anchor="center", padding=10,  font=("Helvetica", "14", "bold"), background="#fe9d97")
    score_label_marvel.pack(pady=10)
    proximo_btn_marvel = ttk.Button(telamarvel1, text="Próximo", command=next_marvel, state="disabled")
    proximo_btn_marvel.pack(pady=10)

    questao_marvel()

def questao_dc():
    question_dc = quiz_dc[questao_atual_dc] #funcao para apresentar o enunciado da questao e as alternativas (DC)
    q_dc.config(text=question_dc["questao"]) #vai pegar a lista do outro arquivo, e a questao atual indica o indice que deve ir na lista
    alternativas_dc = question_dc["alternativas"] #vai pegar as alternativas desse indice

    for i in range(4): #Esse for vai criar os botões de acordo com as alternativas da questão
        choice_btns_dc[i].config(text=alternativas_dc[i], state="normal")

    feedback_label_dc.config(text="") #feedback: (correto/incorreto), mas só vai aparecer quando o usuario clicar em alguma alternativa
    proximo_btn_dc.config(state="disabled") #inicialmente o botao de proximo estara desabilitado, só vai habilitar quando clicar em alguma alternativa

def altcorreta_dc(escolha_dc):
    questao_dc = quiz_dc[questao_atual_dc] #vai pegar o indice de acordo com a questao atual
    escolha_correta_dc = choice_btns_dc[escolha_dc].cget("text") 

    #Checa se a escolha do usuario foi a correta
    if escolha_correta_dc == questao_dc["correta"]:
        global score_dc
        score_dc += 1 #se for correta, aumenta 1 no score
        score_label_dc.config(text="Score {}/{}".format(score_dc, len(quiz_dc))) #ajusta o numero de acertos no score
        feedback_label_dc.config(text="Correto!", foreground="green")
    else:
        feedback_label_dc.config(text="Incorreto!", foreground="red")

    #ao usuario escolher, desabilita todos botões
    for button_dc in choice_btns_dc:
        button_dc.config(state="disabled")
    proximo_btn_dc.config(state="normal") #habilita o botão para ir para o próximo

def next_dc(): 
    global questao_atual_dc
    questao_atual_dc += 1 #aumenta 1 quando a funcao for chamada

    #Se o numero da questao for menor que os elementos da lista do arquivo quiz_marvel, vai apresentar a proxima questao
    if questao_atual_dc <len(quiz_dc):
        questao_dc()

    #Se não, quer dizer que acabou as questoes
    else:
        #apresenta uma nova tela, indicando qual foi seu score
        messagebox.showinfo("Quiz Completado",
                            "Quiz Completado! Final Score: {}/{}".format(score_dc, len(quiz_dc)))

        #Ao usuario clicar no botao, a janela vai ser fechada
        janela.destroy()

def onedc():
    #O global foi usado para deixar todas essas variaveis utilizaveis fora da funcao
    global q_dc, choice_btns_dc, button_dc, feedback_label_dc, score_dc, score_label_dc, proximo_btn_dc

    tela_dc.pack_forget()
    teladc1.pack()
    #Label do enunciado da questao
    q_dc = ttk.Label(teladc1, anchor="center", wraplength=500, padding=10, font=("Helvetica", 22, "bold"))
    q_dc.pack(pady=10)

    #lista dos botoes (dc)
    choice_btns_dc = []

    #For utilizado para criar os botoes
    for i in range(4):
        button_dc = ttk.Button(teladc1, command=lambda i=i: altcorreta_dc(i), style="TButton") 
        button_dc.pack(pady=10)
        choice_btns_dc.append(button_dc) #todo botao é adicionado na lista

    #label do feedback (correto / incorreto)
    feedback_label_dc = ttk.Label(teladc1, anchor="center", padding=10, background="#8dbdeb", font=("Helvetica", 14, "bold"))
    feedback_label_dc.pack(pady=10)

    #criando o label do score, que aparecera em baixo das alternativas
    score_dc = 0 #iniciando a variavel score
    score_label_dc = ttk.Label(teladc1, text="Score: 0/{}".format(len(quiz_dc)), anchor="center", padding=10, font=("Helvetica", 14, "bold"), background="#8dbdeb")
    score_label_dc.pack(pady=10)
    proximo_btn_dc = ttk.Button(teladc1, text="Próximo", command=next_dc, state="disabled")
    proximo_btn_dc.pack(pady=10)

    questao_dc()

#inicializando as duas variaveis
questao_atual_dc = 0 
questao_atual_marvel = 0

#iniciando a janela do tkinter
janela = tk.Tk()
janela.title("Quiz")

#inicializando todos os frames
tela1 = ttk.Frame(janela)
tela2 = ttk.Frame(janela)
tela_dc = ttk.Frame(janela)
teladc1 = ttk.Frame(janela)
tela_marvel = ttk.Frame(janela)
telamarvel1 = ttk.Frame(janela)

#usando a função para definir a cor nos Frames
definir_cor_de_fundo(tela1, "#b8d9c8")
definir_cor_de_fundo(teladc1, "#8dbdeb")


#criacao dos label da tela de email
label_email = ttk.Label(tela1, text="Email:", font=("Helvetica",18, "bold"))
label_email.pack(padx=10, pady=10)

#A caixa de caracteres para o usuario escrever o email
entry_email = ttk.Entry(tela1)
entry_email.pack(padx=10, pady=10)

#Criacao de label da senha
label_senha = ttk.Label(tela1, text="Senha:", font=("Helvetica", 18, "bold"))
label_senha.pack(padx=10, pady=10)

entry_senha = ttk.Entry(tela1, show="*")
entry_senha.pack(padx=10, pady=10)

botao_enviar = ttk.Button(tela1, text="Enviar", command=lambda: [registro(), mostrar_tela2()])
botao_enviar.pack(padx=10, pady=10)

label_escolha = ttk.Label(tela2, text="Escolha o seu preferido:", font=("Helvetica", 20, "bold"), anchor="center")
label_escolha.pack(pady = 10, fill="x")
#label da segunda tela (dc)
quadro_dc = ttk.Frame(tela2)
quadro_dc.pack(side="left", padx=10, pady=10)
imagem_dc = PhotoImage(file="images//dc.png")
label_dc = tk.Label(quadro_dc, image=imagem_dc)
label_dc.pack(padx=10, pady=10)
botao_dc = ttk.Button(quadro_dc, text="Escolher DC", style="TButton", command=lambda: escolha1('DC'))
botao_dc.pack(padx=10, pady=10)

#label da segunda tela (marvel)
quadro_marvel = ttk.Frame(tela2)
quadro_marvel.pack(side="right", padx=10, pady=10)
imagem_marvel = PhotoImage(file="images//marvel.png")
label_marvel = tk.Label(quadro_marvel, image=imagem_marvel)
label_marvel.pack(padx=10, pady=10)
botao_marvel = ttk.Button(quadro_marvel, text="Escolher Marvel", style="my.TButton", command=lambda: escolha1('Marvel'))
botao_marvel.pack(padx=10, pady=10)

#resolucao da janela
janela.geometry("600x500")
janela.configure(background="#fffcf7")
tela1.pack(fill="y")
janela.mainloop()