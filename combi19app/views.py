from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro, Registro_admin, Registro_vehiculo, Registro_ruta, Registro_ciudad, Registro_viaje, Registro_chofer, Registro_insumo, Registro_info_de_contacto, Registro_comentario, Registro_anuncio, Registro_usuario, Registro_contra, Registro_pasaje, Registro_tarjeta, Registro_ticket
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje, Insumo, InformacionDeContacto, Comentario, Anuncio, Pasaje, Tarjeta, Ticket
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django import db
from datetime import datetime, timedelta, date
import dateutil.parser

db.connections.close_all()
# Create your views here.
@login_required
def home (request):
    if request.user.tipo_usuario == 1:
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        vehiculos = Vehiculo.objects.all()
        viajes = Viaje.objects.filter(estado='activo')
        choferes = Usuario.objects.filter(tipo_usuario=2)
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        return render (request, "home.html", {"ciudades":len(ciudades), "rutas":len(rutas), "choferes":len(choferes), "vehiculos":len(vehiculos), "viajes":len(viajes), "usuarios":len(usuarios), "nombre": request.user.nombre})
    elif request.user.tipo_usuario == 2:
        viajes = Viaje.objects.filter(chofer_id=request.user.id, estado='activo')
        return render(request, "homeChofer.html", {"nombre": request.user.nombre, "viajes": len(viajes)})
    else:
        pasajes = Pasaje.objects.filter(id_user=request.user.id)
        viajes = []
        for p in pasajes:
            if p.estado == "activo":
                viaje = Viaje.objects.get(id=p.nro_viaje_id)
                current_time = datetime.now()
                hora = str((current_time.hour - 3))+":"+str(current_time.minute)+":"+str(current_time.second)
                if viaje.fecha_salida.date() > current_time.date():
                    viajes.append(viaje)
                else:
                    if viaje.fecha_salida.date() == current_time.date():
                        if str(viaje.fecha_salida.time()) > hora:
                            viajes.append(viaje)
        return render (request,"homePasajeros.html", {"nombre": request.user.nombre, "viajes": len(viajes)})

def login(request):

    return render (request, "registration/login.html")

def ver_perfil_admin(request):
    print('ver perfil', request.user.id)
    admin = Usuario.objects.get(id=request.user.id)
    long_c = admin.long_contra
    return render (request, "ver_perfil_admin.html", {'admin': admin, 'longitud': long_c})

def editar_admin(request):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro_admin(instance=admin)
    return render(request, "modificar_admin.html", {"dato": registro, "admin": admin})

def ver_perfil_chofer(request):
    chofer = Usuario.objects.get(id=request.user.id)
    long_c = chofer.long_contra
    return render (request, "ver_perfil_chofer.html", {'chofer': chofer, 'longitud': long_c})

def editar_chofer2(request):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(instance=chofer)
    return render(request, "modificar_chofer2.html", {"dato": registro, "chofer": chofer})

def ver_perfil_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    long_c = usuario.long_contra
    return render (request, "ver_perfil_usuario.html", {'usuario': usuario, 'longitud': long_c})

def editar_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro_usuario(instance=usuario)
    return render(request, "modificar_usuario.html", {"dato": registro, "usuario": usuario})

#busca los campos incorrectos (repetidos) que llevan el valor None
def errores(registro):
    lista = []

    if registro.cleaned_data.get('dni') == None:
        lista+=[1]
    # user= Usuario.objects.all().__str__()
    # base_de_datos=user.replace('<QuerySet [', '').replace('1>,', '1').replace('2>,', '2').replace('3>,', '3').replace('<Usuario: ', '').replace('>', '').replace(']', '').split(' ')
    # lista_de_usuarios=[]
    #
    # for i in range(0,len(base_de_datos),4):
    #     lista_de_usuarios.append(base_de_datos[i:i+4])
    #
    # lista_de_usuarios.pop(len(lista_de_usuarios) -1)
    return set(lista)

def actualizar_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro_admin(request.POST, instance=admin)
    if registro.is_valid():
        print('entro')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neee')
    response = redirect('/ver_perfil_admin/')
    return response

def actualizar_chofer2(request, id_chofer):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(request.POST, instance=chofer)
    if registro.is_valid():
        print('entro')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neee')
    response = redirect('/ver_perfil_chofer/')
    return response

def actualizar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro_usuario(request.POST, instance=usuario)
    if registro.is_valid():
        print('hola')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neeee')
    response = redirect('/ver_perfil_usuario/')
    return response

def confirmar_usuario(registro):
    lista = []
    usuarios = Usuario.objects.all()
    for us in usuarios:
        dni = us.dni
        if registro == str(dni):
            lista+=[1]
            break

    return set(lista)

def cambiar_contra(request):
    registro = Registro()
    return render(request, "verificar_dni.html", {'usuario': registro})

def procesar_contra(request):
    if request.POST.get('dni') != None:
        confirmacion = confirmar_usuario(request.POST.get('dni'))
        if len(confirmacion) != 0:
            usuario = Usuario.objects.get(dni=request.POST.get('dni'))
            registro = Registro(request.POST, instance=usuario)
            return render(request, "cambiar_contra.html", {'usuario': usuario})
        else:
            return render(request, "verificar_dni.html", {'mensaje': "no existe"})
    else:
        cambiar_contra(request)
        return render(request, "verificar_dni.html", {'dni': request.POST.get('dni')})

def actualizar_contra(request):
    confirmacion = confirmar_usuario(request.POST.get('dni'))
    if len(confirmacion) != 0:
        usuario = Usuario.objects.get(dni=request.POST.get('dni'))
        registro = Registro(request.POST, instance=usuario)
        if registro.is_valid():
            if registro.cleaned_data.get('tipo_usuario') == 1:
                registro.save_admin()
            elif registro.cleaned_data.get('tipo_usuario') == 2:
                registro.save_chofer()
            else:
                registro.save()

        response = redirect('/accounts/login/')
        return response
        #return render(request, "cambiar_contra.html", {'usuario': usuario, 'mensaje': "existe"})


def cambiar_contra_admin(request):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=admin)
    return render(request, "cambiar_contra_admin.html", {"dato": registro, "admin": admin})

def actualizar_contra_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=admin)
    if registro.is_valid():
        registro.save_admin()

    response = redirect('/accounts/login/')
    return response

def cambiar_contra_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=usuario)
    return render(request, "cambiar_contra_usuario.html", {"dato": registro, "usuario": usuario})

def actualizar_contra_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=usuario)

    if registro.is_valid():
        registro.save()

    response = redirect('/accounts/login/')
    return response

def cambiar_contra_chofer(request):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=chofer)
    return render(request, "cambiar_contra_chofer.html", {"dato": registro, "chofer": chofer})

def actualizar_contra_chofer(request, id_chofer):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=chofer)
    if registro.is_valid():
        registro.save_chofer()
    response = redirect('/accounts/login/')
    return response

def errores_ruta(ruta):
    lista = []

    rutas = Ruta.objects.all()
    for r in rutas:
        if ruta.cleaned_data.get('nombre').upper() == r.nombre:
            lista+=[1]
            break

    if ruta.cleaned_data.get('origen') == ruta.cleaned_data.get('destino'):
        lista+=[2]

    return set(lista)

def errores_ruta2(ruta, r_vieja):
    lista = []

    rutas = Ruta.objects.all()
    print('ruta', ruta.cleaned_data.get('nombre'), 'otra', r_vieja.nombre )
    if ruta.cleaned_data.get('nombre').upper() != r_vieja.nombre:
        for r in rutas:
            if ruta.cleaned_data.get('nombre').upper() == r.nombre:
                lista+=[1]
                break

    if ruta.cleaned_data.get('origen') == ruta.cleaned_data.get('destino'):
        lista+=[2]

    return set(lista)

def errores_ciudad(ciudad):
    lista = []
    ciudades = Ciudad.objects.all()
    for c in ciudades:
        if ciudad.cleaned_data.get('codigo_postal') == c.codigo_postal:
            lista+=[1]
            break
        if (ciudad.cleaned_data.get('nombre').upper() == c.nombre) and ciudad.cleaned_data.get('provincia') == c.provincia:
            lista+=[2]
            break

    return set(lista)

def errores_ciudad2(ciudad, c_vieja):
    lista = []
    ciudades = Ciudad.objects.all()
    if ciudad.cleaned_data.get('codigo_postal') != c_vieja.codigo_postal:
        for c in ciudades:
            if ciudad.cleaned_data.get('codigo_postal') == c.codigo_postal:
                lista+=[1]
                break
            else:
                if c_vieja.nombre != ciudad.cleaned_data.get('nombre').upper() or c_vieja.provincia != ciudad.cleaned_data.get('provincia'):
                    if ciudad.cleaned_data.get('nombre').upper() == c.nombre and ciudad.cleaned_data.get('provincia') == c.provincia:
                        lista+=[2]
                        break

    else:
        for c in ciudades:
            print('entro al else')
            if (ciudad.cleaned_data.get('nombre').upper() == c.nombre) and (ciudad.cleaned_data.get('provincia') == c.provincia):
                print('if')
                lista+=[2]
                break


    return set(lista)

def errores_viaje(viaje,id_viaje):
    lista=[]
    if viaje.cleaned_data.get('precio') == None:
        lista+=[5]
    viajes = Viaje.objects.filter(vehiculo_id = viaje.cleaned_data.get('vehiculo').id, estado='activo')
    for v in viajes:
        if(id_viaje == 0 or id_viaje != v.id):
            #date = dateutil.parser.parse
            diaDespues = v.fecha_salida.date()+timedelta(days=+1)
            fechaDelViaje = viaje.cleaned_data.get('fecha_salida').date()
            fechaDelViajeDT = viaje.cleaned_data.get('fecha_salida')
            if v.fecha_salida.date() == viaje.cleaned_data.get('fecha_salida').date():
                lista+=[1]
                break
            elif v.fecha_llegada.date().strftime("%Y-%m-%d") == fechaDelViaje.strftime("%Y-%m-%d"):
                hora = viaje.cleaned_data.get('hora_salida').split(':')
                if hora[2] == "AM":
                    fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]), minute=int(hora[1]))
                else:
                    if int(hora[0]) == 12 :
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = 0, minute=int(hora[1]))
                    else:
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]) + 12, minute=int(hora[1]))
                if (v.fecha_llegada.hour >= fechaDelViajeDT.hour):
                    lista+=[2]

                    break

    viajes2 = Viaje.objects.filter(chofer_id = viaje.cleaned_data.get('chofer').id, estado='activo')
    for v in viajes2:
        #date = dateutil.parser.parse
        if(id_viaje == 0 or id_viaje != v.id):
            diaDespues = v.fecha_salida.date()+timedelta(days=+1)
            fechaDelViaje = viaje.cleaned_data.get('fecha_salida').date()
            fechaDelViajeDT = viaje.cleaned_data.get('fecha_salida')
            if v.fecha_salida.date() == viaje.cleaned_data.get('fecha_salida').date():
                lista+=[3]
                break

            elif v.fecha_llegada.date().strftime("%Y-%m-%d") == fechaDelViaje.strftime("%Y-%m-%d"): #Si fecha de llegada = fecha del viaje
                hora = viaje.cleaned_data.get('hora_salida').split(':')
                if hora[2] == "AM":
                    fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]), minute=int(hora[1]))
                else:
                    if int(hora[0]) == 12 :
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = 0, minute=int(hora[1]))
                    else:
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]) + 12, minute=int(hora[1]))
                if (v.fecha_llegada.hour >= fechaDelViajeDT.hour):
                    lista+=[4]
                    break
                if (v.fecha_llegada.hour <= fechaDelViajeDT.hour):
                    if fechaDelViajeDT.hour in range(v.fecha_llegada.hour, (v.fecha_llegada.hour+8)):
                        lista+=[6]
                        break

    return set(lista)

def errores_vehiculo(vehiculo):
    lista = []
    vehiculos = Vehiculo.objects.all()
    for v in vehiculos:
        if vehiculo.cleaned_data.get('patente').upper() == v.patente:
            lista+=[1]
            break
    return set(lista)

def errores_tarjeta(tarjeta):
    lista = []
    vencido = tarjeta.cleaned_data.get('vencimiento').split('/')
    if int(vencido[1]) < 21:
        lista+=[1]
    else:
        if int(vencido[1]) == 21:
            if int(vencido[0]) <= 6:
                lista+=[1]

    if len(tarjeta.cleaned_data.get('numero')) < 16:
        lista+=[3]

    return set(lista)

def errores_ven(tarjeta):
    lista = []
    vencido = int(str(tarjeta).replace('Tarjeta object ','').replace('(','').replace(')',''))
    vencido = Tarjeta.objects.get(id=vencido)
    vencido = vencido.vencimiento.split('/')
    if int(vencido[1]) < 21:
        lista+=[1]
    else:
        if int(vencido[1]) == 21:
            if int(vencido[0]) <= 6:
                lista+=[2]
    return set(lista)

def errores_tareta2(tarjetas):
    for i in tarjetas:
        confirmacion=errores_ven(i)
        if len(confirmacion) != 0:
            i.delete()
    return tarjetas

def calcular_minutos():
    minutos=[]
    for i in range(0,60):
        minutos+=[i]
    return minutos

def verificar_eliminacion_ciudad(ciudad):
    lista = []
    lista2= []
    lista2+=[str(ciudad)]
    string = lista2[0]
    string = string.replace('<bound method QuerySet.first of <QuerySet [<Ciudad: ', '').replace('>]>>','').strip()
    verificacion1 = str(Ruta.objects.filter(codigo_origen=int(string)).first)
    verificacion2 = str(Ruta.objects.filter(codigo_destino=int(string)).first)
    print('verificacion antes',verificacion1)
    print('verificacion 2 antes', verificacion2)
    verificacion1 = verificacion1.replace('<bound method QuerySet.first of <QuerySet ','').replace('[','').replace(']>>','')
    verificacion2 = verificacion2.replace('<bound method QuerySet.first of <QuerySet ','').replace('[','').replace(']>>','')
    print('verificacion',verificacion1)
    print('verificacion2',verificacion2)
    if len(verificacion1) != 0 or len(verificacion2) != 0:
        lista+=[1]
    return set(lista)

class FormularioRegistro (HttpRequest):

    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrarse.html", {"dato":registro})

    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            print(registro.cleaned_data.get('dni'))
            registro.save()
            registro = Registro()
            return render(request, "registrarse.html", {"dato": registro, "mensaje": "ok"})
        else:
            print(registro.cleaned_data.get('dni'))
            confirmacion=errores(registro)
            registro = Registro()
            return render(request, "registrarse.html", {"mensaje": "not_ok", "errores": confirmacion})

class FormularioRegistroChofer (HttpRequest):
    @login_required
    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrar_chofer.html", {"dato":registro})
    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save_chofer()
                registro = Registro()
                return render(request, "registrar_chofer.html", {"dato": registro, "mensaje": "ok"})
        confirmacion=errores(registro)
        registro = Registro()
        return render(request, "registrar_chofer.html", {"mensaje": "not_ok", "errores": confirmacion})
    @login_required
    def editar_chofer(request, id_chofer):
        chofer = Usuario.objects.get(id=id_chofer)
        registro = Registro_chofer(instance=chofer)
        return render(request, "modificar_chofer.html", {"dato": registro, "choferes": chofer})
    @login_required
    def actualizar_chofer(request, id_chofer):
        chofer = Usuario.objects.get(id=id_chofer)
        registro = Registro_chofer(request.POST, instance=chofer)
        if registro.is_valid():
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save()
        response = redirect('/listar_choferes/')
        return response
        #choferes = Usuario.objects.filter(tipo_usuario=2)
        #return render (request, "listar_choferes.html", {"choferes": choferes, "mensaje": "editado", "cantidad": len(choferes)})


class FormularioRegistroAdmin (HttpRequest):
    @login_required
    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrar_admin.html", {"dato":registro})
    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save_admin()
                registro = Registro()
                return render(request, "registrar_admin.html", {"dato": registro, "mensaje": "ok"})
        confirmacion=errores(registro)
        registro = Registro()
        return render(request, "registrar_admin.html", {"mensaje": "not_ok", "errores": confirmacion})

def errores_vehiculo2(vehiculo, v_viejo):
    lista = []
    vehiculos = Vehiculo.objects.all()
    if vehiculo.cleaned_data.get('patente').upper() != v_viejo.patente:
        for v in vehiculos:
            if vehiculo.cleaned_data.get('patente').upper() == v.patente:
                lista+=[1]
                break
    return set(lista)

class FormularioVehiculo (HttpRequest):
    @login_required
    def crear_formulario(request):
        vehiculo = Registro_vehiculo()
        return render (request, "agregar_vehiculo.html", {"dato": vehiculo})
    @login_required
    def procesar_formulario(request):
        vehiculo = Registro_vehiculo(request.POST)
        if vehiculo.is_valid():
            confirmacion = errores_vehiculo(vehiculo)
            if len(confirmacion) == 0:
                vehiculo.save_vehiculo()
                vehiculo = Registro_vehiculo()
                return render (request, "agregar_vehiculo.html", {"dato": vehiculo, "mensaje": "ok"})
            else:
                vehiculo = Registro_vehiculo()
                return render (request, "agregar_vehiculo.html", {"mensaje": "not_ok"})
        else:
            vehiculo = Registro_vehiculo()
            return render (request, "agregar_vehiculo.html", {"mensaje": "vacio"})

    @login_required
    def editar(request, id_vehiculo):
        vehiculo = Vehiculo.objects.get(id=id_vehiculo)
        form = Registro_vehiculo(instance=vehiculo)
        return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo})

    @login_required
    def actualizar(request, id_vehiculo):
        vehiculo = Vehiculo.objects.get(id=id_vehiculo)
        vehiculo2 = Vehiculo.objects.get(id=id_vehiculo)
        form = Registro_vehiculo(request.POST, instance = vehiculo)
        if form.is_valid():
        #    db.connections.close_all()
            confirmacion = errores_vehiculo2(form, vehiculo2)
            if len(confirmacion) == 0:
                form.save()
            else:
                return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo, "mensaje": "not_ok"})
            response = redirect('/listar_vehiculos/')
            return response
        #    vehiculos= Vehiculo.objects.all()
        #    return render (request, "listar_vehiculos.html", {"form":form,"vehiculos":vehiculos, "vehiculo":vehiculo, "mensaje": "editado"})

class ListarVehiculos(HttpRequest):
    @login_required
    def crear_listado(request):
        vehiculos = Vehiculo.objects.all()
        contexto = {'vehiculos': vehiculos, 'cantidad':len(vehiculos)}
        return render (request, "listar_vehiculos.html", contexto)
    @login_required
    def mostrar_detalle(request, id_vehiculo):
        detalle= Vehiculo.objects.get(pk=id_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_vehiculo(request, id_vehiculo):
        detalle= Vehiculo.objects.get(pk=id_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalleViajeVehiculo"})

class EliminarVehiculo(HttpRequest):
    @login_required
    def eliminar_vehiculo(request, id_vehiculo):
        vehiculo_eliminado = Vehiculo.objects.get(pk=id_vehiculo)
        try:
            vehiculo_eliminado.delete()
            vehiculo = Vehiculo.objects.all()
            return render (request, "listar_vehiculos.html", {"vehiculos": vehiculo, "mensaje":"eliminado", "cantidad": len(vehiculo)})
        except:
            vehiculo = Vehiculo.objects.all()
            return render (request, "listar_vehiculos.html", {"vehiculos": vehiculo, "mensaje":"no_puede", "cantidad": len(vehiculo)})

class FormularioRuta (HttpRequest):
    @login_required
    def crear_formulario(request):
        ruta = Registro_ruta()
        ciudad = Ciudad.objects.all()
        return render (request, "agregar_ruta.html", {"dato": ruta, "ciudades": ciudad})

    @csrf_exempt
    def procesar_formulario(request):
        ruta = Registro_ruta(request.POST)
        ciudad = Ciudad.objects.all()
        if ruta.is_valid():
            confirmacion=errores_ruta(ruta)
            if len(confirmacion) == 0:
                ruta.save_ruta(ciudad)
                ruta = Registro_ruta()
                return render (request, "agregar_ruta.html", {"dato": ruta, "mensaje": "ok", "ciudades": ciudad})

        confirmacion=errores_ruta(ruta)
        ruta = Registro_ruta()
        return render (request, "agregar_ruta.html", {"mensaje": "not_ok", "errores":confirmacion, "ciudades": ciudad})

    @login_required
    def editar_ruta(request, id_ruta):
        ruta = Ruta.objects.get(id=id_ruta)
        registro = Registro_ruta(instance=ruta)
        ciudad = Ciudad.objects.all()
        return render(request, "modificar_ruta.html", {"dato": registro, "rutas": ruta, "ciudades": ciudad})
    @login_required
    def actualizar_ruta(request, id_ruta):
        ruta = Ruta.objects.get(id=id_ruta)
        ruta2 = Ruta.objects.get(id=id_ruta)
        ciudad = Ciudad.objects.all()
        registro = Registro_ruta(request.POST, instance=ruta)
        if registro.is_valid():
            confirmacion = errores_ruta2(registro, ruta2)
            if len(confirmacion) == 0 :
                registro.save_ruta(ciudad)
                response = redirect('/listar_rutas/')
                return response
            else:
                ciudad = Ciudad.objects.all()
                return render (request, "modificar_ruta.html", {"rutas":ruta,"ciudades":ciudad, "mensaje": "not_ok", "errores":confirmacion})
        #rutas = Ruta.objects.all()
        #return render (request, "listar_rutas.html", {"rutas": rutas, "mensaje": "editado"})

class FormularioCiudad (HttpRequest):
    @login_required
    def crear_formulario(request):
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"dato": ciudad})
    @login_required
    def procesar_formulario(request):
        ciudad = Registro_ciudad(request.POST)
        if ciudad.is_valid():
            confirmacion=errores_ciudad(ciudad)
            if len(confirmacion) == 0:
                ciudad.save_ciudad()
                ciudad = Registro_ciudad()
                return render (request, "agregar_ciudad.html", {"dato": ciudad, "mensaje": "ok"})
        confirmacion=errores_ciudad(ciudad)
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"mensaje": "not_ok", "errores":confirmacion})
    @login_required
    def editar(request, id_ciudad):
        ciudad = Ciudad.objects.get(id=id_ciudad)
        form = Registro_ciudad(instance=ciudad)
        return render (request, "modificar_ciudad.html", {"form":form, "ciudad":ciudad})
    @login_required
    def actualizar(request, id_ciudad):
        ciudad = Ciudad.objects.get(id=id_ciudad)
        ciudad2 = Ciudad.objects.get(id=id_ciudad)
        form = Registro_ciudad(request.POST, instance = ciudad)
        if form.is_valid():
            ok = errores_ciudad2(form, ciudad2)
            if len(ok) == 0:
                form.save_ciudad()
            else:
                ciudad =Ciudad.objects.get(id=id_ciudad)
                return render (request, "modificar_ciudad.html", {"ciudad": ciudad, "errores": ok, "mensaje": "not_ok"})
        response = redirect('/listar_ciudades/')
        return response
            #ciudades= Ciudad.objects.all()
            #return render (request, "listar_ciudades.html", {"form":form, "ciudad":ciudad, "mensaje": "ok", "ciudades":ciudades, "mensaje": "editado"})

class ListarCiudad (HttpRequest):
    @login_required
    def crear_listado(request):
        ciudad = Ciudad.objects.all()
        print(ciudad)
        contexto = {'ciudades': ciudad, 'cantidad':len(ciudad)}
        return render (request, "listar_ciudades.html", contexto)
    @login_required
    def mostrar_detalle(request, id_ciudad):
        detalle= Ciudad.objects.get(pk=id_ciudad)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ciudad(request, id_ciudad):
        detalle= Ciudad.objects.get(pk=id_ciudad)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalleViajeCiudad"})

class EliminarCiudad (HttpRequest):
    @login_required
    def eliminar_ciudad(request, id_ciudad):
        ciudad = Ciudad.objects.filter(pk=id_ciudad).first
        ciudad_eliminada = Ciudad.objects.get(pk=id_ciudad)
        confirmacion = verificar_eliminacion_ciudad(ciudad)
        ciudades = Ciudad.objects.all()
        if len(confirmacion) == 0:
            try:
                ciudad_eliminada.delete()
                return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"eliminado", "cantidad": len(ciudades)})
            except:
                return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"no_puede", "cantidad": len(ciudades)})
        else:
            return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"no_puede2", "cantidad": len(ciudades)})

class BuscarCiudad(HttpRequest):
    @login_required
    def listar_ciudades(request):
        ciudades = Ciudad.objects.all()
        return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades})

    @login_required
    def listar_ciudades_result(request):
        if request.GET.get('origen')==request.GET.get('destino'):
            ciudades = Ciudad.objects.all()
            return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades, "errores": 1})

        ruta = Ruta.objects.filter(origen=request.GET.get('origen'), destino=request.GET.get('destino'))
        #print(ruta[1].id)
        viajes = []
        for r in ruta:
            #viajes += Viaje.objects.filter(ruta_id=r.id).filter(fecha_salida=date.date())
            if(request.GET.get('fecha_salida') != ""):
                date = dateutil.parser.parse(request.GET.get('fecha_salida'))
                print(request.GET.get('fecha_salida'))
                print(date.day)
                print(date.month)
                if(date.day>12):
                    viajes += Viaje.objects.filter(ruta_id=r.id ,fecha_salida__year=date.year,fecha_salida__day=date.day, fecha_salida__month=date.month, estado='activo')
                else:
                    viajes += Viaje.objects.filter(ruta_id=r.id ,fecha_salida__year=date.year,fecha_salida__day=date.month, fecha_salida__month=date.day, estado='activo')
            else:
                viaje = Viaje.objects.filter(ruta_id=r.id)
                hoy = datetime.now()
                for v in viaje:
                    if v.fecha_salida.date() >= hoy.date():
                        viajes.append(v)
                #viajes += Viaje.objects.filter(ruta_id=r.id)
        return render (request, "buscar_viaje_result.html",{"viajes": viajes, "rutas":ruta})


class ListarRuta (HttpRequest):
    @login_required
    def crear_listado(request):
        ruta = Ruta.objects.all()
        contexto = {'rutas': ruta, 'cantidad':len(ruta)}
        return render (request, "listar_rutas.html", contexto)
    @login_required
    def mostrar_detalle(request, id_ruta):
        detalle= Ruta.objects.get(pk=id_ruta)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ruta(request, id_ruta):
        detalle= Ruta.objects.get(pk=id_ruta)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalleViajeRuta"})
    @login_required
    def eliminar_ruta(request, id_ruta):
        ruta_eliminada = Ruta.objects.get(pk=id_ruta)
        try:
            ruta_eliminada.delete()
            ruta = Ruta.objects.all()
            return render (request, "listar_rutas.html", {"rutas": ruta, "mensaje":"eliminado", "cantidad": len(ruta)})
        except:
            ruta = Ruta.objects.all()
            return render (request, "listar_rutas.html", {"rutas": ruta, "mensaje":"no_puede", "cantidad": len(ruta)})


def errores_viajes(viaje, dato):

    if viaje.cleaned_data.get('fecha_salida') == None:
        viaje.fecha_salida = dato.fecha_salida
        print('viaje salida', viaje.fecha_salida)
    if viaje.cleaned_data.get('fecha_llegada') == None:
        viaje.fecha_llegada = dato.fecha_llegada

    return viaje

def eliminar_pasajes(pasaje, ticket):

    for p in pasaje:
        for t in ticket:
            if p.id_user == t.id_user:
                t.delete()
        p.delete()

class FormularioViaje (HttpRequest):
    @login_required
    def crear_formulario(request):
        viaje = Registro_viaje()
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        return render (request, "agregar_viaje.html", {"dato": viaje, "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})

    @login_required
    def procesar_formulario(request):
        viaje = Registro_viaje(request.POST)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        if viaje.is_valid():
            confirmacion = errores_viaje(viaje,0)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=viaje.cleaned_data.get('vehiculo'))
                r = Ruta.objects.get(nombre=viaje.cleaned_data.get('ruta'))
                viaje.save_viaje(v,r)
                viaje = Registro_viaje()
                return render (request, "agregar_viaje.html", {"dato": viaje, "mensaje":"ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        confirmacion=errores_viaje(viaje,0)
        viaje = Registro_viaje()
        return render (request, "agregar_viaje.html", {"errores":confirmacion, "mensaje": "not_ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
    @login_required
    def editar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        registro = Registro_viaje(instance=viaje)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        rutas = Ruta.objects.all()
        ciudades = Ciudad.objects.all()
        return render(request, "modificar_viaje.html", {"dato": registro, "viajes": viaje, "rutas": rutas, "ciudades": ciudades, "minutos": minutos, "vehiculos": vehiculos, "choferes": choferes})

    @csrf_exempt
    def actualizar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        registro1 = Registro_viaje(instance=viaje)
        registro = Registro_viaje(request.POST, instance=viaje)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        if registro.is_valid():
            print("ok")
            confirmacion = errores_viaje(registro,id_viaje)
            confirmacion = list(confirmacion)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=registro.cleaned_data.get('vehiculo'))
                r = Ruta.objects.get(nombre=registro.cleaned_data.get('ruta'))
                registro.save_viaje(v,r)
            else:
                viajes = Viaje.objects.all()
                return render (request, "modificar_viaje.html", {"viajes": viaje, "errores":confirmacion[0], "mensaje": "not_ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        else:
            print(registro.cleaned_data.get('precio'))
            print(registro.cleaned_data.get('vehiculo'))
            dato = errores_viajes(registro, viaje)
            if dato.is_valid():
                dato.save_viaje2(dato)
        #viajes = Viaje.objects.all()
        #return render (request, "listar_viajes.html", {"viajes": viajes, "mensaje": "editado", "cantidad": len(viajes)})
        response = redirect('/listar_viajes/')
        return response

    def eliminar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        pasaje = Pasaje.objects.filter(nro_viaje_id= id_viaje, estado='cancelado')
        ticket = Ticket.objects.filter(viaje_id= id_viaje)
        try:
            viaje.delete()
            viaje = Viaje.objects.all()
            rutas = []
            for v in viaje:
                r = Ruta.objects.get(id = v.ruta_id)
                if r not in rutas:
                    rutas.append(r)
            return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"eliminado", "cantidad": len(viaje)})
        except:
            pasaje_activo = Pasaje.objects.filter(nro_viaje_id= id_viaje, estado='activo')
            print('activo', pasaje_activo)
            if len(pasaje_activo) == 0:
                eliminar = eliminar_pasajes(pasaje, ticket)
                viaje.delete()
                viaje = Viaje.objects.all()
                rutas = []
                for v in viaje:
                    r = Ruta.objects.get(id = v.ruta_id)
                    if r not in rutas:
                        rutas.append(r)
                return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"eliminado", "cantidad": len(viaje)})
            else:
                viaje = Viaje.objects.all()
                rutas = []
                for v in viaje:
                    r = Ruta.objects.get(id = v.ruta_id)
                    if r not in rutas:
                        rutas.append(r)
                return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"no_puede", "cantidad": len(viaje)})

class ListarViajes(HttpRequest):
    @login_required
    def crear_listado(request):
        viaje = Viaje.objects.all()
        viajes = []
        rutas = []
        for v in viaje:
            if v.estado == 'activo':
                hoy = datetime.today()
                if v.fecha_salida.date() >= hoy.date():
                    viajes.append(v)
                else:
                    if v.fecha_salida.date() < hoy.date():
                        v.estado = 'realizado'
                        v.save()
            r = Ruta.objects.get(id = v.ruta_id)
            if r not in rutas:
                rutas.append(r)
        contexto = {'viajes': viajes, 'cantidad':len(viajes), 'rutas':rutas}
        return render (request, "listar_viajes.html", contexto)

    @login_required
    def mostrar_detalle(request, id_viaje):
        detalle= Viaje.objects.get(id=id_viaje)
        ruta= Ruta.objects.get(id=detalle.ruta_id)
        return render (request, "listar_viajes.html", {"dato":detalle,"ruta":ruta, "mensaje":"detalle"})

    @login_required
    def listar_viajes_por_realizar(request):
        pasajes = Pasaje.objects.filter(id_user=request.user.id)
        viajes = []
        rutas = []
        for p in pasajes:
            if p.estado == 'activo':
                viaje = Viaje.objects.get(id=p.nro_viaje_id)
                ruta = Ruta.objects.get(id=viaje.ruta_id)
                if ruta not in rutas:
                    rutas.append(ruta)
                current_time = datetime.today()
                hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
                if(viaje.fecha_salida.date() > current_time.date()):
                    viajes.append(viaje)
                else:
                    if(viaje.fecha_salida.date() == current_time.date()):
                        if(str(viaje.fecha_salida.time()) > hora):
                            viajes.append(viaje)
        contexto ={'viajes': viajes, 'rutas': rutas}
        return render (request, "ver_viajes_por_realizar.html", contexto)

    @login_required
    def listar_viajes_realizados(request):
        pasajes = Pasaje.objects.filter(id_user=request.user.id)
        viajes = []
        rutas = []
        for p in pasajes:
            if p.estado == 'activo':
                viaje = Viaje.objects.get(id=p.nro_viaje_id)
                ruta = Ruta.objects.get(id=viaje.ruta_id)
                if ruta not in rutas:
                    rutas.append(ruta)
                current_time = datetime.today()
                hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
                if(viaje.fecha_salida.date() < current_time.date()):
                    viajes.append(viaje)
                else:
                    if(viaje.fecha_salida.date() == current_time.date()):
                        if(str(viaje.fecha_salida.time()) < hora):
                            viajes.append(viaje)
        contexto ={'viajes': viajes, 'rutas': rutas}
        return render (request, "ver_viajes_realizados.html", contexto)

    @login_required
    def listar_proximos_viajes(request):
        viajes = Viaje.objects.filter(chofer_id=request.user.id)
        viajes_por_hacer = []
        rutas = []
        for v in viajes:
            if v.estado == 'activo':
                viaje = Viaje.objects.get(id=v.id)
                ruta = Ruta.objects.get(id=viaje.ruta_id)
                if ruta not in rutas:
                    rutas.append(ruta)
                current_time = datetime.today()
                hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
                if(viaje.fecha_salida.date() > current_time.date()):
                    viajes_por_hacer.append(viaje)
                else:
                    if(viaje.fecha_salida.date() == current_time.date()):
                        if(str(viaje.fecha_salida.time()) > hora):
                            viajes_por_hacer.append(viaje)
        contexto ={'viajes': viajes_por_hacer, 'rutas': rutas, 'cantidad': len(viajes_por_hacer)}
        return render (request, "listar_proximos_viajes.html", contexto)

    @login_required
    def mostrar_detalle_chofer(request, id_viaje):
        detalle= Viaje.objects.get(id=id_viaje)
        ruta= Ruta.objects.get(id=detalle.ruta_id)
        return render (request, "listar_proximos_viajes.html", {"dato":detalle,"ruta":ruta, "mensaje":"detalle"})

    @login_required
    def cancelar_viaje_chofer(request, id_viaje):
        viajes = Viaje.objects.filter(chofer_id=request.user.id)
        if len(viajes) != 0:
            hoy = datetime.today()
            viaje = Viaje.objects.get(id=id_viaje, chofer_id=request.user.id)
        viaje.estado = 'cancelado'
        viaje.save()
        return ListarViajes.listar_proximos_viajes(request)

class ListarChofer(HttpRequest):

    @csrf_exempt
    def crear_listado(request):
        chofer = Usuario.objects.filter(tipo_usuario=2)
        contexto = {'choferes': chofer, 'cantidad': len(chofer)}
        return render (request, "listar_choferes.html", contexto)
    @login_required
    def mostrar_detalle(request, id_chofer):
        detalle = Usuario.objects.get(pk=id_chofer)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_chofer(request, id_chofer):
        detalle = Usuario.objects.get(pk=id_chofer)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalleViajeChofer"})
    @login_required
    def eliminar_chofer(request, id_chofer):
        chofer_eliminado = Usuario.objects.get(pk=id_chofer)
        try:
            chofer_eliminado.delete()
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"eliminado", "cantidad": len(chofer)})
        except:
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"no_puede", "cantidad": len(chofer)})

class ListarAdministradores(HttpRequest):
    @login_required
    def crear_listado(request):
        admin = Usuario.objects.filter(tipo_usuario=1)
        contexto = {'admin': admin, 'cantidad':len(admin)}
        return render (request, "listar_admin.html", contexto)
    @login_required
    def mostrar_detalle(request, id_admin):
        detalle= Usuario.objects.get(pk=id_admin)
        return render (request, "listar_admin.html", {"dato":detalle, "mensaje":"detalle"})

    @login_required
    def eliminar_admin(request, id_admin):
        admins = Usuario.objects.filter(tipo_usuario=1)
        admin_eliminado = Usuario.objects.get(pk=id_admin)
        try:
            if id_admin != request.user.id:
                if len(admins) > 1:
                    admin_eliminado.delete()
                    admin = Usuario.objects.filter(tipo_usuario=1)
                    return render (request, "listar_admin.html", {"admin": admin, "mensaje":"eliminado", "cantidad": len(admin)})
            else:
                admin = Usuario.objects.filter(tipo_usuario=1)
                return render (request, "listar_admin.html", {"admin": admin, "mensaje":"no_puede", "cantidad": len(admin)})
        except:
            admin = Usuario.objects.filter(tipo_usuario=1)
            return render (request, "listar_admin.html", {"admin": admin, "mensaje":"no_puede", "cantidad": len(admin)})

class ListarPasajeros(HttpRequest):
    @login_required
    def crear_listado(request):
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        contexto = {'usuarios': usuarios, 'cantidad':len(usuarios)}
        return render (request, "listar_pasajeros.html", contexto)

    # @login_required
    # def crear_listado_chofer(request):
    #     usuarios = Usuario.objects.filter(tipo_usuario=3)
    #     contexto = {'usuarios': usuarios, 'cantidad':len(usuarios)}
    #     return render (request, "listar_pasajeros_chofer.html", contexto)


def errores_insumo(insumo):
    lista= []
    insumos = Insumo.objects.all()

    for i in insumos:
        if insumo.cleaned_data.get('nombre').upper() == i.nombre:
            lista+=[1]
            break
        if insumo.cleaned_data.get('precio') == None:
            lista+=[2]
    return set(lista)

def errores_insumo2(insumo, i_vieja):
    lista = []
    insumos = Insumo.objects.all()
    if insumo.cleaned_data.get('nombre').upper() != i_vieja.nombre:
        for i in insumos:
            if insumo.cleaned_data.get('nombre').upper() == i.nombre:
                lista+=[1]
                break

    if insumo.cleaned_data.get('precio') == None:
        lista+=[2]
    return set(lista)

class FormularioInsumo(HttpRequest):
    @login_required
    def crear_formulario(request):
        insumo = Registro_insumo()
        return render (request, "agregar_insumo.html", {"dato": insumo})

    @login_required
    def procesar_formulario(request):
        insumo = Registro_insumo(request.POST)
        if insumo.is_valid():
            confirmacion = errores_insumo(insumo)
            if len(confirmacion) == 0:
                insumo.save_insumo()
                insumo = Registro_insumo()
                return render (request, "agregar_insumo.html", {"dato": insumo, "mensaje":"ok"})

        confirmacion=errores_insumo(insumo)
        insumo = Registro_insumo()
        return render (request, "agregar_insumo.html", {"errores":confirmacion, "mensaje": "not_ok"})

    @login_required
    def editar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        registro = Registro_insumo(instance=insumo)
        return render(request, "modificar_insumo.html", {"dato": registro, "insumos": insumo})

    @csrf_exempt
    def actualizar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        insumo2 = Insumo.objects.get(id=id_insumo)
        registro = Registro_insumo(request.POST, instance=insumo)
        if registro.is_valid():
            confirmacion = errores_insumo2(registro, insumo2)
            if len(confirmacion) == 0:
                registro.save_insumo()
                insumos = Insumo.objects.all()
                contexto = {'insumos': insumos, 'cantidad':len(insumos)}
                return render (request, "listar_insumos.html", contexto)
            else:
                insumo = Insumo.objects.get(id=id_insumo)
                return render (request, "modificar_insumo.html", {"insumos": insumo, "errores": confirmacion, "mensaje": "not_ok"})
        else:
            confirmacion = errores_insumo2(registro, insumo2)
            return render (request, "modificar_insumo.html", {"errores":confirmacion, "mensaje": "not_ok", "insumos":insumo})

        response = redirect('/listar_insumos/')
        return response


class ListarInsumos(HttpRequest):
    @login_required
    def crear_listado(request):
        insumo = Insumo.objects.all()
        contexto = {'insumos': insumo, 'cantidad':len(insumo)}
        return render (request, "listar_insumos.html", contexto)

    @login_required
    def mostrar_detalle(request, id_insumo):
        detalle= Insumo.objects.get(pk=id_insumo)
        return render (request, "listar_insumos.html", {"dato":detalle, "mensaje":"detalle"})

    @login_required
    def eliminar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        try:
            insumo.delete()
            insumo = Insumo.objects.all()
            return render (request, "listar_insumos.html", {"insumos": insumo, "mensaje":"eliminado", "cantidad": len(insumo)})
        except:
            insumo = Insumo.objects.all()
            return render (request, "listar_insumos.html", {"insumos": insumo, "mensaje":"no_puede", "cantidad": len(insumo)})

class FormularioInfoDeContacto(HttpRequest):
    @login_required
    def ver_info_contacto(request):
        texto = InformacionDeContacto.objects.get(id=1)
        contexto = {'texto':texto}
        return render (request, "infoContacto.html", contexto)
    @login_required
    def menu_editar_info_contacto(request):
        texto = InformacionDeContacto.objects.get(id=1)
        contexto = {'texto':texto}
        return render (request, "menu_info_de_contacto.html", contexto)
    @login_required
    def editar_info_contacto(request, id_texto):
        texto = InformacionDeContacto.objects.get(id=id_texto)
        form = Registro_info_de_contacto(instance=texto)
        return render (request, "modificar_info_de_contacto.html", {"form":form, "texto":texto})
    @login_required
    def actualizarInfoDeContacto(request, id_texto):
        texto = InformacionDeContacto.objects.get(id=id_texto)
        form = Registro_info_de_contacto(request.POST, instance = texto)

        if form.is_valid():
        #    db.connections.close_all()
            if form.cleaned_data.get('telefono2') == 0:
                form.saveTelefono2None()
            form.save()
            response = redirect('/menu_info_de_contacto/')
            return response
        else:
            print(form.cleaned_data.get('direccion'))
            print(form.cleaned_data.get('email'))
            print(form.cleaned_data.get('celular'))
            print(form.cleaned_data.get('telefono1'))
            print(form.cleaned_data.get('telefono2'))
            print(form.cleaned_data.get('descripcion'))

class FormularioComentario(HttpRequest):
    @login_required
    def mostrar_viajes(request):
        anuncio = Registro_anuncio()
        anuncios = Anuncio.objects.all().order_by('-id')
        viajes = Viaje.objects.all()
        viajes_hechos=[]
        nombre_chofer={}
        usuario = request.user.id
        #faltaria agregar que el viaje sea realizado
        hoy = datetime.today()
        hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
        for i in viajes:
            if i.fecha_llegada.date() < hoy.date():
                viajes_hechos+=[i]
            else:
                if i.fecha_llegada.date() == hoy.date():
                    if str(i.fecha_llegada.time()) < hora:
                        viajes_hechos+=[i]
            chofer = Usuario.objects.get (id = i.chofer_id)
            nombre_chofer[i.chofer]= chofer.nombre +' '+ chofer.apellido
        if (request.user.tipo_usuario == 1):
             return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"viajes": viajes_hechos, "anuncios":anuncios, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
        else:
             if (request.user.tipo_usuario == 2):
                 return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos,"is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
             else:
                 return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})

    @login_required
    def ver_comentarios(request,id_viaje,tipo, id_user):
        comentario = Registro_comentario()
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
        pasaje = Pasaje.objects.filter(id_user = id_user, nro_viaje_id = id_viaje)
        if (tipo == 1):
             return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
        else:
             if (tipo == 2):
                 return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
             else:
                 return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})

    @login_required
    def guardar_comentario(request,id_viaje, tipo, id_user):
        comentario = Registro_comentario(request.POST)
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        pasaje = Pasaje.objects.filter(id_user = id_user)
        if comentario.is_valid():
            comentario.save()
            comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
            if (tipo == 1):
                 return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
            else:
                 if (tipo == 2):
                     return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
                 else:
                     return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})

    @login_required
    def eliminar_comentario(request, id_viaje,tipo,id_coment, id_user):
        comentario_eliminado = Comentario.objects.get(pk=id_coment)
        comentario_eliminado.delete()
        comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        pasaje = Pasaje.objects.filter(id_user = id_user)
        if (tipo == 1):
            return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
        else:
            if (tipo == 2):
                return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
            else:
                return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})


class FormularioAnuncio(HttpRequest):
    @login_required
    def crear_formulario(request):
        anuncio = Registro_anuncio()
        return render (request, "agregar_anuncio.html", {"dni": request.user.dni})

    @login_required
    def procesar_formulario(request):
        anuncio = Registro_anuncio(request.POST)
        if anuncio.is_valid():
            anuncio.save()
            anuncio = Registro_anuncio()
            return render (request, "agregar_anuncio.html", {"dni": request.user.dni, "mensaje":"ok"})


    @login_required
    def eliminar_anuncio(request, id_anuncio):
        anuncio_eliminado = Anuncio.objects.get(pk=id_anuncio)
        anuncio_eliminado.delete()
        comentarios = Comentario.objects.all().order_by('-id')
        anuncios = Anuncio.objects.all().order_by('-id')
        viajes = Viaje.objects.all()
        viajes_hechos=[]
        nombre_chofer={}
        usuario = request.user.id
        #faltaria agregar que el viaje sea realizado
        hoy = datetime.today()
        hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
        for i in viajes:
            if i.fecha_llegada.date() < hoy.date():
                viajes_hechos+=[i]
            else:
                if i.fecha_llegada.date() == hoy.date():
                    if str(i.fecha_llegada.time()) < hora:
                        viajes_hechos+=[i]
            chofer = Usuario.objects.get (id = i.chofer_id)
            nombre_chofer[i.chofer]= chofer.nombre +' '+ chofer.apellido
        if (request.user.tipo_usuario == 1):
             return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"comentarios": comentarios, "viajes": viajes_hechos, "anuncios":anuncios, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
        else:
             if (request.user.tipo_usuario == 2):
                 return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos,"is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
             else:
                 return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})


    @login_required
    def editar(request, id_anuncio):
        anuncio = Anuncio.objects.get(id=id_anuncio)
        form = Registro_anuncio(instance=anuncio)
        return render (request, "modificar_anuncio.html", {"form":form, "anuncio":anuncio})

    @login_required
    def actualizar(request, id_anuncio):
        anuncio = Anuncio.objects.get(id=id_anuncio)
        form = Registro_anuncio(request.POST, instance = anuncio)
        if form.is_valid():
            form.save()
            return render (request,"modificar_anuncio.html", {"form":form, "anuncio":anuncio, "mensaje": "ok"})


class ComprarPasaje(HttpRequest):
    @login_required
    def comprar_pasaje_menu(request,id_viaje):
        viaje = Viaje.objects.get(id =id_viaje)
        hora_llegada = viaje.fecha_llegada.time()
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        chofer = Usuario.objects.get (id = viaje.chofer_id)
        patente = Vehiculo.objects.get ( id = viaje.vehiculo_id).patente
        tipo_asiento = Vehiculo.objects.get ( id = viaje.vehiculo_id).premium
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
        return render (request, "comprar_pasaje_menu.html", {"viaje": viaje, "tipo_asiento":tipo_asiento,"nombre":nombre, "hora_llegada":hora_llegada, "chofer":chofer,"patente":patente, "ya_tiene":len(pasaje)})

    @login_required
    def mi_carrito(request,id_viaje):
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        precio_total =0
        for i in carrito:
            precio_total= precio_total + i.precio_ticket
        return render (request, "comprar_pasaje_carrito.html", {"viaje":viaje,"insumos":carrito, "cosas":len(carrito), "precio_total":precio_total})

    @login_required
    def confirmar_eliminado(request,id_viaje, id_ticket):
        ticket = Ticket.objects.get(id = id_ticket)
        ins = Insumo.objects.get(id=ticket.insumo.id)
        print(ins)
        insumo = Registro_insumo(instance=ins)
        viaje = Viaje.objects.get(id = id_viaje)
        return render (request, "comprar_pasaje_carrito_eliminar.html", {"ticket":ticket, "insumo":ins, "viaje": viaje})

    @login_required
    def eliminar_mi_carrito(request,id_viaje,id_ticket):
        ticket_eliminado = Ticket.objects.get(id=id_ticket)
        insumo = Insumo.objects.get(id = ticket_eliminado.insumo.id)
        cantidad = ticket_eliminado.cantidad
        form = Registro_insumo(request.POST, instance = insumo)
        ticket_eliminado.delete()
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        precio_total =0
        for i in carrito:
            precio_total= precio_total + i.precio_ticket
        if form.is_valid():
            form.save_insumo3(cantidad)
            return render (request, "comprar_pasaje_carrito.html", {"viaje":viaje,"insumos":carrito, "cosas":len(carrito),"precio_total":precio_total})
        else:
            print(form.cleaned_data.get('nombre'))
            print(form.cleaned_data.get('precio'))
            print(form.cleaned_data.get('stock'))
            print(form.cleaned_data.get('sabor'))
            print(form.cleaned_data.get('categoria'))


    @login_required
    def tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta()
        tarjetas_registradas = Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        usuario = request.user.id
        if len(tarjetas_registradas) != 0:
            tarjetas_registradas = errores_tareta2(tarjetas_registradas)
            if len(tarjetas_registradas) != 0:
                return render (request, "comprar_pasaje_tarjeta.html", {"mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
        return render (request, "comprar_pasaje_tarjeta.html", {"mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":0,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})

    def otra_tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta()
        tarjetas_registradas= Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        usuario = request.user.id
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        if len(tarjetas_registradas) != 0:
            return render (request, "comprar_pasaje_tarjeta.html", {"mensaje":"otra", "viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
        else:
            return render (request, "comprar_pasaje_tarjeta.html", {"mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":0,"carrito": carrito, "compro":len(carrito), "precio_total":precio_total})


    @login_required
    def setear_tarjeta(request, id_viaje, id_tarjeta):
        pasaje = Registro_pasaje()
        viaje_form = Registro_viaje()
        tarjeta = Tarjeta.objects.get(id=id_tarjeta)
        viaje = Viaje.objects.get(id =id_viaje)
        ruta_id = Ruta.objects.get(id=(viaje.ruta).id)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        usuario = request.user.id
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        return render (request, "comprar_pasaje_tarjeta2.html", {"viaje": viaje, "nombre":nombre,"tarjeta":tarjeta, "usuario":usuario, "carrito":carrito, "compro":len(carrito), "precio_total":precio_total})


    @login_required
    def procesar_tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta(request.POST)
        tarjetas_registradas= Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        usuario = request.user.id
        if tarjeta.is_valid():
            confirmacion= errores_tarjeta(tarjeta)
            if len(confirmacion) == 0:
                pasaje = Registro_pasaje()
                hay_tarjeta = Tarjeta.objects.filter(id_user_id = request.user.id, numero = tarjeta.cleaned_data.get('numero'))
                if len(hay_tarjeta):
                    id_t = Tarjeta.objects.get(numero = tarjeta.cleaned_data.get('numero'), id_user_id =request.user.id)
                else:
                    tarjeta.save()
                    id_t = Tarjeta.objects.last()
                return render (request, "comprar_pasaje_tarjeta3.html", {"usuario":usuario, "viaje": viaje, "nombre":nombre, "tarjeta":id_t, "ok":"ok", "carrito":carrito, "compro": len(carrito), "precio_total":precio_total})
            else:
                return render (request, "comprar_pasaje_tarjeta3.html", {"errores": confirmacion, "usuario":usuario,"viaje": viaje, "nombre":nombre, "ok": "not_ok","carrito":carrito, "compro": len(carrito), "precio_total":precio_total})

    @login_required
    def procesar_pasaje(request, id_viaje):
        pasaje = Registro_pasaje(request.POST)
        viaje = Viaje.objects.get(id=id_viaje)
        print(id_viaje)
        if pasaje.is_valid():
            verificar=Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
            if len(verificar) == 0:
                pasaje.save_pasaje()
                form = Registro_viaje(request.POST, instance = viaje)
                if form.is_valid():
                    ruta = Ruta.objects.get(id=(viaje.ruta).id)
                    form.save_viaje3(ruta)
                    verificar=Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
                    return render (request, "comprar_pasaje_pagar.html", {"aceptado":"si", "pasaje":verificar, "viaje":viaje})
            else:
                verificar=Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
                return render (request, "comprar_pasaje_pagar.html", {"aceptado":"no", "pasaje":verificar, "viaje":viaje})

    @login_required
    def ver_tienda(request, id_viaje):
        insumos = Insumo.objects.all()
        stocks={}
        for i in insumos:
            stocks[i.id] = range(1,i.stock+1)
        viaje = Viaje.objects.get(id= id_viaje)
        usuario = request.user.id
        return render (request, "comprar_pasaje_tienda.html", {"insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"no"})

    @login_required
    def procesar_ver_tienda(request, id_viaje, id_insumo):
        carrito = Registro_ticket()
        insumo_comprado = Registro_insumo()
        viaje = Viaje.objects.get(id= id_viaje)
        insumo = Insumo.objects.get(id=id_insumo)
        usuario = request.user.id
        insumos = Insumo.objects.all()
        stocks={}
        for i in insumos:
            stocks[i.id] = range(1,i.stock+1)
        return render (request, "comprar_pasaje_seleccionar_cantidad.html", {"insumos":insumos,"insumo":insumo, "stocks":stocks, "usuario":usuario, "viaje":viaje})

    @login_required
    def procesar_confirmacion_insumo(request, id_viaje, id_insumo):
        ya_esta = Ticket.objects.filter(id_user = request.user.id, viaje_id = id_viaje, insumo_id = id_insumo)
        if len(ya_esta) != 0:
            ins = str(ya_esta).replace('<QuerySet [<Ticket: Ticket object (','').replace(')>]>','')
            ins = Ticket.objects.get(id = ins)
            cant= ins.cantidad
            ticket = Registro_ticket(request.POST, instance= ins)
            ok=True
        else:
            ticket = Registro_ticket(request.POST)
            ok=False
        insumo_comprado = Insumo.objects.get(id=id_insumo)
        viaje = Viaje.objects.get(id= id_viaje)
        usuario = request.user.id
        form = Registro_insumo(request.POST, instance = insumo_comprado)
        if ticket.is_valid():
            cantidad = ticket.cleaned_data.get('cantidad')
            if ok:
                ticket.save_ticket2(insumo_comprado.precio, cant)
            else:
                ticket.save_ticket(insumo_comprado.precio)
            form = Registro_insumo(request.POST, instance = insumo_comprado)
            if form.is_valid():
                form.save_insumo2(cantidad)
                insumos = Insumo.objects.all()
                stocks={}
                for i in insumos:
                    stocks[i.id] = range(1,i.stock+1)
                return render (request, "comprar_pasaje_tienda.html", {"insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"si"})

    @login_required
    def cancelar_pasaje(request, id_viaje):
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id= id_viaje, estado= 'activo')
        print('pasaje', pasaje )
        if len(pasaje) != 0:
            pasaje = Pasaje.objects.get(id_user=request.user.id, nro_viaje_id= id_viaje, estado= 'activo')
        pasaje.estado ='cancelado'
        pasaje.save()
        viaje = Viaje.objects.get(id=id_viaje)
        viaje.asientos_disponibles = viaje.asientos_disponibles + 1
        viaje.save()

        return ListarViajes.listar_viajes_por_realizar(request)

    @login_required
    def ver_detalle_pasaje(request, id_viaje):
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get (id = viaje.chofer_id)
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
        if len(pasaje) != 0:
            pasaje = Pasaje.objects.get(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
        usuario = Usuario.objects.get(id = pasaje.id_user)
        tarjeta = Tarjeta.objects.get(id = pasaje.tarjeta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        return render (request, "ver_detalle_pasaje.html", {"viaje":viaje, "tarjeta":tarjeta, "usuario":usuario, "chofer":chofer, "precio_total":precio_total, "insumos":carrito, "inumo":len(carrito), "pasaje":pasaje})
