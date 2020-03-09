from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw
import json


def getRectangle(faceDictionary):
    """
    Função para criar um retângulo a partir de uma face identificada pelo Azure Face Detection
    :param faceDictionary:
    :return:
    """
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return ((left, top), (right, bottom))


if __name__ == "__main__":
    #Cria o Client da API
    with open("./azurekeys.json", 'r') as jsonfile:
        azurekeys = json.load(jsonfile)

    KEY = azurekeys["FacialDetection"]["KEY"] #Coloque aqui sua chave
    ENDPOINT = azurekeys["FacialDetection"]["ENDPOINT"]  #Coloque aqui seu endpoint (Ponto de Extremidade)
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    imagefile01 = "../datasets/facial/elthon00.jpg" #Imagem com a face única
    NomeDoDonoDoRosto = "Elthon" #Nome da pessoa que está na face única
    imagefile02 = "../datasets/facial/elthon03.jpg" #Imagem com as faces a procurar

    #Identifica FaceIDs da imagem 01
    with open(imagefile01, 'r+b') as w:
        detected_faces01 = face_client.face.detect_with_stream(image=w)

    for face in detected_faces01:
        face_to_find = face.face_id
        print("**** [{0}] foi detectado com face id [{1}] em : {2}".format(NomeDoDonoDoRosto, face.face_id, face.face_rectangle))

    # Identifica FaceIDs da imagem 02
    with open(imagefile02, 'r+b') as w:
        detected_faces02 = face_client.face.detect_with_stream(image=w)
    faces_to_compare = []
    for face in detected_faces02:
        faces_to_compare.append(face.face_id)
        print("**** Detected face id [{0}] on : {1}".format(face.face_id, face.face_rectangle))

    #Chama API para identificar faces similares
    similar_faces = face_client.face.find_similar(face_id=face_to_find, face_ids=faces_to_compare)



    if not similar_faces[0]:
        print('Sem rostos similares na segunda imagem.')
    else:
        for similar in similar_faces:
            print("Face [{0}] similar à face [{1}] com {2} de confiança.".format( face_to_find, similar.face_id, similar.confidence))
        img = Image.open(imagefile02)
        draw = ImageDraw.Draw(img)
        img = Image.open(imagefile02)
        draw = ImageDraw.Draw(img)
        for face in detected_faces02: #Loop de todas as faces na foto 2
            if face.face_id in list(map(lambda x: x.face_id, similar_faces)): #Se a face estiver entre as similares
                draw.rectangle(xy=getRectangle(face), outline='red')
                draw.text(xy=(face.face_rectangle.left, face.face_rectangle.top + face.face_rectangle.height),
                          text=NomeDoDonoDoRosto,
                          fill="red")
        img.show()

    pass

