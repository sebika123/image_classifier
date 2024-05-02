from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageUploadSerializer
from efficientnet.tfkeras import EfficientNetB0
import numpy as np
from PIL import Image
import io
from tensorflow.keras.applications.imagenet_utils import decode_predictions


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer._validated_data['image']
            img = Image.open(io.BytesIO(image.read())).resize((224,224))
            img_array = np.expand_dims(np.array(img), axis=0)/ 255.0

       
            model = EfficientNetB0(weights = 'imagenet')

    
            predictions = model.predict(img_array)
            decoded_predictions = decode_predictions(predictions)

          
            top_prediction = decoded_predictions[0][0]
            class_label = top_prediction[1]
            
            class_probability = top_prediction[2]
            print(class_label)
            return Response({'class_label': class_label,
            'class_probability': class_probability,
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)