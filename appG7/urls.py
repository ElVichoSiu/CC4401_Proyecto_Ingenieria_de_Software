from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register_user, name='register_user'), 
    path('', views.index_page, name='index_page'),
    path('login',views.login_user, name='login'),
    path('sesion',views.estudio_page, name='sesion'),
    path('logout',views.logout_user, name='logout'),
    path('opinion_usuario/<str:critico_name>/<str:criticado_name>/', views.opinion_usuario, name='opinion_usuario'),
    path('perfil/<str:user_apodo>/', views.UserProfile.as_view(), name='user_profile'),
    path('ver_sesiones', views.ver_sesiones, name='ver_sesiones'),
    path('session/<int:session_id>/join/', views.unirse_sesion, name='join_session'),
    path('session/<int:session_id>/leave/', views.salirse_sesion, name='leave_session'),
    path('unirse/<int:session_id>/', views.unirse_sesion, name='unirse_sesion'),
    path('salirse/<int:session_id>/', views.salirse_sesion, name='salirse_sesion'),
    path('mis_sesiones/', views.mis_sesiones, name='mis_sesiones'),
    path('detalle_sesion/<int:session_id>/', views.detalle_sesion, name='detalle_sesion'),
    path('expulsar_miembre/<int:session_id>/<int:miembro_id>/', views.expulsar_miembre, name='expulsar_miembre'),
    path('borrar_sesion/<int:session_id>/', views.borrar_sesion, name='borrar_sesion'),
]
