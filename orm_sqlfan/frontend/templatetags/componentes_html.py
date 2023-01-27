# templatestags/componentes_html.py

from django import template
register = template.Library()

@register.inclusion_tag("componentes\caja_texto.html")
def mostrar_boton(titulo,campo,tipo,campo_llave=False,referencia=""):
    return {"titulo":titulo,
             "campo":campo,"tipo":tipo, 
             "campo_llave":campo_llave,
             "referencia": referencia}