from django.urls import path
from . import views

urlpatterns =[
    path('producto/', views.verProductos, name="producto"),
    path('producto/<str:id>', views.verProductos, name="producto"),
    path('carrito/<str:id>', views.agregar, name="carrito"),
    path('vercarrito/', views.verCarrito, name="ver_carrito"),
    path('eliminar/<str:id>', views.eliminarCarrito, name="eliminar"),
    path('cambiarCantidad/', views.cambiarCantidad),
]