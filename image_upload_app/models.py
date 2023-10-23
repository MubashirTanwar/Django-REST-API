import base64
from django.db import models

class UploadedImage(models.Model):
    base64_image = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # new_field = models.CharField(max_length=140, default='nulled')
    def save_base64_image(self, image_data):
        self.base64_image = base64.b64encode(image_data).decode('utf-8')

    def load_base64_image(self):
        return base64.b64decode(self.base64_image)
