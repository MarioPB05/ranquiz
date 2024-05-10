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

----

## Estructura del Proyecto
El proyecto Django sigue una arquitectura Modelo-Vista-Controlador (MVC), que se organiza en tres aplicaciones principales:

### API
La aplicación API maneja las solicitudes entrantes y dirige el flujo de datos al servicio correspondiente para su procesamiento. Aquí se encuentra la lógica de presentación y la coordinación de las respuestas a las solicitudes del cliente.

Componentes:
- **Controladores (Controllers)**: Responsables de manejar las solicitudes entrantes y dirigirlas al servicio apropiado para su procesamiento.
- **Modelos (Models)**: Representan la estructura de datos de la aplicación y definen la interacción con la base de datos.
- **Servicios (Services)**: Encapsulan la lógica de negocio y se utilizan para realizar operaciones específicas en los datos del modelo, como operaciones CRUD y cualquier otra lógica de negocio necesaria.
- **Routing.py (Enrutamiento)**: Contiene las rutas de la API y las vincula a los controladores correspondientes, especificando qué controlador manejará cada ruta.

### Core
La aplicación Core maneja las solicitudes relacionadas con el frontend de la aplicación. Aquí se completan las vistas utilizando los servicios proporcionados por la API. Los datos obtenidos de los servicios se utilizan para rellenar las plantillas HTML.

### Websockets
La aplicación Websockets se encarga de gestionar todas las solicitudes del protocolo WebSocket. WebSocket es un protocolo de comunicación bidireccional y en tiempo real que permite una conexión persistente entre el cliente y el servidor a través de la web, facilitando la transmisión eficiente de datos con baja latencia.

En nuestra aplicación, hemos utilizado la funcionalidad de Websockets para implementar notificaciones en tiempo real. Esto permite a los usuarios recibir actualizaciones instantáneas sobre eventos importantes dentro de la aplicación, como nuevos comentarios, cambios en las listas favoritas o nuevos seguidores. Gracias a Websockets, podemos proporcionar una experiencia de usuario más dinámica e interactiva, manteniendo a los usuarios informados de manera oportuna sobre las actividades relevantes en la plataforma.

---

## Share Codes
En nuestro proyecto, la columna `share_code` se repite en la mayoría de las tablas y desempeña un papel crucial en la representación única de diversos objetos, como listas, categorías, usuarios, entre otros.

El share code es un estándar diseñado para generar un código único que represente un objeto específico dentro de nuestra aplicación. Este estándar está definido por los dos primeros dígitos que indican el área a la que está asociada:
- LS: Listas
- CS: Categorías
- US: Usuarios

Los siguientes 18 dígitos del share code son el identificador único del recurso al que apuntan.

### Ventajas de utilizar Share Codes
1. **Seguridad**: Una de las principales ventajas de utilizar share codes es que proporciona una capa adicional de seguridad a nuestra aplicación. Al mostrar un código único en lugar de los IDs de la base de datos, protegemos la información sensible de nuestros recursos.
2. **Portabilidad**: Los share codes son independientes de la infraestructura subyacente, lo que significa que se pueden utilizar fácilmente en diferentes entornos y sistemas sin necesidad de cambiar la lógica de la aplicación.
3. **Uniformidad**: Al seguir un estándar predefinido para generar share codes, mantenemos una consistencia en la representación de nuestros recursos en toda la aplicación, lo que facilita su gestión y mantenimiento a largo plazo.
4. **Privacidad**: Al ocultar los IDs de la base de datos detrás de los share codes, protegemos la privacidad de nuestros usuarios al evitar que se revelen detalles innecesarios sobre la estructura interna de nuestra base de datos.

El uso de share codes es una práctica recomendada en el desarrollo de aplicaciones web que ofrece múltiples beneficios, tanto en términos de seguridad como de usabilidad. En nuestro proyecto, hemos adoptado esta técnica para garantizar la seguridad de nuestros usuarios finales.

---

## Autores
- [@marioperdiguero](https://github.com/marioperdiguero)
- [@david-perez-2357](https://github.com/david-perez-2357)
- [@jorgeariasmartin](https://github.com/jorgeariasmartin)
- [@mricofer](https://github.com/mricofer)

