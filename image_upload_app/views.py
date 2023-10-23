from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import UploadedImage
from .serializers import UploadedImageSerializer
import base64
from django.http import HttpResponse

def user_view(request):
    return HttpResponse("This is the user view.")

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_data = request.data.get('image')  # Get the image data from the request

        if image_data:
            # Encode the image to base64
            base64_image = base64.b64encode(image_data.read()).decode('utf-8')

            # Create a dictionary with the base64 image data
            data = {'base64_image': base64_image}
            file_serializer = UploadedImageSerializer(data=data)

            if file_serializer.is_valid():
                file_serializer.save()
                return Response({'message': 'Image uploaded successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Image data is missing.'}, status=status.HTTP_400_BAD_REQUEST)

class GetImageView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all UploadedImage objects from the database
        images = UploadedImage.objects.all()

        # Serialize the data
        serializer = UploadedImageSerializer(images, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


#=== VIEWS =======
# views.py
from django.shortcuts import render
from .forms import UploadImageForm

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file here (e.g., save it to the database)
            # You can also use the UploadedImage model and serializer you've created.

            return render(request, 'success.html', {'message': 'Image uploaded successfully.'})
    else:
        form = UploadImageForm()

    return render(request, 'upload_form.html', {'form': form})
