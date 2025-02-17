from .serializers import QrCodeInfoSerializer
import json, qrcode, io
from .models import Attendance



def from_qr_code_string(qr_code_str : str) -> Attendance | None:
    ##
    # You should decryptograph the string here
    ##
    try:
        obj = json.loads(qr_code_str)
        data = QrCodeInfoSerializer(data = obj)

        if data.is_valid():
            return Attendance.objects.filter(id=obj['id']).get()
    
    except Exception:
        pass
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
