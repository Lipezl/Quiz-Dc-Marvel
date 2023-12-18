import json

#Função para registrar o email e a senha do usuario, e importar no arquivo JSON
def registro(email, senha):
    if len(email) > 0 and len(senha) > 0: #Se o email e a senha ter mais de uma caractere, sera salvo no json
        #Dicionario para o JSON
        dados = {
            "Email:": email,
            "Senha:": senha
        }
        with open("json_data//dados.json", "a") as arquivo: #Cada usuario que colocar o email e a senha, vai adicionar +1 no jSON

            json.dump(dados, arquivo, indent=4)