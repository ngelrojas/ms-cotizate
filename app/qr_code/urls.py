from django.urls import path
# from .views import generate_qr_code, decode_qr_code
from .views import QRCodeGenerator

urlpatterns = [
    path('generate-qr-code/', QRCodeGenerator.as_view(
        {"post": "post"}
    ), name='generate-qr-code'),
    # path('decode-qr-code/', decode_qr_code, name='decode-qr-code'),
]
