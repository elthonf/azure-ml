from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import sklearn
import math
from azureml.core import Experiment
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.ensemble import RandomForestRegressor as rfr

# O azureml-core da versão 1.0.72 ou superior é requerido
# é necessário azureml-dataprep[pandas] na versão 1.1.34 ou superior
from azureml.core import Workspace, Dataset

#Trocar os códigos abaixo pelos da sua instância!
subscription_id = '5298dbd8-b7e6-432a-b8fc-828328490c29'
resource_group = 'APIs'
workspace_name = 'revisao'

workspace = Workspace(subscription_id, resource_group, workspace_name)



def get_a_funnyName():
    f = open("../../datasets/names/funnynames.txt", "r")
    nomes = f.readlines()
    return random.choice(nomes).rstrip('\n')


if __name__ == "__main__":
    # Carrega os dados
    mydf = pd.read_csv('../../datasets/statistical/BaseDefault01.csv')
    #mydf = pd.read_csv('datasets/statistical/BaseDefault01.csv')

    # Identifica no dataset as variáveis independentes e a variavel alvo
    targetcol = 'default'
    y = mydf[targetcol]

    #Cria experimento
    experiment = Experiment(workspace=workspace, name="risco-credito-experimentos-local")
    run = experiment.start_logging()
    run.log("Tipo", "Classificador")


    # Treina modelo 01 (Classificador)
    independentcols = ['renda', 'idade', 'etnia', 'sexo', 'casapropria', 'outrasrendas', 'estadocivil', 'escolaridade']
    x = mydf[independentcols]
    clf = rfc()
    clf.fit(X=x, y=y)
    clf.independentcols = independentcols

    #Acuracia
    clf_acuracia = clf.score(X=x, y=y)
    print("Modelo 01 (classificador), criado com acurácia de: [{0}]".format(clf_acuracia))
    run.log("acuracia", clf_acuracia)

    #Demais logs (não serão comparados)
    run.log("Versao sklearn", sklearn.__version__)
    run.log("criterion", clf.criterion)
    run.log("n_estimators", clf.n_estimators)
    run.log("min_samples_leaf", clf.min_samples_leaf)
    run.log("max_depth", clf.max_depth)
    run.log_list("Inputs", independentcols)

    model_name = "model_risco_RF_local01.pkl"
    filename = "outputs/" + model_name

    joblib.dump(value=clf, filename=filename)

    # Upload do arquivo, deve demorar um pouco
    run.upload_file(name=model_name, path_or_stream=filename)
    run.complete()

    pass

    # Treina modelo 02 (Regressor)
    independentcols = ['renda', 'idade', 'sexo', 'casapropria', 'outrasrendas', 'estadocivil', 'escolaridade']

    run = experiment.start_logging()
    run.log("Tipo", "Regressor")

    pass