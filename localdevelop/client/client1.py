
import requests
import pandas as pd



if __name__ == "__main__":
    # Carrega os dados
    mydf = pd.read_csv('../../datasets/statistical/BaseUnknown03.csv')

    mysample = mydf.sample(6).drop('nome', axis=1) #Obtém X exemplos aleatórios
    # Atenção! Verificar se o teu modelo possui a coluna etnia, caso contrário, também é necessário remover
    # com a instrução a seguir:
    #mysample = mysample.sample(20).drop('etnia', axis=1)

    # Prepara chamada
    url = "http://XXXXXXXXX" #Coloque aqui o URL da Azure
    headers = {'Content-Type': 'application/json'}
    #Caso seja com chave, adicionar o código abaixo
    #authKey = "ohx16XDHu3gOEDat8EqLHRd0YGpAhgLV" #Coloque aqui a chave do Web Servicec
    #headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + authKey)}

    conteudo = mysample.to_json(orient='split')

    #Chama a tua API
    response = requests.request("POST", url, headers=headers, data=conteudo)
    print("Resposta da API:")
    print(response.text.encode('utf8').decode())
    pass



