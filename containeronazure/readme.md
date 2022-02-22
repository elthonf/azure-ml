# Objetivo

O objetivo desde diretório é :
- criar uma imagem de container no Azure Container Registry
- criar um container no Azure Container Instance

Este processo vai requerer um arquivo de modelo com o nome:
```
./modelo/nome_arquivo.pkl
``` 

# Instruções

## 1 - Definir a variável RES_GROUP (Resource Group)
```
RES_GROUP=
```

## 2 - Criar um diretório temporário
- Criar um diretório temporário
- Clonar este repositório
- Entrar no subdiretório `containeronazure`
```
cd `mktemp -d` &&
   git clone https://github.com/elthonf/azure-ml.git &&
   cd azure-ml/containeronazure
```

## 3 - Sobreescreva o arquivo do modelo (opcional)
Agora, vc deve substituir o arquivo `azure-ml/containeronazure/modelo/nome_arquivo.pkl` pelo seu modelo.

Isso é interessante pois o arquivo atual, é menor (apenas 16MB) para caber no github, enquanto o seu modelo real pode ter muitos MBs de tamanho.


<hr />



## 4 - Exibir info do grupo.
Obs.: Caso o grupo não exista, esta instrução também o cria
```
az group create --resource-group $RES_GROUP --location eastus
```

## 5 - Criar um container registry novo dentro do Resource Group
Obs.: Para este caso estamos usando um nome aleatório
```
ACR_NAME=acr$(python3 myuuid.py)
echo Container Registry criado = $AKV_NAME
az acr create --resource-group $RES_GROUP --location eastus --sku Standard --name $ACR_NAME
```


## 6 - Criar KeyVault
Obs.: KeyVaults são necessárias para *acessar* imagens customizadas dentro do container registry
```
AKV_NAME=kv$(python3 myuuid.py)
echo Key Vault criada = $AKV_NAME
az keyvault create --resource-group $RES_GROUP --name $AKV_NAME
```

## 7 - Criar senha e usuario no KV do service principal, usando os usuários do ACR
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
echo "Usuario: " $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-usr --query value -o tsv)
echo "Senha: " $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-pwd --query value -o tsv)
```

## 8 - BUILD!! Gera a imagem
```
az acr build --registry $ACR_NAME --image supermodelo:latest --file ./dockerfile.txt  .
```

<hr />


## 9 - Por fim, instrução para cria os contêineres "klusterless"
Obs.: O processo pode demorar alguns minutos para atualizar o DNS.
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

<hr />


## Extras:

```
#To attach
az container attach --resource-group $RES_GROUP --name acr-tasks

az container exec --exec-command "/bin/bash" --resource-group $RES_GROUP --name acr-tasks
```

## Arquivo Shell Script para executar pela internet:

```
curl https://raw.githubusercontent.com/elthonf/azure-ml/master/containeronazure/buildcont.sh > buildcont.sh
bash buildcont.sh

```