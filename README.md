# Integrantes
Valeska Aguirre
Bastián Cabello
Nicolás Espejo
Andrés González

# Plataforma de Retos Lógicos y Matemáticos

## Descripción
Este proyecto es una plataforma web educativa para la publicación y resolución de retos lógicos y matemáticos. Permite:  
- Publicar acertijos y problemas categorizados por dificultad.  
- Registrar respuestas de los usuarios y calcular puntajes automáticamente.  
- Mostrar un ranking general de usuarios basado en los puntos obtenidos.  
- Gestionar usuarios mediante un modelo personalizado (`Usuario`) con puntaje total.  

**Rubro:** Educación / Juegos Mentales

---

## Instalación

1. Clonar el repositorio:
- git clone https://github.com/Saebloom/Proyecto_NUAM_TIHI43_V.git
- cd Proyecto_NUAM_TIHI43_V

2. Crear entorno virtual:
- python3 -m venv environment
- source environment/bin/activate  # Linux

3. Instalar dependencias:
pip install -r requirements.txt

4. Aplicar migraciones:
- python manage.py makemigrations
- python manage.py migrate

5. Crear superusuario:
- python manage.py createsuperuser
- Crear nombre de superusuario: ""
- correo electronico super usuario: ""
- Crear contraseña: ""

6. Ejecutar servidor de desarrollo:
- python manage.py runserver
- Luego abre tu navegador en http://127.0.0.1:8000/

## Uso

- Registro y login: Los usuarios pueden registrarse con su nombre completo, email y contraseña.
- Publicación de retos: Solo el superusuario o el creador del reto pueden publicar o eliminar retos.
- Responder retos: Los usuarios pueden intentar resolver los retos, acumulando puntos por respuestas correctas.
- Ranking: Se muestra el top 10 de usuarios según puntaje total.

## Estructura del proyecto:

PROYECTO_NUAM/
│
├─ miapp/                  # Aplicación principal
│   ├─ migrations/         # Migraciones de la base de datos
│   ├─ templates/          # Plantillas HTML
│   ├─ static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├─ admin.py
│   ├─ forms.py
│   ├─ models.py
│   ├─ urls.py
│   └─ views.py
├─ myproject/              # Configuración principal de Django
├─ manage.py
├─ requirements.txt        # Dependencias del proyecto
├─ .gitignore
└─ README.md               # Este archivo

## Dependencias:

- Django==5.2.6
- asgiref==3.9.2
- sqlparse==0.5.3
- tzdata==2025.2

(Todas instalables con pip install -r requirements.txt)

## Notas:

- Se utiliza SQLite como base de datos por defecto.
- Las migraciones no están incluidas en el repositorio; se deben generar con makemigrations y migrate.
- El modelo de usuario está personalizado (Usuario) y se configura en settings.py con AUTH_USER_MODEL = 'miapp.Usuario'.
