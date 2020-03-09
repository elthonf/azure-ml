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


def drawCrossesOnFace(faceLandmarks, size=2, color='white'):
    fl = faceLandmarks.as_dict()
    for l in fl.keys():
        x = fl[l]['x']
        y = fl[l]['y']
        draw.line(((x - size, y - size), (x + size, y + size)), fill=color)
        draw.line(((x - size, y + size), (x + size, y - size)), fill=color)
    pass

if __name__ == "__main__":
    #Cria o Client
    KEY = "XXXXX" #Coloque aqui sua chave
    ENDPOINT = "XXXXXX/" #Coloque aqui seu endpoint (Ponto de Extremidade)
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


    #imagefile = "./face_varias.jpg"
    imagefile = "./face_unica.jpg"

    return_face_attributes = ["age", "gender", "headPose", "smile", "hair", "accessories", "facialHair", "glasses", "emotion",  "noise", "occlusion", "blur", "makeup"]
    with open(imagefile, 'r+b') as w:
        detected_faces = face_client.face.detect_with_stream(image=w, return_face_landmarks = True, return_face_attributes = return_face_attributes)


    img = Image.open(imagefile)
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        print("**** Detected face id [{0}] on : {1}".format(face.face_id, face.face_rectangle))
        print("Landmarks: ")
        print(json.dumps(face.face_landmarks.as_dict(), indent=4) )
        print("Atributes: ")
        print(json.dumps(face.face_attributes.as_dict( ), indent=4) )
        draw.rectangle(getRectangle(face), outline='red')
        drawCrossesOnFace(face.face_landmarks, size=2, color='white')
    img.show()

    pass