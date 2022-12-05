import csv
import random
from ..models import Cliente

#lista que almacenara los ruts
listaruts = ['1435566-4']

#funcion que dara los ruts automaticos
def rut():
    #guardara el caracter del codigo verificador
    caracter = '-'
    contnuevorut = 0
    # guarda el csv del cliente
    csvcliente = 'clientee.csv'
    # abre el csv y especifica su codificacion de lectura en utf8
    with open(csvcliente, encoding='utf-8') as fa:
        reader = csv.reader(fa)
        # salta a la siguiente fila ignorando los titulos
        next(fa)
        #recorrera las columnas
        for row in reader:
            #recorre el caracter para ser usado despues
            for x in range(len(caracter)):
                #recorre la lista de los ruts
                for s in listaruts:
                    #verifica si longitud de la lista sea igual a 264 para que no siga infinitamente
                    if (len(listaruts) == 264):
                        #sale del for
                        break
                    #guardara el valor del rut de la posicion
                    rutverificar = f'{s}'
                    #borrara el signo "-" verificador
                    rutverificar = rutverificar.replace(caracter[x],"")
                    #eliminara el ultimo digito verificador
                    rutverificar = rutverificar[:-1]
                    #verifica si el rut es igual a uno ya guardado
                    if (rutverificar == s[:-2]):
                        #se asigna + 1 al contador
                        contnuevorut = 1
                        #se suma +1 al rut recortado anteriormente
                        nuevorutfinal = int(rutverificar) + 1
                    #verifica si el nuevo rut entregado sigue siendo igual al anterior
                    if (str(nuevorutfinal) != str(s[:-2])):
                        #variable que sera el nuevo codigo verificador con un numero random
                        codigodigitador = random.randint(0, 9)
                        #verifica si el contador es mayor a 0
                        if(contnuevorut > 0):
                            # guardara el nuevo rut concatenando strings entre el nuevo rut, el - y el codigo verificador
                            nuevorutfinal = str(nuevorutfinal) + "-" + str(codigodigitador)
                            #agregara el rut a la lista
                            listaruts.append(nuevorutfinal)
                        #si no es igual lo guarda simplemente
                        else:
                            nuevorutfinal = str(rutverificar) + "-" + str(codigodigitador)
                            #retornara el nuevo rut
                            listaruts.append(nuevorutfinal)
                    break


#lista email
listaemail = []

#funcion email
def email(pnombre,apellidopaterno,pamaterno):
    # guarda el csv del cliente
    csvcliente = 'clientee.csv'
    # abre el csv y especifica su codificacion de lectura en utf8
    with open(csvcliente, encoding='utf-8') as fa:
        reader = csv.reader(fa)
        # salta a la siguiente fila ignorando los titulos
        next(fa)
        #guarda los nombres y apellidos en las variables
        prnombre = pnombre[:1]
        prmaterno = pamaterno[:1]
        #estructura del email son el dominio
        emailnuevo = prnombre + apellidopaterno + prmaterno
        #estructura con el dominio
        emailfinal = emailnuevo + "@djangocorreo.tk"

        #contador puesto en 0
        contador = 0
        #recorrera el csv
        for row in reader:
            #cuenta y verifica si hay emails repetidos en la lista
            if (listaemail.count(emailfinal) >= 1):
                #se suma + al contador
                contador = contador + 1
                #se le agrega a la estructura sin dominio el valor sumatorio
                emailnuevor = emailnuevo + str(contador)
                #se le agrega al email el dominio
                emailfinal = emailnuevor + "@djangocorreo.tk"
                #se agrega el email a la lista
                listaemail.append(emailfinal)
                #indica que email fue repetido
                #print('EMAIL REPETIDO', emailfinal)
                #detiene el ciclo para no repetir el mismo email
                break
            #verifica si no se repite ningun email
            elif (listaemail.count(emailfinal) == 0):
                #agrega el email directamente a la lista
                listaemail.append(emailfinal)
                #indica que el email no tiene errores
                #print('EMAIL BUENO', emailfinal)
                break


listatelefono = []

#funcion para crear telefono
def telefono():
    caracter = '-'
    for x in range(len(caracter)):
        # guarda el csv del cliente
        csvcliente = 'clientee.csv'
        # abre el csv y especifica su codificacion de lectura en utf8
        with open(csvcliente, encoding='utf-8') as fa:
            reader = csv.reader(fa)
            # salta a la siguiente fila ignorando los titulos
            next(fa)
            # recorre la lista de los ruts
            for row in reader:
                #recorrera la lista de ruts
                for s in listaruts:
                    #guardara el telefono concatenando el rut + el cod de cliente
                    telefono = s[:-2] + f'{row[1]}'
                    #agrega a la lista
                    listatelefono.append(telefono)
                    break

#Crea los ruts
#crea los telefonos
rut()
telefono()

#comienza a crear los emails
caracter = '-'
for x in range(len(caracter)):
    # guarda el csv del cliente
    csvcliente = 'clientee.csv'
    # abre el csv y especifica su codificacion de lectura en utf8
    with open(csvcliente, encoding='utf-8') as fa:
        reader = csv.reader(fa)
        # salta a la siguiente fila ignorando los titulos
        next(fa)
        # recorre la lista de los ruts
        for row in reader:
            email(row[5],row[3],row[4])


caracterfecha = '/'
contador = 0
#guarda el csv del cliente
csvcliente = 'clientee.csv'
#abre el csv y especifica su codificacion de lectura en utf8
with open(csvcliente, encoding='utf-8') as fa:
    reader = csv.reader(fa)
    #salta a la siguiente fila ignorando los titulos
    next(fa)
    for x in range(len(caracterfecha)):
        for row in reader:
            fechaca = f'{row[2]}'
            fechaulti = fechaca[:-4]
            print(fechaulti)
            # borrara el signo "/" de la fecha por un -
            rutverificar = rutverificar.replace(caracterfecha[x], "-")
            print("Rut: {0}\nNumero Cliente: {1}\nFecha Ingreso: {2}\nApellido Paterno: {3}\nApellido Materno: {4}\nNombres: {5}\nCorreo: {6}\nTelefono: {7}\nFecha Nacimiento: {8}\n"
                .format(listaruts[contador], row[1], row[2], row[3], row[4], row[5], listaemail[contador], listatelefono[contador], row[8]))
            #cliente = Cliente(Rut=listaruts[contador], Nombre_Cliente=row[5], Fecha_Registro=row[2],
            #Apellido_Paterno=row[3],
            #Apellido_Materno=row[4], Correo=listaemail[contador], Fecha_Nacimiento=row[8], Telefono=listatelefono[contador])
            #cliente.save()
            contador = contador + 1

clientes_creados = True