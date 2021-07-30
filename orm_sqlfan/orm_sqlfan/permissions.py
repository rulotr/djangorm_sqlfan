from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

class EsGrupoBase(BasePermission):
    nombre_grupo = ''
    
    def has_permission(self, request, view):
        print(view)
        return request.user.groups.filter(name=self.nombre_grupo).exists()
   
class EsGrupoAdministrador(EsGrupoBase):
    nombre_grupo ='Administrador'

class EsGrupoRevisor(EsGrupoBase):
    message = 'No perteneces al grupo de Revisores'
    nombre_grupo ='Revisor'

class EsIpPermitida(BasePermission):
    message = 'Ip no permitida'
    ip_bloqueadas = ['127.0.0.1','192.168.01']

    def has_permission(self, request, view):
        return request.META['REMOTE_ADDR'] not in self.ip_bloqueadas

