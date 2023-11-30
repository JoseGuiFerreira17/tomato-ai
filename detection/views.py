from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config
from .models import Detection
from .serializers import DetectionSerializer
from tensorflow.keras.models import load_model
from django.utils.crypto import get_random_string
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from io import BytesIO
import numpy as np

def upload_directory_res(instance, filename):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    file_name = get_random_string(10, chars)
    return "media/resultado/{0}.png".format(file_name)

class TomatoDetectionView(APIView):
    def post(self, request, format=None):
        import os
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

        original_image = request.data.get("original_image")
        image = original_image
        model = load_model(config("MODEL_PATH"))
        class_names = [
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]

        if original_image is None:
            return Response({"error": "Imagem não encontrada"}, status=status.HTTP_400_BAD_REQUEST)
        original_image = Image.open(original_image)
        original_image = original_image.resize((224, 224))
        original_image = original_image.convert('RGB')
        original_image = np.array(original_image) / 255.0
        original_image = original_image.reshape(1, 224, 224, 3)
        
        predictions = model.predict(original_image)

        predicted_class = np.argmax(predictions)
        predicted_label = class_names[predicted_class]

        for i in range(len(class_names)):
            probability = predictions[0][i]
            formatted_probability = "{:.2f}".format(probability)
        
        
        plt.figure(figsize=(24, 12))
        plt.subplot(1, 2, 1)
        plt.imshow(original_image[0])
        plt.axis('off')
        plt.title(f'Classe prevista: {predicted_label}')

        probabilities = [predictions[0][i] for i in range(len(class_names))]

        plt.subplot(1, 2, 2)
        ax = sns.barplot(x=probabilities, y=class_names, orient='h')

        plt.title('Probabilidades por Classe')
        plt.tight_layout()

        for p in ax.patches:
            width = p.get_width()
            plt.text(width, p.get_y() + p.get_height() / 2, f'{width:.2f}', ha="left")

        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        plt.close()

        image_path = upload_directory_res(None, "result_image.png")  # Pode precisar ajustar dependendo da sua lógica
        with open(image_path, 'wb') as f:
            f.write(image_buffer.getvalue())


        result_instance = Detection(original_image=image, result_image=image_path)
        result_instance.save()

        serializer = DetectionSerializer(result_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
