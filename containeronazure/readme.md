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
#ou
ACR_NAME=acr$(python3 myuuid.py)
az acr create --resource-group $RES_GROUP --location eastus --sku Standard --name $ACR_NAME
```


## 7 - Criar KeyVault
```
AKV_NAME=kv$(python3 myuuid.py)
echo Key Vault = $AKV_NAME
az keyvault create --resource-group $RES_GROUP --name $AKV_NAME
```

## 8 - Cria senha e usuario no KV do service principal, usando os usuários do ACR
```
az keyvault secret set \
  --vault-name $AKV_NAME \
  --name $ACR_NAME-pull-pwd \
  --value $(az ad sp create-for-rbac \
              --name $ACR_NAME-pull \
              --scopes $(az acr show --name $ACR_NAME --query id --output tsv) \
              --role acrpull \
              --query password \
              --output tsv)

az keyvault secret set \
  --vault-name $AKV_NAME \
  --name $ACR_NAME-pull-usr \
  --value $(az ad sp list --display-name $ACR_NAME-pull --query [].appId --output tsv)
``` 

para testar e obter usuario e senha::

```
echo $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-usr --query value -o tsv)
echo $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-pwd --query value -o tsv)
```

## 9 - BUILD!! Gera a imagem
```
az acr build --registry $ACR_NAME --image supermodelo:latest --file ./dockerfile.txt  .
```

<hr />


## 10 - Por fim, cria os contêineres
```
az container create \
  --resource-group $RES_GROUP \
  --name acr-tasks \
  --image $ACR_NAME.azurecr.io/supermodelo:latest \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-usr --query value -o tsv) \
  --registry-password $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-pwd --query value -o tsv) \
  --dns-name-label acr-tasks-$ACR_NAME \
  --query "{FQDN:ipAddress.fqdn}" \
  --output table
```


## Extras:

```
#To attach
az container attach --resource-group $RES_GROUP --name acr-tasks

az container exec --exec-command "/bin/bash" --resource-group $RES_GROUP --name acr-tasks
```