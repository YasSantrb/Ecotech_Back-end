# NOVO permissions.ESTÁVEL.py

from rest_framework import permissions

class IsDoador(permissions.BasePermission):
    def has_permission(self, request, view):
        usuario = request.user
        return bool(usuario and usuario.is_authenticated and 
                    hasattr(usuario, 'userprofile') and 
                    usuario.userprofile.tipo_usuario == 'DOADOR') 
    
class IsEmpresa(permissions.BasePermission):
    def has_permission(self, request, view):
        usuario = request.user
        return bool(usuario and usuario.is_authenticated and 
                    hasattr(usuario, 'userprofile') and 
                    usuario.userprofile.tipo_usuario == 'EMPRESA')