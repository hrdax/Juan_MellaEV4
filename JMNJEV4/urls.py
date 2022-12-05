from django.urls import path
from . import views


urlpatterns = [
    path('verproductos', views.verproductos, name='verproductos'),
    path('verclientes', views.verclientes, name='verclientes'),
    path('crearclientes', views.crearclientes, name='crearclientes'),
    path('crearProductos', views.crearProductos, name='crearproductos'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('buscarproducto', views.buscarproducto, name='buscarproducto'),
    path('productobuscado', views.productobuscado, name='productobuscado'),
    path('venderproducto', views.venderproducto, name='venderproducto'),
    path('productoavender', views.productoavender, name='productoavender'),
    path('productodetalleboleta', views.productodetalleboleta, name='productodetalleboleta'),
    path('concluirventa', views.concluirventa, name='concluirventa'),
    path('verventas', views.verventas, name='verventas'),
    path('publicidad', views.publicidad, name='publicidad'),
    path('correomasivoTODOS', views.correomasivoTODOS, name='correomasivoTODOS'),
    path('correomasivo34anos', views.correomasivo34anos, name='correomasivo34anos'),
    path('correouncliente', views.correouncliente, name='correouncliente'),
    path('enviarcorreocliente', views.enviarcorreocliente, name='enviarcorreocliente'),
    path('correomasivo1033', views.correomasivo1033, name='correomasivo1033'),
    path('graficocliente', views.graficocliente, name='graficocliente'),
    path('graficoproducto', views.graficoproducto, name='graficoproducto'),


]