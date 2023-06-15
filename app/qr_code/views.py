import io
import qrcode
import asyncio
import aiohttp
import uuid
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


class QRCodeGenerator(viewsets.ViewSet):
    serializer_class = None
    queryset = None

    async def upload_to_s3(self, image, bucket_name, key):
        async with aiohttp.ClientSession() as session:
            url = f'https://{bucket_name}.s3.amazonaws.com/qr-code/{key}'
            headers = {'Content-Type': 'image/png'}
            async with session.put(url, data=image, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f'Failed to upload image to S3. Status code: {response.status}')

    async def generate_qr_code(self, data):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        byte_stream = io.BytesIO()
        img.save(byte_stream, 'PNG')
        byte_stream.seek(0)

        return byte_stream.getvalue()

    def generate_qr_code_and_upload(self, request):
        data = request.data.get("data")
        loop = asyncio.new_event_loop()
        image_data = loop.run_until_complete(self.generate_qr_code(data))

        # Upload image to S3 bucket
        # s3://citi-qr-code/qr-code/
        bucket_name = 'citi-qr-code'
        unique_key = str(uuid.uuid4())
        key = f'{unique_key}.png'
        loop.run_until_complete(self.upload_to_s3(image_data, bucket_name, key))
        return Response({
            "data": key
        }, status=status.HTTP_200_OK)
        # return HttpResponse(image_data, content_type='image/png')

    def get(self, request, pk=None):
        return self.generate_qr_code_and_upload(request)
