# Objetivo

O objetivo desde diretório é :
- criar uma imagem de container no Azure Container Registry
- criar um container no Azure Container Instance

Este processo vai requerer um arquivo de modelo com o nome:
```
./modelo/nome_arquivo.pkl
``` 

# Instruções

## 1 - Crie um diretório temporário
```
cd `mktemp -d`
```

## 2 - Clone este repositório
```
git clone https://github.com/elthonf/azure-ml.git
```

## 3 - Entre no diretório `containeronazure`
```
cd azure-ml/containeronazure
```

## 3.1 - Sobreescreva o arquivo do modelo
Agora, vc deve substituir o arquivo `modelo/nome_arquivo.pkl`


## 4 - Defina a variável RES_GROUP (Resource Group)
```
RES_GROUP=
```

## 5 - Caso o grupo não exista, crie-o
```
az group create --resource-group $RES_GROUP --location eastus
```

## 6 - Crie o container registry (ACR) ou use um já existente dentro do Resource Group
```
ACR_NAME=
az acr create --resource-group $RES_GROUP --location eastus --sku Standard --name $ACR_NAME
```

## 7 - BUILD!! Gere a imagem
```
az acr build --registry $ACR_NAME --image supermodelo:latest --file ./dockerfile.txt  .
```

<hr />

## 8 *- Criar KeyVault
```
AKV_NAME=kv$(python3 myuuid.py)
echo Key Vault = $AKV_NAME
az keyvault create --resource-group $RES_GROUP --name AKV_NAME
```