import joblib
import pandas as pd
import sys
import json
import numpy as np
from flask import Flask, jsonify, request

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder
global meumodelo

def init():
    print(f"Python version: {sys.version}")
    #nltk.download("punkt")
    global meumodelo
    #sess = onnxruntime.InferenceSession(
    #    os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.onnx")
    #)
    #model_path = Model.get_model_path("knn")
    #print("Model Path is  ", model_path)
    #model = joblib.load(model_path)

    #meumodelo = joblib.load( './nome_arquivo.pkl')
    meumodelo = joblib.load( './modelo/nome_arquivo.pkl')

def run(data):
    print(data)

    json_ = json.loads(data)
    campos = pd.DataFrame(json_)

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    for col in meumodelo.independentcols:
        if col not in campos.columns:
            campos[col] = 0
    x = campos[meumodelo.independentcols]

    prediction = meumodelo.predict(x)
    try:
      predict_proba = meumodelo.predict_proba(x)
    except Exception as ex:
      predict_proba = None

    ret = json.dumps({'prediction': list(prediction),
                      'proba': list(predict_proba),
                      'author': "Elthon Manhas de Freitas"}, cls=NpEncoder)
    print(ret)

    return app.response_class(response=ret, mimetype='application/json')

