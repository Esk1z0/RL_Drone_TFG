from iprocess import IProcess
from keras.applications import EfficientNetB7
from keras.applications.efficientnet import decode_predictions
from keras.preprocessing import image
import numpy as np

class CameraRecognitionProcess(IProcess):

    def __init__(self):
        self.__model = self.__get_model()

    def process_data(self, data) -> dict:
        pass

    def __get_model(self):
        model = EfficientNetB7()
        return model

    def __preprocess(self, img):
        x = np.expand_dims(img, axis=0)
        return x

    def __predict(self, data, model):
        preds = model.predict(data)
        return preds

    def __decode_prediction(self, preds):
        decoded_preds = decode_predictions(preds, top=3)[0]
        return decoded_preds