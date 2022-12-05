from django.shortcuts import render
import csv
import random
from .models import Cliente, Producto, Ventas
from django.core.mail import EmailMessage
from barcode.codex import Code128
from barcode.writer import ImageWriter
from reportlab.platypus import (SimpleDocTemplate, Image, Spacer,Table)
from reportlab.lib.pagesizes import A2
from reportlab.lib import colors
import datetime
from django.http import HttpResponse

#redirige a vender
def venderproducto(request):
    return render(request, 'venderproducto.html')
#captura por post los valores del codigo la cantidad
def productoavender(request):
    if request.method == "POST":
        codpro = request.POST['codigoproducto']
        cantidad = request.POST['cantidad']
        #verifica si el stock es menor a la cantidad
        try:
            #trata de buscar el codigo
            producto = Producto.objects.get(codProducto=codpro)
            cantidad = int(cantidad)
            stock = producto.Stock
            if (int(cantidad) > stock or cantidad == 0):
                return render(request, 'venderproducto.html',{"message": "Error Producto no encontrado o stock sobrepasado"})
            else:
                #en caso de cualquier error se devuelve con un mensaje
                return render(request, 'productoavender.html', {"productob": producto, "cantidad": cantidad})
        except Exception:

            return render(request, 'venderproducto.html',{"message": "Error Producto no encontrado o stock sobrepasado"})





#captura por post el codigo de producto la cantidad y el precio en CLP
def productodetalleboleta(request):
    if request.method == "POST":
        codpro = request.POST['codigoproducto']
        cantidad = request.POST['cantidad']
        precioCLP = request.POST['CLP']
        #iva
        iva = 0.19
        #calculo precio bruto precio CLP multiplicado por la cantidad
        preciobruto = int(precioCLP) * int(cantidad)
        #se calcula el IVA
        calcsumar = preciobruto * iva
        #se suma el iva y el precio bruto
        Total = preciobruto + calcsumar
        #busca el producto por el codigo
        producto = Producto.objects.get(codProducto=codpro)
        #guarda el stock
        stock = producto.Stock
        #verifica si el stock es menor a la cantidad
        if (int(cantidad) > stock):
            return render(request, 'venderproducto.html', {"message": "Error Producto no encontrado o stock sobrepasado"})
        else:
            #entrega los valores y redirige el detalle de la boleta
            return render(request, 'productodetalleboleta.html', {"productob": producto,"total":Total,"iva":calcsumar,"preciobruto":preciobruto, "cantidad": cantidad})

def verventas(request):
    # se hace un "select" con el metodo all
    ventas = Ventas.objects.all()
    return render(request, 'verventas.html', {"ventas": ventas})

def concluirventa(request):
    boleta = random.randint(32145, 412397)
    codpro = int(request.POST['codigoproducto'])
    cantidad = int(request.POST['unidades'])
    preciobruto = int(request.POST['preciobruto'])
    iva = float(request.POST['iva'])
    total = float(request.POST['total'])
    productoadescontar = Producto.objects.get(codProducto=codpro)
    #descuenta el stock actual con las unidades compradas
    stockdescontado = int(productoadescontar.Stock) - cantidad
    #actualiza el stock
    productoadescontar.Stock = stockdescontado
    #guarda en la bd
    productoadescontar.save()

    venta = Ventas(Boleta=boleta, Producto=codpro, cantidad=cantidad, Venta_Bruto=preciobruto, iva=iva,Total_Venta=int(total))
    venta.save()
    return render(request, 'dashboard.html')

def buscarproducto(request):
    return render(request, 'buscarproducto.html')

def productobuscado(request):
    if request.method == "POST":
        codpro = request.POST['codigoproducto']
        try:
            #Prueba encontrar el codigo
            producto = Producto.objects.get(codProducto=codpro)
            return render(request, 'productobuscado.html', {"productob": producto})
        except Exception:
            #en caso de cualquier error se devuelve con un mensaje
            return render(request, 'buscarproducto.html', {"message": "Error Producto no encontrado"})





def dashboard(request):
    return render(request, 'dashboard.html')

def verclientes(request):
    # se hace un "select" con el metodo all
    clientes = Cliente.objects.all()
    return render(request, 'verclientes.html', {"clientes":clientes})

def verproductos(request):
    #se hace un "select" con el metodo all
    productos = Producto.objects.all().order_by("codProducto")
    return render(request, 'verproductos.html',{"productos":productos})


def crearProductos(request):

    # funcion de cambio a peso chileno
    def euroapeso(euro):
        peso = 929.73 * euro
        return peso

    # funcion para crear el codigo debarra
    def codigodebarra(codproducto):
        # abre o selecciona directorio donde se va a guardar la imagen y con el tipo de nombre y formato
        with open(
                'JMNJEV4/static/barcode/' + codproducto + '.jpg',
                'wb') as f:
            # escribe en formato de imagen el codigo
            Code128(codproducto, writer=ImageWriter()).write(f)

    # guarda el csv delos productos
    csvproductos = 'JMNJEV4/Django_productoss.csv'
    # abre el archivo y especifica su codificacion en utf-8
    with open(csvproductos, encoding='utf-8') as f:
        reader = csv.reader(f)
        # salta a la siguiente fila ignorando los titulos
        next(f)
        # lee las columnas
        for row in reader:
            # variable que guarda el signo euro
            caracter = '€'
            # entregara el codigo de producto a la funcion del codigo de barra
            codigodebarra(row[0])
            # for que analiza todos los caracteres que tenga la variable caracter
            for x in range(len(caracter)):
                # variable que almacena el valor de la columna de los precios como string
                cambiopreciofloat = row[5]
                # variable nueva el cual almacena el precio euro como un FLOAT y con la funcion replace elimina el signo del euro para poder ser parseado
                cambiopreciofloatnuevo = float(cambiopreciofloat.replace(caracter[x], ""))
                # almacena el nuevo precio como int desde el retorno de la funcion
                nuevoprecio = int(euroapeso(cambiopreciofloatnuevo))
                print(
                    "Codigo Producto: {0}\nNombre Producto: {1}\nProovedor: {2}\nCategoria: {3}\nCantidad por Unidad: {4}\nPrecio Unidad: ${5}\nUnidades en existencias: {6}\n"
                    .format(row[0], row[1], row[2], row[3], row[4], nuevoprecio, row[6]))

                producto = Producto(codProducto=row[0], Nombre_Producto=row[1], Proovedor=row[2],
                Categoria=row[3],
                Cantidad_por_Unidad=row[4], Valor_en_Peso=nuevoprecio, Valor_en_Euro=cambiopreciofloatnuevo, Stock=row[6])
                producto.save()

    return render(request, 'productoscreados.html')
def graficoproducto(request):
    productos = Producto.objects.all()
    listaproductosnombre = []
    listapreciosclp = []
    cont = 0
    for x in productos:
        nombreproducto = str(x.Nombre_Producto)
        precioCLP = int(x.Valor_en_Peso)
        tdolares = 2650

        if (precioCLP > tdolares):
            cont = cont + 1
            listaproductosnombre.append(nombreproducto)
            listapreciosclp.append(precioCLP)
            print(x.Nombre_Producto)
            print(precioCLP)
            print(listaproductosnombre)
            print(listapreciosclp)
    return render(request, 'graficoproducto.html', {"productos": listaproductosnombre, "preciosclp": listapreciosclp})

def graficocliente(request):
    clientes = Cliente.objects.all()
    listaclientesmenorigual35 = []
    listaedades = []
    cont = 0
    for x in clientes:
        edad = str(x.Fecha_Nacimiento)
        numero = int(x.Numero_Cliente)
        anonacimiento = edad[:4]
        anos = 2022 - int(anonacimiento)
        if (anos <= 35 and numero > 1033):
            cont = cont + 1
            listaclientesmenorigual35.append(x)
            listaedades.append(anos)
            print(x.Nombre_Cliente)
            print(anos)
            print(numero)
            print(listaclientesmenorigual35)
            print(listaedades)
    return render(request, 'graficocliente.html', {"clientes":listaclientesmenorigual35,"edades":listaedades})

def correomasivoTODOS(request):
    cliente = Cliente.objects.all()
    for clientes in cliente:
        print(clientes.Correo)
        # contrasena desde el rut
        contrasena = clientes.Rut
        contrsena = contrasena[4:-2]
        print(contrsena)
        doc = SimpleDocTemplate("JMNJEV4/static/pdf/" + clientes.Rut + "-produc.pdf", pagesize=A2, encrypt=contrsena)
        story = []
        datos = [['Codigo de Barra', "Nombre Producto", "Cantidad por Unidad", "Precio CLP", "Precio Euro", "Proovedor"]]
        listaproducto = Producto.objects.all()
        for pro in listaproducto:
            barcode = Image('JMNJEV4/static/barcode/' + str(pro.codProducto) + '.jpg', width=100, height=50)
            datos.append([barcode, pro.Nombre_Producto, pro.Cantidad_por_Unidad, '$'+str(pro.Valor_en_Peso), '€'+str(pro.Valor_en_Euro),
                          pro.Proovedor])
        tabla = Table(data=datos,
                      style=[
                          ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                          ('BOX', (0, 0), (-1, -1), 2, colors.black),
                          ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                      ])
        story.append(tabla)
        story.append(Spacer(0, 15))
        doc.build(story)

        # crea un correo a enviar
        email = EmailMessage(
            'GRAN OFERTASO UNIMARC',
            'CLIENTE PRECIOS IMPERDIBLES en EUROS Y CLP Para desbloquear use sus 4 ultimos digitos de su rut sin codigo verificador',
            '#remitente',
            [clientes.Correo],
        )
        # adjunta un archivo al correo
        email.attach_file('JMNJEV4/static/pdf/' + clientes.Rut + '-produc.pdf')
        # envia el correo
        email.send()
    return render(request, 'correoenviado.html')



def correouncliente(request):

    return render(request, 'clientecorreo.html')

def enviarcorreocliente(request):
    if request.method == "POST":
        correo = request.POST['correo']
        try:
            cliente = Cliente.objects.get(Correo=correo)
            # contrasena desde el rut
            contrasena = cliente.Rut
            contrsena = contrasena[4:-2]
            print(contrsena)
            doc = SimpleDocTemplate("JMNJEV4/static/pdf/" + cliente.Rut + "-produc.pdf", pagesize=A2, encrypt=contrsena)
            story = []
            datos = [
                ['Codigo de Barra', "Nombre Producto", "Cantidad por Unidad", "Precio CLP", "Precio Euro", "Proovedor"]]
            listaproducto = Producto.objects.all()
            for pro in listaproducto:
                barcode = Image('JMNJEV4/static/barcode/' + str(pro.codProducto) + '.jpg', width=100, height=50)
                datos.append([barcode, pro.Nombre_Producto, pro.Cantidad_por_Unidad, '$' + str(pro.Valor_en_Peso),
                              '€' + str(pro.Valor_en_Euro), pro.Proovedor])
            tabla = Table(data=datos,
                          style=[
                              ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                              ('BOX', (0, 0), (-1, -1), 2, colors.black),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                              ])
            story.append(tabla)
            story.append(Spacer(0, 15))
            doc.build(story)

            # crea un correo a enviar
            email = EmailMessage(
                'GRAN OFERTASO UNIMARC',
                'CLIENTE PRECIOS IMPERDIBLES en EUROS Y CLP Para desbloquear use sus 4 ultimos digitos de su rut sin codigo verificador',
                '#remitente',
                [cliente.Correo],
            )
            # adjunta un archivo al correo
            email.attach_file('JMNJEV4/static/pdf/' + cliente.Rut + '-produc.pdf')
          # envia el correo
            email.send()

        except Exception:
            return render(request, 'clientecorreo.html', {"message":"Cliente no encontrado"})


        return render(request, 'correoenviado.html')




def correomasivo34anos(request):
    #obtiene los clientes haciendo un select a la bd
    cliente = Cliente.objects.all()
    cont = 0
    for clientes in cliente:
        fecha_naci = clientes.Fecha_Nacimiento
        print(fecha_naci)
        anocomparacion = datetime.date(1988,12,12)
        print(anocomparacion)
        if (fecha_naci <=anocomparacion):
            #cuenta cuantos hay con mas de 34 anos
            cont = cont + 1
            print(clientes.Correo)
            print(clientes.Fecha_Nacimiento)
            print(cont)
            # contrasena desde el rut
            contrasena = clientes.Rut
            contrsena = contrasena[4:-2]
            #selecciona donde se guardara y con que nombre y que tipo de hoja tendra el pdf
            doc = SimpleDocTemplate("JMNJEV4/static/pdf/" + clientes.Rut + "-produc.pdf", pagesize=A2, encrypt=contrsena)
            story = []
            #en este array se pone los titulos que tendra
            datos = [
                ['Codigo de Barra', "Nombre Producto", "Cantidad por Unidad", "Precio CLP", "Precio Euro", "Proovedor"]]
            #obtiene los productos
            listaproducto = Producto.objects.all()
            #recorre la lista de los productos
            for pro in listaproducto:
                #busca la imagen del codigo de barra de cada producto
                barcode = Image('JMNJEV4/static/barcode/' + str(pro.codProducto) + '.jpg', width=100, height=50)
                #anade todos los datos en la lista de datos
                datos.append([barcode, pro.Nombre_Producto, pro.Cantidad_por_Unidad, '$'+str(pro.Valor_en_Peso), '€'+str(pro.Valor_en_Euro),
                              pro.Proovedor])
            #diseno donde se va a mostrar el pdf
            tabla = Table(data=datos,
                          style=[
                              ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                              ('BOX', (0, 0), (-1, -1), 2, colors.black),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                          ])
            #lo anade al story donde este tendra el diseno con los datos
            story.append(tabla)
            story.append(Spacer(0, 15))
            #crea el pdf
            doc.build(story)
            # crea un correo a enviar
            email = EmailMessage(
                'GRAN OFERTASO UNIMARC',
                'CLIENTE PRECIOS IMPERDIBLES en EUROS Y CLP Para desbloquear use sus 4 ultimos digitos de su rut sin codigo verificador',
                '#remitente',
                [clientes.Correo],
            )
            #adjunta un archivo al correo
            email.attach_file('JMNJEV4/static/pdf/' + clientes.Rut + '-produc.pdf')
            #envia el correo
            email.send()
    return render(request, 'correoenviado.html')

def correomasivo1033(request):
    # obtiene los clientes haciendo un select a la bd
    cliente = Cliente.objects.all()
    cont = 0
    for clientes in cliente:
        numerocliente = clientes.Numero_Cliente
        if (numerocliente > 1033):
            # cuenta cuantos hay con numero mayor a 1033
            cont = cont + 1
            print(clientes.Numero_Cliente)
            print(cont)
            #contrasena desde el rut
            contrasena = clientes.Rut
            contrsena = contrasena[4:-2]
            # selecciona donde se guardara y con que nombre y que tipo de hoja tendra el pdf
            doc = SimpleDocTemplate("JMNJEV4/static/pdf/" + clientes.Rut + "-produc.pdf", pagesize=A2, encrypt=contrsena)
            story = []
            # en este array se pone los titulos que tendra
            datos = [
                ['Codigo de Barra', "Nombre Producto", "Cantidad por Unidad", "Precio CLP", "Precio Euro", "Proovedor"]]
            # obtiene los productos
            listaproducto = Producto.objects.all()
            # recorre la lista de los productos
            for pro in listaproducto:
                # busca la imagen del codigo de barra de cada producto
                barcode = Image('JMNJEV4/static/barcode/' + str(pro.codProducto) + '.jpg', width=100, height=50)
                # anade todos los datos en la lista de datos
                datos.append(
                    [barcode, pro.Nombre_Producto, pro.Cantidad_por_Unidad, '$'+str(pro.Valor_en_Peso), '€'+str(pro.Valor_en_Euro),
                     pro.Proovedor])
            # diseno donde se va a mostrar el pdf
            tabla = Table(data=datos,
                          style=[
                              ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                              ('BOX', (0, 0), (-1, -1), 2, colors.black),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                          ])
            # lo anade al story donde este tendra el diseno con los datos
            story.append(tabla)
            story.append(Spacer(0, 15))
            # crea el pdf
            doc.build(story)
            # envia los emails
            email = EmailMessage(
                'GRAN OFERTASO UNIMARC',
                'CLIENTE PRECIOS IMPERDIBLES en EUROS Y CLP Para desbloquear use sus 4 ultimos digitos de su rut sin codigo verificador',
                '#remitente',
                [clientes.Correo],
            )
            email.attach_file('JMNJEV4/static/pdf/' + clientes.Rut + '-produc.pdf')
            email.send()
    return render(request, 'correoenviado.html')

def publicidad(request):
    return render(request, 'publicidad.html')



def crearclientes(request):
    # lista que almacenara los ruts
    listaruts = ['14355566-4']
    # funcion que dara los ruts automaticos
    def rut():
        # guardara el caracter del codigo verificador
        caracter = '-'
        contnuevorut = 0
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
            reader = csv.reader(fa)
            # salta a la siguiente fila ignorando los titulos
            next(fa)
            # recorrera las columnas
            for row in reader:
                # recorre la lista de los ruts
                for s in listaruts:
                    for row in reader:
                        # guardara el valor del rut de la posicion
                        rutverificar = f'{s}'
                        # borrara el signo "-" verificador
                        rutverificar = rutverificar.replace(caracter, "")
                        # eliminara el ultimo digito verificador
                        rutverificar = rutverificar[:-1]
                        # verifica si el rut es igual a uno ya guardado
                        if (rutverificar == s[:-2]):
                            # se asigna + 1 al contador
                            contnuevorut = 1
                            # se suma +1 al rut recortado anteriormente
                            nuevorutfinal = int(rutverificar) + 1
                        # verifica si el nuevo rut entregado sigue siendo igual al anterior
                        if (str(nuevorutfinal) != str(s[:-2])):
                            # variable que sera el nuevo codigo verificador con un numero random
                            codigodigitador = random.randint(0, 9)
                            # verifica si el contador es mayor a 0
                            if (contnuevorut > 0):
                                # guardara el nuevo rut concatenando strings entre el nuevo rut, el - y el codigo verificador
                                nuevorutfinal = str(nuevorutfinal) + "-" + str(codigodigitador)
                                # agregara el rut a la lista
                                listaruts.append(nuevorutfinal)
                                #print('AAARUTENIF',nuevorutfinal)
                                #print('AAARUTENIF', listaruts)
                                #print("HAY DE RUTS", len(listaruts))
                                break
                        break
                break

    # lista email
    listaemail = []

    # funcion email
    def email(pnombre, apellidopaterno, pamaterno):
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
            reader = csv.reader(fa)
            # salta a la siguiente fila ignorando los titulos
            next(fa)
            # guarda los nombres y apellidos en las variables
            prnombre = pnombre[:1]
            prmaterno = pamaterno[:1]
            # estructura del email son el dominio
            emailnuevo = prnombre + apellidopaterno + prmaterno
            # estructura con el dominio
            emailfinal = emailnuevo + "@djangocorreo.tk"

            # contador puesto en 0
            contador = 0
            # recorrera el csv
            for row in reader:
                # cuenta y verifica si hay emails repetidos en la lista
                if (listaemail.count(emailfinal) >= 1):
                    # se suma + al contador
                    contador = contador + 1
                    # se le agrega a la estructura sin dominio el valor sumatorio
                    emailnuevor = emailnuevo + str(contador)
                    # se le agrega al email el dominio
                    emailfinal = emailnuevor + "@djangocorreo.tk"
                    # se agrega el email a la lista
                    listaemail.append(emailfinal)
                    # indica que email fue repetido
                    # print('EMAIL REPETIDO', emailfinal)
                    # detiene el ciclo para no repetir el mismo email
                    break
                # verifica si no se repite ningun email
                elif (listaemail.count(emailfinal) == 0):
                    # agrega el email directamente a la lista
                    listaemail.append(emailfinal)
                    # indica que el email no tiene errores
                    # print('EMAIL BUENO', emailfinal)
                    break

    listatelefono = []

    # funcion para crear telefono
    def telefono():
        cont = 0
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
            reader = csv.reader(fa)
            # salta a la siguiente fila ignorando los titulos
            next(fa)
            # recorrera la lista de ruts
            for row in reader:
                a = listaruts[cont]
                # guardara el telefono concatenando el rut + el cod de cliente
                telefono = a[:-2] + f'{row[1]}'
                # agrega a la lista
                listatelefono.append(telefono)
                print('telefonoo',telefono)
                print(listatelefono)
                cont = cont + 1





    def crearclientesbd():
        caracterfecha = '/'
        contador = 0
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
            reader = csv.reader(fa)
            # salta a la siguiente fila ignorando los titulos
            next(fa)
            for row in reader:
                #proceso para poder guardar la fecha de registro en la BD sin errores
                fecharegistroca = f'{row[2]}'
                fecharegistroulti = fecharegistroca[-4:] + '-'
                fecharegistroca = fecharegistroca[:-5]
                fecharegistromes = fecharegistroca[-1:]
                if (fecharegistromes == '0'):
                    fecharegistromes = '1' + fecharegistromes
                fecharegistroca = fecharegistroca[:2]
                fecharegistroca = fecharegistroca.replace(caracterfecha, "")
                fecharegistroca = fecharegistromes + '-' + fecharegistroca
                #borrara el signo "/" de la fecha por un -
                fecharegistroca = fecharegistroca.replace(caracterfecha, "-")
                fecharegistroca =  fecharegistroulti + fecharegistroca

                # proceso para poder guardar la fecha de nacimiento en la BD sin errores
                fechanacimientoca = f'{row[8]}'
                fechanacimientoulti = fechanacimientoca[-4:] + '-'
                fechanacimientoca = fechanacimientoca[:-5]
                fechanacimientomes = fechanacimientoca[-1:]
                fechanacimientoca = fechanacimientoca[:2]
                fechanacimientoca = fechanacimientoca.replace(caracterfecha[x], "")
                fechanacimientoca = fechanacimientomes + '-' + fechanacimientoca
                # borrara el signo "/" de la fecha por un -
                fechanacimientoca = fechanacimientoca.replace(caracterfecha[x], "-")
                fechanacimientoca = fechanacimientoulti + fechanacimientoca
                print(
                    "Rut: {0}\nNumero Cliente: {1}\nNombre Cliente: {5}\nFecha Ingreso: {2}\nApellido Paterno: {3}\nApellido Materno: {4}\nCorreo: {6}\nTelefono: {7}\nFecha Nacimiento: {8}\n"
                    .format(listaruts[contador],row[1], fecharegistroca, row[3], row[4], row[5], listaemail[contador],
                            listatelefono[contador], fechanacimientoca))
                #ejecutar una sola vez
                cliente = Cliente(Rut=listaruts[contador], Numero_Cliente=row[1],Nombre_Cliente=row[5], Fecha_Registro=fecharegistroca,
                Apellido_Paterno=row[3],
                Apellido_Materno=row[4], Correo=listaemail[contador], Fecha_Nacimiento=fechanacimientoca, Telefono=listatelefono[contador])
                cliente.save()
                contador = contador + 1
    #crea clientes desde los companeros del ramo
    def crearcompaneros():
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/alumnos.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente,encoding='utf-8') as fa:
            reader = csv.reader(fa, delimiter=';')
            for row in reader:
                print(
                    "Rut: {4}\nNombre: {0}\nApellido Paterno: {1}\nApellido Materno: {2}\nEmail: {3}"
                    .format(row[0], row[1], row[2], row[3],row[4]))

                cliente = Cliente(Rut=row[4], Numero_Cliente="0",Nombre_Cliente=row[0], Fecha_Registro="2000-01-01",
                Apellido_Paterno=row[1],
                Apellido_Materno=row[2], Correo=row[3], Fecha_Nacimiento="2000-01-01", Telefono="12345")
                cliente.save()




    # comienza a crear los emails
    caracter = '-'
    for x in range(len(caracter)):
        # guarda el csv del cliente
        csvcliente = 'JMNJEV4/clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
                reader = csv.reader(fa)
                # salta a la siguiente fila ignorando los titulos
                next(fa)
                # recorre la lista de los ruts
                for row in reader:
                    email(row[5], row[3], row[4])

    # Crea los ruts
    rut()
    # crea los telefonos
    telefono()
    #crea los clientes con los ruts y telefonos y emails en la bd
    crearclientesbd()
    #crea los companeros de la carrera
    crearcompaneros()
    return render(request, 'Usuarioscreados.html')




