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
    #Cria o Client
    KEY = "XXXX"  # Coloque aqui sua chave
    ENDPOINT = "https://XXXX/"  # Coloque aqui seu endpoint (Ponto de Extremidade)
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    imagefile01 = "./elthon00.jpg"
    imagefile02 = "./elthon03.jpg"

    #Identifica FaceIDs da imagem 01
    with open(imagefile01, 'r+b') as w:
        detected_faces01 = face_client.face.detect_with_stream(image=w)

    for face in detected_faces01:
        face_to_find = face.face_id
        print("**** Detected face id [{0}] on : {1}".format(face.face_id, face.face_rectangle))

    # Identifica FaceIDs da imagem 02
    with open(imagefile02, 'r+b') as w:
        detected_faces02 = face_client.face.detect_with_stream(image=w)
    faces_to_compare = []
    for face in detected_faces02:
        faces_to_compare.append(face.face_id)
        print("**** Detected face id [{0}] on : {1}".format(face.face_id, face.face_rectangle))

    img = Image.open(imagefile02)
    draw = ImageDraw.Draw(img)
    similar_faces = face_client.face.find_similar(face_id=face_to_find, face_ids=faces_to_compare)
    if not similar_faces[0]:
        print('Sem rostos similares na segunda imagem.')
    else:
        img = Image.open(imagefile02)
        draw = ImageDraw.Draw(img)
        for face in detected_faces02:
            if face.face_id in list(map(lambda x: x.face_id, similar_faces)):
                draw.rectangle(getRectangle(face), outline='red')
        img.show()

    pass

