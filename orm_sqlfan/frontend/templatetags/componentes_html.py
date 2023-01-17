#templates/components/boton_busqueda.py
from django import template
register = template.Library()

@register.inclusion_tag("componentes/boton_busqueda.html")
def mostrar_boton(filtro):
    return {"filtro": filtro}