#!/bin/bash
set -x #echo on


if [ $# -gt 0 ]
then
    RES_GROUP=$1
else
    echo "Por favor, informe o parâmetro Resource Group após ${0} "
    echo "Exemplo:"
    echo "bash ${0} meugrupo"
    exit 400
fi

echo Resource Group: $RES_GROUP

cd `mktemp -d` &&
   echo Diretório temporário criado : $(pwd) &&
   git clone https://github.com/elthonf/azure-ml.git &&
   cd azure-ml/containeronazure


az group create --resource-group $RES_GROUP --location eastus



MYUUID=$(python3 myuuid.py)

ACR_NAME=acr$(MYUUID)
az acr create --resource-group $RES_GROUP --location eastus --sku Standard --name $ACR_NAME



AKV_NAME=kv$(MYUUID)
echo Key Vault = $AKV_NAME
az keyvault create --resource-group $RES_GROUP --name $AKV_NAME

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



az acr build --registry $ACR_NAME --image supermodelo:latest --file ./dockerfile.txt  .

az container create \
  --resource-group $RES_GROUP \
  --name aci-modelo \
  --image $ACR_NAME.azurecr.io/supermodelo:latest \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-usr --query value -o tsv) \
  --registry-password $(az keyvault secret show --vault-name $AKV_NAME --name $ACR_NAME-pull-pwd --query value -o tsv) \
  --dns-name-label acr-tasks-$ACR_NAME \
  --query "{FQDN:ipAddress.fqdn}" \
  --output table

