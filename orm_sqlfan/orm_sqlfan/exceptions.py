# Django rest framework nos proporciona una serie de clases para 
# manejar exceptiones que utilizamos con mucha frecuencia
# ademas de poder tener mejor organizadas nuestras excepciones

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

#REST_FRAMEWORK = {
#    'EXCEPTION_HANDLER': 'orm_sqlfan.exceptions.custom_exception_handler'
#}

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['codigo_estatus'] = response.status_code

    return response


#"nombre": ["This field is required."]

class Excepcion_FaltanCampos(APIException):
    status_code = 300
    #default_detail = self.details
    #default_detail = {"error:" : "Faltan campos", "campos": parent.default_detail}
    default_code = "error"

    def __init__(self, detail=None, code=None):
      
        if detail is not None:
            self.detail = {'Faltan estos campos': detail}
        else: self.detail = {'detail': "Faltan algunos campos pero no se especificaron cuales"}
