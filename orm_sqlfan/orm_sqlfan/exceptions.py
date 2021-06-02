# Django rest framework nos proporciona una serie de clases para 
# manejar exceptiones que utilizamos con mucha frecuencia
# ademas de poder tener mejor organizadas nuestras excepciones

from rest_framework.exceptions import APIException


class Excepcion_FaltanCampos(APIException):
    status_code = 300
    default_code = "faltan_campos_error"
    default_detail  = "Faltan algunos campos que son requeridos" # Si no se le envian los detalles
    
    def __init__(self, detail=None, code=None):
      
        if detail is not None:
            self.detail = {'detalles': self.default_detail, 'Faltan estos campos': detail}
        else: 
            self.detail = {'detalles': "Faltan algunos campos pero no se especificaron cuales"}





from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['codigo_estatus'] = response.status_code

    return response