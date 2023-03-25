from rest_framework import viewsets ,generics,serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
import qrcode
import qrcode.image.pil
import cv2
import io

class QrViewSet(APIView): 
    def post(self, request, *args, **kwargs):
        binary_data = request.data.get('image_data')
        binary_data = bytes(binary_data)

        if (not binary_data):
            return Response({'error': 'バイナリデータが見つかりませんでした。'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image = Image.open(io.BytesIO(binary_data))
        except IOError:
            return Response({'error': '画像を開くことができませんでした。'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        qr_code = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr_code.add_data(image)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")

        img = cv2.imread(img_qr)
        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

        if retval == False or decoded_info == "":
            return Response({'error': 'QRコードからデータを読み取ることができませんでした。'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'qr_data': decoded_info})