from django.db import models

# Create your models here.
class Cliente(models.Model):
    Rut = models.CharField(max_length=1000)
    Numero_Cliente = models.BigIntegerField()
    Nombre_Cliente= models.CharField(max_length=1000)
    Fecha_Registro= models.DateField()
    Apellido_Paterno= models.CharField(max_length=1000)
    Apellido_Materno= models.CharField(max_length=1000)
    Correo= models.CharField(max_length=1000)
    Fecha_Nacimiento= models.DateField()
    Telefono= models.BigIntegerField()

class Producto(models.Model):
    codProducto= models.BigIntegerField()
    Nombre_Producto= models.CharField(max_length=1000)
    Proovedor= models.CharField(max_length=1000)
    Categoria = models.CharField(max_length=1000)
    Cantidad_por_Unidad = models.CharField(max_length=1000)
    Valor_en_Peso = models.BigIntegerField()
    Valor_en_Euro = models.FloatField()
    Stock = models.BigIntegerField()

class Ventas(models.Model):
    Boleta = models.BigIntegerField()
    Producto = models.BigIntegerField()
    cantidad = models.BigIntegerField()
    Venta_Bruto = models.BigIntegerField()
    iva = models.FloatField()
    Total_Venta= models.BigIntegerField()





    
