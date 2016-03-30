from django.contrib import admin
from libro.models import Area, Autor, Devolucion, Editor, Estado, Libro, Prestamo, TipoDocumento

# Register your models here.
admin.site.register(Area)
admin.site.register(Autor)
admin.site.register(Devolucion)
admin.site.register(Editor)
admin.site.register(Estado)
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(TipoDocumento)