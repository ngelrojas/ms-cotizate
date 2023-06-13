# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import viewsets
import qrcode
from django.http import HttpResponse
import asyncio
# import aiohttp
import io


class QRCodeGenerator(viewsets.ViewSet):
    serializer_class = None
    queryset = None

    def get(self, request, pk=None):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(request.data.get("data"))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        byte_stream = io.BytesIO()
        img.save(byte_stream, 'PNG')
        # saving images in aws s3
        # async def upload_image():
        #     async with aiohttp.ClientSession() as session:
        #         async with session.post(
        #                 'https://api.imgbb.com/1/upload',
        #                 data={
        #                     'key': 'a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5',
        #                     'image': byte_stream.getvalue(),
        #                 },
        #         ) as response:
        #             return await response.json()
        # # recovery url of images from aws s3
        # loop = asyncio.get_event_loop()
        # data = loop.run_until_complete(upload_image())
        # print(data)

        byte_stream.seek(0)

        return HttpResponse(byte_stream, content_type='image/png')
