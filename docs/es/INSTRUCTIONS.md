# Guía de Uso de la Plantilla de Módulo de Python (Legacy)

Este proyecto es una plantilla para crear un módulo de Python instalable, basada en las prácticas de empaquetado tradicionales con `setup.py` y `setup.cfg`. Su objetivo es servir como guía de arranque, mostrando una estructura de proyecto robusta, buenas prácticas y los procesos comunes en el ciclo de vida de un paquete.

## Cómo Empezar

Sigue estos pasos para usar esta plantilla y empezar tu propio módulo.

### 1. Clonar el Repositorio

Clona este repositorio en tu máquina local con el nombre que desees para tu nuevo proyecto:

```bash
git clone https://github.com/usuario/plantilla-python.git mi-nuevo-modulo
cd mi-nuevo-modulo
```

### 2. Renombrar el Módulo

El código fuente principal se encuentra en la carpeta `module_name`. Debes renombrarla para que coincida con el nombre de tu paquete Python.

```bash
mv ecomm_review_analyzer mi_paquete
```

### 3. Actualizar los Metadatos del Paquete

Abre el archivo `mi_paquete/__init__.py` y edita los siguientes campos con tu información:

```python
# mi_paquete/__init__.py

__author__ = "Tu Nombre"
__email__ = "tu_email@dominio.com"
__version__ = "0.0.1"  # O la versión inicial que prefieras

PACKAGE_NAME = "mi_paquete" # Asegúrate que coincida con el nuevo nombre de la carpeta
```

El archivo `setup.py` leerá esta información automáticamente.

### 4. Actualizar la Configuración de Versión

El archivo `setup.cfg` se usa para automatizar el versionado con `bumpversion`. Asegúrate de que la ruta apunte a tu nuevo directorio de paquete.

**Si renombraste `module_name` a `mi_paquete`**, actualiza `setup.cfg` así:

```ini
[bumpversion:file:mi_paquete/__init__.py]
search = __version__ = "{current_version}"
replace = __version__ = "{new_version}"
```

### 5. Elegir una Licencia

Este proyecto incluye por defecto la licencia "The Unlicense" (ver archivo `LICENSE`), que dedica el software al dominio público.

**Buena práctica:** Investiga qué licencia se adapta a tus necesidades. `choosealicense.com` es un excelente recurso. Una vez elegida, reemplaza el contenido del archivo `LICENSE`.

### 6. Instalar Dependencias

**Buena práctica:** Es muy recomendable usar un entorno virtual para aislar las dependencias de tu proyecto.

```bash
# Crear un entorno virtual
python -m venv .venv

# Activar el entorno (en macOS/Linux)
source .venv/bin/activate

# Activar el entorno (en Windows)
.\.venv\Scripts\activate
```

Instala las dependencias y tu paquete en modo editable. Esto te permitirá probar tus cambios localmente de forma inmediata.

```bash
# Instalar dependencias
pip install -r requirements_dev.txt
pip install -r requirements.txt

# Instalar el paquete en modo editable
pip install -e .
```

### 7. ¡A Programar!

¡Listo! Ya puedes empezar a desarrollar tu módulo. Añade tu código dentro de la carpeta `mi_paquete`.

---

## Calidad de Código y Tareas Automatizadas con `Makefile`

Para facilitar las tareas comunes y mantener un código limpio y consistente, esta plantilla incluye herramientas de calidad de código y un `Makefile`.

### Herramientas de Calidad de Código

-   **Ruff (`ruff`)**: Un linter y formateador de Python extremadamente rápido. Ayuda a detectar errores, malas prácticas y problemas de estilo.
-   **Black (`black`)**: Un formateador de código "sin concesiones" que asegura un estilo uniforme en todo el proyecto.

Estas herramientas están configuradas en el archivo `pyproject.toml`.

### Comandos del `Makefile`

El `Makefile` contiene atajos para los comandos más comunes. Para ver todos los comandos disponibles, ejecuta `make help`.

-   `make install`: Crea un entorno virtual (si no existe) e instala todas las dependencias. **Es el primer comando que deberías ejecutar.**
-   `make test`: Ejecuta la suite de pruebas.
-   `make lint`: Revisa el código en busca de errores y problemas de estilo con `ruff`.
-   `make format`: Formatea todo el código del proyecto con `ruff` y `black`.
-   `make build`: Construye el paquete para su distribución.
-   `make clean`: Elimina todos los archivos generados (entorno virtual, artefactos de build, etc.).

---

## Testing con `pytest`

`pytest` es el estándar de facto para testing en Python por su simplicidad y potencia.

**Escribir Tests:**
Simplemente crea funciones que empiecen con `test_` y usa `assert` para comprobar los resultados.

```python
# tests/test_main.py
from ecomm_review_analyzer.main import greet


def test_greet_with_name():
    """Prueba que la función saluda por nombre."""
    assert greet("Javi") == "Hello, Javi"
```

**Ejecutar Tests:**
Usa el atajo del `Makefile`:
```bash
make test
```
O ejecuta `pytest` directamente:
```bash
pytest
```

---

## Versionado Semántico y `bumpversion`

El versionado ayuda a comunicar qué tipo de cambios incluye una nueva versión. Usamos el **Versionado Semántico** (formato `MAYOR.MENOR.PARCHE`).

-   **PARCHE (`PATCH`)**: Corrección de bugs retrocompatible.
-   **MENOR (`MINOR`)**: Nueva funcionalidad retrocompatible.
-   **MAYOR (`MAJOR`)**: Cambios que rompen la retrocompatibilidad.

`bumpversion` es una herramienta que automatiza la actualización de la versión en todos los archivos necesarios.

### Uso de `bumpversion`

**Buena práctica:** Antes de subir la versión, asegúrate de que todos tus cambios están en `git`.

```bash
# Sube un parche (e.g., de 0.0.1 a 0.0.2)
bumpversion patch

# Sube una versión menor (e.g., de 0.0.2 a 0.1.0)
bumpversion minor

# Sube una versión mayor (e.g., de 0.1.0 a 1.0.0)
bumpversion major
```

Estos comandos actualizan la versión en `VERSION.txt` y en el `__init__.py` de tu paquete, y crean un `commit` y un `tag` de `git` automáticamente.

---

## Empaquetado y Distribución

Cuando tu módulo esté listo para ser compartido, debes empaquetarlo.

### 1. Construir el Paquete

El siguiente comando genera dos formatos de distribución en una nueva carpeta `dist/`:

-   **Wheel (`.whl`)**: Un formato pre-compilado (binario) que acelera la instalación.
-   **Source Archive (`.tar.gz`)**: Un archivo con el código fuente (`sdist`).

```bash
python setup.py sdist bdist_wheel
```

**Buena práctica:** El archivo `.gitignore` de esta plantilla ya está configurado para ignorar las carpetas `dist/`, `build/` y `*.egg-info/`, que se generan durante este proceso.

### 2. Instalar Localmente (Sin Publicar)

Si quieres instalar el paquete en otro entorno local para probar el artefacto final antes de publicarlo, puedes usar el archivo `.whl` que generaste. Esto es útil para probar la instalación real del paquete en un entorno limpio.

```bash
# Instala el paquete usando la ruta al archivo wheel.
# Reemplaza el nombre del archivo con el que se generó en tu carpeta dist/.
pip install dist/mi_paquete-0.0.1-py3-none-any.whl
```

### 3. Publicar en PyPI

[PyPI (Python Package Index)](https://pypi.org/) es el repositorio oficial de paquetes de Python. Para publicar tu módulo, necesitarás la herramienta `twine`.

```bash
# Instalar twine si no lo tienes
pip install twine
```

**Buena práctica:** Antes de publicar en el PyPI real, es recomendable hacer una prueba en [TestPyPI](https://test.pypi.org/), un entorno de pruebas separado.

```bash
# Publicar en TestPyPI
twine upload --repository testpypi dist/*
```

Cuando estés seguro de que todo funciona, publícalo en el PyPI oficial:

```bash
# Publicar en PyPI (oficial)
twine upload dist/*
```

Twine te pedirá tu usuario y contraseña de PyPI. ¡Y listo, tu paquete estará disponible para que cualquiera lo instale con `pip`!

---

## Próximos Pasos: Haz Tuyo el Proyecto

Una vez que hayas configurado y probado la plantilla, es hora de hacerla tuya. Aquí hay algunos pasos para limpiar el contenido de ejemplo y empezar con tu propio código:

1.  **Elimina el código de ejemplo (`module_name/main.py`):**
    *   La función `greet()` y el punto de entrada `main()` son solo ejemplos. Bórralos y empieza a escribir la funcionalidad real de tu módulo.

2.  **Borra los tests de ejemplo (`tests/test_main.py`):**
    *   Este archivo contiene tests para la función `greet()`. Borra este archivo o vacía su contenido para empezar a escribir tus propios tests.

3.  **Actualiza tu registro de cambios (`CHANGELOG.md`):**
    *   El archivo `CHANGELOG.md` está vacío, listo para que añadas tu primera entrada.
    *   Puedes empezar con algo como: `0.0.1 - YYYY-MM-DD: Initial project setup from template.`

4.  **Revisa la licencia (`LICENSE`):**
    *   Aunque ya lo mencionamos, asegúrate de que el archivo `LICENSE` contenga la licencia final que deseas usar para tu proyecto.
