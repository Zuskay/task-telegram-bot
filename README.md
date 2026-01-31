## Instalación y Ejecución Local - Guía Paso a Paso

Esta sección contiene instrucciones detalladas para ejecutar el proyecto completamente en tu máquina local.

### Prerequisitos Requeridos

Antes de comenzar, asegúrate de tener lo siguiente instalado:

1. **Python 3.11+**
   - Descarga desde [python.org](https://www.python.org/downloads/)
   - Verifica la instalación: `python --version`

2. **Git**
   - Descarga desde [git-scm.com](https://git-scm.com/)
   - Verifica: `git --version`

3. **Redis Server**
   - Opción A (Windows con WSL): Instala en WSL2
   - Opción B (Docker): `docker run -d -p 6379:6379 redis:latest`
   - Opción C (Online): Usa Redis Cloud (https://redis.com/try-free/)
   - Verifica: `redis-cli ping` (debe retornar "PONG")

### Obtener Credenciales Necesarias

#### 1. **Token de Telegram Bot** 
1. Abre Telegram y busca [@BotFather](https://t.me/botfather)
2. Escribe `/newbot` y sigue las instrucciones
3. Elige un nombre para tu bot (ej_usado: "Zusy")
4. Elige un username único (ej_usado: "ZusyTasks_bot")
5. BotFather te dará un token similar a: `123456789:ABCdefGHIjklmnoPQRstuvWXYZ`
6. **Guarda este token**, lo necesitarás en el `.env`

#### 2. **OpenAI API Key**
1. Ve a [platform.openai.com](https://platform.openai.com)
2. Inicia sesión o crea una cuenta
3. Ve a "API keys" en el menú lateral
4. Haz clic en "Create new secret key"
5. Copia la clave (formato: `sk-proj-...`)
6. **Guarda esta clave**, no podrás verla de nuevo

#### 3. **Ngrok Auth Token**
1. Ve a [ngrok.com](https://ngrok.com) y crea una cuenta gratuita
2. Ve a "Getting Started" → "Your Authtoken"
3. Copia tu token único
4. **Guarda este token** para después

---

### Paso 1: Clonar el Repositorio

Abre una terminal (PowerShell en Windows) y ejecuta:

```bash
# Navega a donde quieres guardar el proyecto
cd C:\Users\TuUsuario\Desktop

# Clona el repositorio
git clone <repository-url>
cd task-telegram-bot

# Verifica que estés en la carpeta correcta
dir
# Deberías ver: src/, prompts/, README.md, requirements.txt, .env.example, etc.
```

---

### Paso 2: Crear y Activar Entorno Virtual

El entorno virtual aísla las dependencias del proyecto de tu Python global.

**Para Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\activate

```

**Para Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate
```

**Verificación:** Deberías ver `(.venv)` al inicio del prompt de la terminal.

---

### Paso 3: Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias requeridas:

```bash
# Actualiza pip a la versión más reciente
pip install --upgrade pip

# Instala todas las dependencias del proyecto
pip install -r requirements.txt

# Verifica la instalación (opcional)
pip list
```

---

### Paso 4: Crear Archivo de Configuración (.env)

Crea un archivo `.env` en la raíz del proyecto con tus credenciales:

**Contenido del archivo `.env`:**
```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ
OPENAI_API_KEY=sk-proj-your-actual-key-here
NGROK_AUTHTOKEN=your-ngrok-token-here
REDIS_URL=redis://localhost:6379/0
```

**IMPORTANTE:**
- Reemplaza los valores con tus credenciales reales
- Nunca compartas este archivo (contiene secretos)
- Asegúrate de que `.env` esté en `.gitignore`

---

### Paso 5: Verificar que Redis está Funcionando

Antes de ejecutar el bot, asegúrate de que Redis está corriendo:

**Si instalaste Redis localmente:**
```bash
# En una terminal separada, inicia Redis
sudo service redis-server start

# verifica la conexión
redis-cli ping
# Debe retornar: PONG
```

**Si usas Docker:**
```bash
# Inicia Redis en Docker
docker run -d -p 6379:6379 redis:latest

# Verifica (necesitas redis-cli instalado)
redis-cli ping
```

**Si usas Redis Cloud:**
- Actualiza `REDIS_URL` en `.env` con tu URL de conexión
- Ej: `redis://default:password@host:port`

---

### Paso 6: Ejecutar el Bot

Con todo configurado, ejecuta el bot:

```bash
# Asegúrate de que estés en la carpeta correcta
# y que el entorno virtual está activado (deberías ver .venv al inicio del terminal)

# Ejecuta el bot
python -m src.main
```

**Verás algo como esto:**
```
2026-01-31 10:00:00.000 | INFO     | __main__:main:17 - Starting Telegram CRUD Bot...
2026-01-31 10:00:01.234 | INFO     | cel.gateway.message_gateway:setup:585 - Forwarding established from https://YOUR-UNIQUE-ID.ngrok-free.dev to 127.0.0.1:5004
2026-01-31 10:00:01.567 | INFO     | __main__:main:51 - Audio processing (STT) enabled with Whisper API
INFO:     Uvicorn running on http://127.0.0.1:5004
```
---

### Paso 7: Probar el Bot en Telegram

1. **Abre Telegram** en tu teléfono o escritorio
2. **Busca tu bot** por el nombre que creaste (ej: "Mi Task Manager")
3. **Haz clic en "Iniciar"**
4. **Prueba estos comandos:**

```
Mensaje: "ayuda"
Respuesta: [Muestra opciones disponibles]

Mensaje: "agregar tarea: Comprar leche"

Mensaje: "mostrar mis tareas"
Respuesta: [Lista todas tus tareas]

Mensaje: "chao"
Respuesta: "¡Hasta luego! Tus tareas están seguras aquí."
```

---

### Paso 8: Probar Características Especiales

#### Mensajes de Voz (STT)
1. En Telegram, presiona el botón de micrófono
2. Graba algo como: "recordarme llamar a mamá"
3. El bot transcribe el audio y crea la tarea

#### Detectar Idioma
```
Mensaje en inglés: "show my tasks"
Respuesta: (en inglés)

Mensaje en español: "mostrar mis tareas"
Respuesta: (en español)
```

#### Caracteres Especiales
```
Mensaje: "tarea: Proyecto v2.0,final"
Respuesta: Guarda exactamente "Proyecto v2.0,final"
```

---

### Verificación Final

Para confirmar que todo está funcionando:

1. **Terminal 1: Inicia Redis**
   ```bash
   sudo service redis-server start
   ```

2. **Terminal 2: Activa entorno y ejecuta bot**
   ```bash
   .\.venv\Scripts\activate  # Windows
   python -m src.main
   ```

3. **En Telegram: Envía un mensaje al bot**
   - Espera respuesta (puede tomar 5-10 segundos la primera vez)