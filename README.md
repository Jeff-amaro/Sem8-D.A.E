# Laboratorio 08 - Django REST Framework

API para administrar examenes, preguntas y opciones. Esta hecha con Django y
Django REST Framework, y es la continuacion del proyecto de cuestionarios del
curso.

## Como ejecutarlo

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

La API se puede revisar desde el navegador en `http://127.0.0.1:8000/api/`.
El panel de administracion de Django queda en `http://127.0.0.1:8000/admin/`.

## Organizacion del proyecto

```
Sem8-D.A.E/
├── config/              # ajustes y rutas principales del proyecto
├── quiz/                # logica de la API
│   ├── models.py        # Exam, Question y Option
│   ├── serializers.py   # validaciones y forma de los datos
│   ├── views.py         # viewsets de los tres recursos
│   ├── urls.py          # router de la API
│   ├── admin.py         # registro en el panel de Django
│   └── tests.py         # pruebas automaticas
├── manage.py
├── requirements.txt
└── .gitignore
```

## Modelo de datos

Un examen tiene varias preguntas y cada pregunta tiene sus opciones. Las
opciones viajan dentro de la pregunta porque casi siempre se consultan juntas y
asi se evita una peticion extra por cada alternativa. El examen, en cambio, se
manda solo con su `id`: la pregunta ya pertenece a un examen y repetir todo el
objeto dentro de cada pregunta seria innecesario.

Los campos `id`, `created_at` y los datos anidados de solo lectura los genera el
servidor. Al crear una pregunta con sus opciones, el serializador se encarga de
guardarlas; si se actualiza con una lista nueva, reemplaza las anteriores.

## Endpoints

| Recurso | Direccion | Metodo | Cuerpo de ejemplo | Respuesta |
|---------|-----------|--------|-------------------|-----------|
| Examenes | `/api/exams/` | GET | - | 200 con `count`, `next`, `previous` y `results` |
| Examenes | `/api/exams/` | POST | `{"title": "Examen de prueba", "description": "Semana 8"}` | 201 con el examen creado |
| Examen | `/api/exams/{id}/` | GET | - | 200 con el examen y sus preguntas |
| Examen | `/api/exams/{id}/` | PATCH | `{"title": "Examen corregido"}` | 200 con el cambio aplicado |
| Examen | `/api/exams/{id}/` | DELETE | - | 204 sin contenido |
| Preguntas | `/api/questions/` | GET | - | 200 paginado |
| Preguntas | `/api/questions/` | POST | `{"text": "Cuanto es 2 + 2?", "exam": 1, "options": [{"text": "4", "is_correct": true}, {"text": "5", "is_correct": false}]}` | 201 con la pregunta y sus opciones |
| Pregunta | `/api/questions/{id}/` | GET | - | 200 con la pregunta y sus opciones |
| Pregunta | `/api/questions/{id}/` | PATCH | `{"text": "Cuanto vale 2 + 2?"}` | 200 con el texto actualizado |
| Pregunta | `/api/questions/{id}/` | DELETE | - | 204 sin contenido |
| Opciones | `/api/options/` | GET | - | 200 paginado |
| Opciones | `/api/options/` | POST | `{"text": "4", "is_correct": true, "question": 1}` | 201 con la opcion creada |
| Opcion | `/api/options/{id}/` | PATCH | `{"is_correct": false}` | 200 con la opcion actualizada |
| Opcion | `/api/options/{id}/` | DELETE | - | 204 sin contenido |

### Filtros y busqueda

| Accion | Direccion | Resultado |
|--------|-----------|-----------|
| Preguntas de un examen | `/api/questions/?exam=1` | Solo las preguntas de ese examen |
| Buscar por enunciado | `/api/questions/?search=Django` | Preguntas cuyo texto contiene el termino |
| Paginar | `/api/exams/?page=2` | Segunda pagina, cinco elementos por pagina |

La paginacion esta configurada en `settings.py` con `PageNumberPagination` y un
tamano de pagina de cinco registros. Para las busquedas se usa `SearchFilter` y
para el filtro por examen se agrego `django-filter`, porque el parametro `exam`
necesita un backend que lo interprete.

## Errores que devuelve la API

| Caso | Peticion | Codigo | Mensaje |
|------|----------|--------|---------|
| Falta un campo obligatorio | POST `/api/exams/` con `{"description": "Sin titulo"}` | 400 | `{"title": ["This field is required."]}` |
| Tipo de dato incorrecto | POST `/api/questions/` con `"exam": "abc"` | 400 | `{"exam": ["Incorrect type. Expected pk value, received str."]}` |
| Opcion correcta invalida | POST `/api/questions/` con dos opciones `is_correct: true` | 400 | `{"options": ["A question must have exactly one correct option."]}` |

La validacion de la opcion correcta vive en `QuestionSerializer.validate`.
Revisa las opciones que llegan en la peticion (o las que ya tiene la pregunta si
se esta editando) y exige que haya exactamente una marcada como correcta. Si hay
cero o mas de una, responde con un error 400.

## Pruebas

Las pruebas estan en `quiz/tests.py` y cubren listado, creacion, campos
obligatorios, tipos incorrectos, opciones anidadas, filtro por examen y busqueda
por texto.

```bash
python manage.py test
```

Tambien se probo todo a mano desde la API navegable y desde un cliente HTTP
externo enviando JSON. Los codigos que se observaron fueron: 200 al listar y ver
detalles, 201 al crear, 200 al modificar con PATCH, 204 al eliminar y 404 al
consultar un recurso que ya no existe.

## Notas

- La `SECRET_KEY` se lee de la variable de entorno `DJANGO_SECRET_KEY`. Si no
  esta definida, se usa una clave de desarrollo que no debe servir para
  produccion.
- `db.sqlite3` y las carpetas `__pycache__` estan fuera del repositorio por el
  `.gitignore`.
- El trabajo fue desarrollado de forma individual por Jeff Amaro.
