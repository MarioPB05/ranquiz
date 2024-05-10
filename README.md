![Ranquiz Logo](./static/assets/media/ilustrations/github_banner.png)

# Ranquiz

¡Bienvenido a Ranquiz, la red social donde tus listas cobran vida!

Ranquiz es una plataforma única que te permite explorar, crear y compartir listas sobre una amplia variedad de temas, desde personajes de videojuegos hasta tus comidas favoritas. Ya sea que estés buscando descubrir nuevas recomendaciones, compartir tus intereses o simplemente divertirte explorando listas curadas por otros usuarios, Ranquiz tiene algo para ti.

## Características principales
- **Explora listas**: Sumérgete en una variedad de listas creadas por otros usuarios y descubre nuevos temas que te apasionen.
- **Crea tus propias listas**: Deja volar tu imaginación y crea listas personalizadas sobre cualquier tema que te guste. Desde películas y libros hasta lugares para visitar, las posibilidades son infinitas.
- **Comparte con tus amigos**: Haz que tus listas sean públicas para que otros usuarios puedan disfrutarlas o compártelas directamente con tus amigos y familiares.
- **Diviértete y aprende**: Explora, vota y comenta en las listas de otros usuarios para divertirte mientras descubres nuevos intereses y conocimientos.

## Instrucciones de instalación y ejecución local

### Requisitos previos
Asegúrate de tener instalado/configurado lo siguiente en tu sistema:
- Python (preferiblemente Python 3.x)
- MariaDB
- Cuenta de Cloudinary
- Cuenta de Gmail

### Pasos a seguir
1. Clona el repositorio:
```bash
  git clone https://github.com/MarioPB05/ranquiz.git
```

2. Instala las dependencias:
```bash
  cd ranquiz
  pip install -r requirements.txt
```

3. Configura las siguientes variables de entornos en un archivo `.env` en la raíz del proyecto:

| Variable de Entorno   | Descripción                                                                                       | Valor Recomendado |
|-----------------------|---------------------------------------------------------------------------------------------------|-------------------|
| APP_SECRET_KEY        | Clave secreta utilizada por Django para firmar cookies y otros datos sensibles                    |                   |
| APP_DEBUG_MODE        | Modo de depuración de la aplicación. Puede ser `True` para activarlo, o `False` para desactivarlo | False             |
| DB_NAME               | Nombre de la base de datos de la aplicación                                                       | ranquiz_db        |
| DB_USER               | Nombre de usuario de la base de datos                                                             |                   |
| DB_PASSWORD           | Contraseña de la base de datos                                                                    |                   |
| DB_HOST               | Host de la base de datos                                                                          |                   |
| DB_PORT               | Puerto de la base de datos                                                                        | 3306              |
| CLOUDINARY_CLOUD_NAME | Nombre del cloud en Cloudinary utilizado para almacenar y gestionar imágenes                      |                   |
| CLOUDINARY_API_KEY    | Clave de la API de Cloudinary                                                                     |                   |
| CLOUDINARY_API_SECRET | Secreto de la API de Cloudinary                                                                   |                   |
| EMAIL_HOST            | Host del servidor de correo electrónico                                                           | smtp.gmail.com    |
| EMAIL_USE_TLS         | Indica si se debe usar TLS (`True/False`) para el servidor de correo electrónico                  | True              |
| EMAIL_USE_SSL         | Indica si se debe usar SSL (`True/False`) para el servidor de correo electrónico                  | False             |
| EMAIL_PORT            | Puerto utilizado por el servidor de correo electrónico                                            | 587               |
| EMAIL_HOST_USER       | Dirección de correo electrónico utilizada para enviar correos electrónicos                        |                   |
| EMAIL_HOST_PASSWORD   | Contraseña de la dirección de correo electrónico utilizada                                        |                   |

4. Inicializa la base de datos:
```bash
  python manage.py migrate
```

5. Ejecuta el servidor:
```bash
  python manage.py runserver 127.0.0.1:8000
```

6. Accede a la aplicación en tu navegador:
Abre tu navegador web y visita `http://127.0.0.1:8000`

¡Y eso es todo! Ahora deberías poder ejecutar Ranquiz en tu entorno local y empezar a explorar sus características.

## Autores
- [@marioperdiguero](https://github.com/marioperdiguero)
- [@david-perez-2357](https://github.com/david-perez-2357)
- [@jorgeariasmartin](https://github.com/jorgeariasmartin)
- [@mricofer](https://github.com/mricofer)

