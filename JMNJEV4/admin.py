from django.contrib import admin

# Register your models here.

from .models import Cliente, Producto, Ventas

class Clientedisplay(admin.ModelAdmin):
    #ver clientes
    list_display = ("Rut","Nombre_Cliente","Fecha_Registro","Apellido_Paterno","Apellido_Materno","Correo","Fecha_Nacimiento","Telefono")
    #buscar clientes
    search_fields = ("Nombre_Cliente",)
    #filtrar
    list_filter = ("Rut","Nombre_Cliente","Fecha_Registro","Apellido_Paterno","Apellido_Materno","Correo","Fecha_Nacimiento","Telefono",)

class Productodisplay(admin.ModelAdmin):
    #ver clientes
    list_display = ("codProducto","Nombre_Producto","Proovedor","Categoria","Cantidad_por_Unidad","Valor_en_Peso","Valor_en_Euro","Stock")
    #buscar clientes
    search_fields = ("Nombre_Producto",)
    #filtrar
    list_filter = ("codProducto","Nombre_Producto","Proovedor","Categoria","Cantidad_por_Unidad","Valor_en_Peso","Valor_en_Euro","Stock",)

class Ventasdisplay(admin.ModelAdmin):
    #ver clientes
    list_display = ("Boleta","Producto","cantidad","Venta_Bruto","iva","Total_Venta")
    #buscar clientes
    search_fields = ("Boleta",)
    #filtrar
    list_filter = ("Boleta","Producto","cantidad","Venta_Bruto","iva","Total_Venta",)


admin.site.register(Cliente, Clientedisplay)
admin.site.register(Producto, Productodisplay)
admin.site.register(Ventas, Ventasdisplay)
