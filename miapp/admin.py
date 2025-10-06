from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Categoria, Dificultad, Reto, Respuesta, HistorialPuntaje, Ranking

# Personalización del admin de Usuario
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'username', 'us_nombre', 'email', 'is_staff', 'is_superuser', 'puntaje_total')
    search_fields = ('username', 'us_nombre', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('us_nombre', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Extra', {'fields': ('puntaje_total',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'us_nombre', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# Registrar todos los modelos
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Categoria)
admin.site.register(Dificultad)
admin.site.register(Reto)
admin.site.register(Respuesta)
admin.site.register(HistorialPuntaje)
admin.site.register(Ranking)
