# miapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Importar vistas de autenticación de Django

urlpatterns = [
    path('', views.index, name='index'),
    path('acertijo/', views.acertijo, name='acertijo'),
    path('ranking/', views.ranking, name='ranking'),
    path('publicacion/', views.publicar_reto, name='publicacion'), # Cambiado a publicar_reto
    path('acertijo/responder/<int:reto_id>/', views.responder_reto, name='responder_reto'), # Nueva URL para responder
    path('eliminar_reto/<int:id_reto>/', views.eliminar_reto, name='eliminar_reto'),

    # URLs de autenticación
    path('register/', views.registro, name='registro'),
    path('login/', views.user_login, name='login'), # Usamos nuestra vista personalizada
    path('logout/', views.user_logout, name='logout'), # Usamos nuestra vista personalizada
]

