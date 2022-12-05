
CAMBIAR NOMBRE DE SETTINGSDEFAULT.PY A settings.py
Configurar settings.py

ingresar usuario y contrasena de postgres

ingresar usuario y contrasena de email para envio de correos

en JMNJEV4/views.py buscar 

en el editor de codigo ctrl + f y buscar
"#remitente"

y cambiar por el email ingresado en settings


Para no tener problemas con la base de datos

hay que ir a /JMNJEV4/migrations

Y eliminar el archivo 0001_initial.py

luego en una shell en la carpeta del manage.py
ejecutar

1. python manage.py makemigrations

2. python manage.py migrate

luego estaria funcional

ejecutar

  python manage.py runserver

En el dashboard principal hay un mensaje que es importante,
NO ejecutar más de 1 vez cada creación de los clientes o productos, ya que podria provocar malfuncionamiento de la app considerando que todos los clientes y productos son únicos

para ir al dashboard principal la ruta es

/JMNJEV4/dashboard
