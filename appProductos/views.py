from asyncio.windows_events import NULL
from csv import list_dialects
import json
from multiprocessing import context
from django.shortcuts import render
from asyncio.windows_events import NULL
from .models import Carrito, Producto
from django.http import JsonResponse
import json

# Create your views here.

def verProductos(request, id= NULL):
    if not id:
        listaProductos = Producto.objects.all()
        print('----------')
        print(listaProductos)
        context = {
            'productos': listaProductos,
        }
        return render(request, 'productos/productos.html', context)
    else:
        id = int(id)
        resgProducto = Producto.objects.get(id=id)
        context = {
            'producto': resgProducto,
        }
        return render(request, 'productos/unProductos.html', context)

"""
Funcion para el manejo de los productos en el carrito
"""
def agregar(request, id= NULL):
    id = int(id)
    user = request.user
    regProducto = Producto.objects.get(id=id)
    existe = Carrito.objects.filter(producto = regProducto, estado = 'carrito').exists()
    if existe:
        regCarrito = Carrito.objects.get(cliente=user,producto = regProducto, estado = 'carrito')
        regCarrito.cantidad += 1
        regCarrito.save()
    else:
        regCarrito = Carrito(cliente = user, producto = regProducto, precio = regProducto.precio)
        regCarrito.save()

    listaProductos = Producto.objects.all()
    context = {
        'productos' : listaProductos,
    }
    return render(request, 'productos/productos.html', context)


def verCarrito(request):
    regUser = request.user
    carrito = Carrito.objects.filter(cliente=regUser, estado='carrito')
    # Recorrer elementos del carrito para calcular totales

    listaCarrito = []
    total = 0
    for prod in carrito:
        unProducto={
			'cantidad': prod.cantidad,
			'icono': prod.producto.icono,
			'nombre': prod.producto.nombre,
			'valor': prod.producto.precio,
			'talla': prod.producto.talla,
			'total': int(prod.cantidad)	* int(prod.producto.precio),
			'id': prod.id,
	    }
 
        listaCarrito.append(unProducto) 
        total += unProducto['total']

    #ensamblar datos para la plantilla
    context = {
        'carrito':  listaCarrito,
        'subtotal': total,
        'iva': total * 0.19,
        'envio': 10000,
        'total': total * 1.19 + 8000,
    }
    print('pppp')
    print(context)
    return render(request, 'productos/carrito.html', context)


def eliminarCarrito(request, id):
    #Consultar el reg
    regCarrito = Carrito.objects.get(id=id)
    regCarrito.estado = 'cancelado'
    #guardar en DB
    regCarrito.save()
    #Desplegar el carrito
    return verCarrito(request)

def cambiarCantidad(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH')== 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            #toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            cantidad = int(data.get('cantidad'))
            if cantidad > 0:
                #lee el registro y lo modifica
                regProducto = Carrito.objects.get(id=id)
                regProducto.cantidad = cantidad
                regProducto.save()
            
            return JsonResponse({'mensaje': 'cantidad modificada a ' + str(cantidad)})
        
        return JsonResponse({'alarma' : 'no se pudo modificar...'}, status=400)
    
    else:
        return verCarrito(request)