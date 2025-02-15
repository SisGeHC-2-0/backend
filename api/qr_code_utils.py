from .serializers import QrCodeInfoSerializer
import json, qrcode, io




def from_qr_code_string(qr_code_str : str) -> QrCodeInfoSerializer | None:
    ##
    # You should decryptograph the string here
    ##

    data = QrCodeInfoSerializer(json.loads(qr_code_str))

    if data.is_valid():
        return data
    return None    

def to_qr_code_str(data) -> str:
    data_str = json.dumps(data)

    ##
    # You should cryptograph the string here
    ##

    return data_str

def to_qr_code_byte_stream(data):
    data_str = to_qr_code_str(data)

    byte_stream = io.BytesIO()
    qrcode.make(data_str).save(byte_stream, format='PNG')
    byte_stream.seek(0)

    return byte_stream
