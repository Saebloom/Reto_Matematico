# miapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Reto, Respuesta
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Reto, Usuario, Dificultad, Categoria, Respuesta, Ranking
from .forms import CustomUserCreationForm # Importa el nuevo formulario

# ... (tus vistas existentes) ...
def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso. ¡Bienvenido!")
            return redirect('index') # Redirige al menú principal o a donde desees
        else:
            messages.error(request, "Error en el registro. Por favor, corrige los errores.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Modificar la vista 'publicar_reto' para usar los modelos de Django
@login_required
def publicar_reto(request):
    if request.method == "POST":
        re_nombre = request.POST.get("re_nombre")
        re_descripcion = request.POST.get("re_descripcion")
        respuesta_reto = request.POST.get("respuesta_reto")
        dificultad_id = request.POST.get("re_dificultad")
        categoria_id = request.POST.get("re_categoria")
        intentos = request.POST.get("intentos", 3)

        try:
            dificultad = Dificultad.objects.get(id_dificultad=dificultad_id)
            categoria = None
            if categoria_id:
                categoria = Categoria.objects.get(id_categoria=categoria_id)
                nuevo_reto = Reto.objects.create(
                re_nombre=re_nombre,
                re_descripcion=re_descripcion,
                respuesta_reto=respuesta_reto,
                re_dificultad=dificultad,
                re_categoria=categoria,
                intentos=intentos,
                re_usuario=request.user # Asigna el usuario actual como autor
            )
            messages.success(request, "Reto publicado exitosamente.")
            return redirect("acertijo")
        except Dificultad.DoesNotExist:
            messages.error(request, "La dificultad seleccionada no es válida.")
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría seleccionada no es válida.")
        except Exception as e:
            messages.error(request, f"Error al publicar el reto: {e}")
    dificultades = Dificultad.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "publicacion.html", {'dificultades': dificultades, 'categorias': categorias})

@login_required
def eliminar_reto(request, id_reto):
    reto = get_object_or_404(Reto, id_reto=id_reto)
    # Solo el superusuario o el creador pueden eliminar
    if request.user.is_superuser or request.user == reto.re_usuario:
        if request.method == 'POST':
            reto.delete()
            messages.success(request, 'El reto ha sido eliminado correctamente.')
            return redirect('acertijo')  # Cambia 'acertijo' por el nombre de la url principal
        else:
            messages.error(request, 'Método no permitido.')
            return redirect('acertijo')
    else:
        messages.error(request, 'No tienes permiso para eliminar este reto.')
        return redirect('acertijo')



# Modificar la vista 'acertijo' para mostrar retos de la base de datos
@login_required
def acertijo(request):
    retos = Reto.objects.all()
    usuario = request.user if request.user.is_authenticated else None
    respuestas_usuario = {}
    if usuario:
        respuestas = Respuesta.objects.filter(res_usuario=usuario, res_reto__in=retos)
        for respuesta in respuestas:
            respuestas_usuario.setdefault(respuesta.res_reto.id_reto, []).append(respuesta)
    context = {
        'retos': retos,
        'respuestas_usuario': respuestas_usuario,
        'usuario': usuario,
    }
    return render(request, 'acertijo.html', context)

# Nueva vista para manejar la respuesta a un acertijo
@login_required
def responder_reto(request, reto_id):
    reto = get_object_or_404(Reto, id_reto=reto_id)
    usuario = request.user

    if request.method == "POST":
        respuesta_usuario_str = request.POST.get("respuesta").strip().lower()
        respuesta_correcta_str = reto.respuesta_reto.strip().lower()

        # Contar intentos previos del usuario para este reto
        intentos_previos = Respuesta.objects.filter(res_usuario=usuario, res_reto=reto).count()

        if intentos_previos >= reto.intentos:
            messages.warning(request, f"Has agotado tus {reto.intentos} intentos para este reto.")
            return redirect('acertijo')

        respuesta_correcta = (respuesta_usuario_str == respuesta_correcta_str)
        puntaje_obtenido = 0

        if respuesta_correcta:
            puntaje_obtenido = reto.re_dificultad.puntaje
            messages.success(request, f"¡Respuesta correcta! Has ganado {puntaje_obtenido} puntos.")
            # Actualizar puntaje total del usuario
            usuario.puntaje_total += puntaje_obtenido
            usuario.save()

            # Registrar en HistorialPuntaje
            # HistorialPuntaje.objects.create(usuario=usuario, puntos=puntaje_obtenido)

            # Actualizar o crear Ranking
            ranking_entry, created = Ranking.objects.get_or_create(ra_usuario=usuario, defaults={'puntaje': puntaje_obtenido})
            if not created:
                ranking_entry.puntaje += puntaje_obtenido
                ranking_entry.save()
        else:
            messages.error(request, "Respuesta incorrecta. Inténtalo de nuevo.")

        # Guardar la respuesta del usuario
        Respuesta.objects.create(
            res_usuario=usuario,
            res_reto=reto,
            respuesta_usuario=respuesta_usuario_str,
            respuesta_correcta=respuesta_correcta,
            puntaje=puntaje_obtenido,
            intento=intentos_previos + 1
        )
        return redirect('acertijo') # Redirige de nuevo a la lista de acertijos

    # Si se accede por GET, simplemente muestra el acertijo (aunque esta vista es para POST)
    return redirect('acertijo')

# Modificar la vista 'ranking' para usar los modelos de Django
def ranking(request):
    # Obtener el ranking general de usuarios
    ranking_general = Usuario.objects.order_by('-puntaje_total')[:10] # Top 10 usuarios

    # Obtener el ranking por dificultad (esto requeriría más lógica si quieres un ranking por dificultad de retos resueltos)
    # Por ahora, mostraremos el ranking general.
    # Si quieres un ranking por dificultad, necesitarías agregar un campo de dificultad a la tabla Ranking
    # o calcularlo dinámicamente de las respuestas.

    context = {
        'ranking_general': ranking_general,
        # 'ranking_facil': [], # Puedes implementar esto si es necesario
        # 'ranking_medio': [],
        # 'ranking_dificil': [],
    }
    return render(request, 'ranking.html', context)

# Nueva vista para login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'login.html')

# Nueva vista para logout
@login_required
def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('index')


