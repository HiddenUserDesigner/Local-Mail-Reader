# Local Mail Reader con IA

## 1. Descripción
Script en Python que conecta con la API oficial de Gmail para descargar correos electrónicos recientes y procesar su contenido mediante un modelo de lenguaje local (como Llama 3 en LM Studio). Permite realizar preguntas y resumir la bandeja de entrada de forma interactiva manteniendo la **privacidad total de los datos** (sin enviar información a servidores externos).

## 2. Requisitos Previos
* **Lenguaje:** Python 3.x
* **Entorno de IA:** LM Studio (con servidor local encendido en el puerto de preferencia)
* **API Google:** Cuenta de Google Cloud con la API de Gmail habilitada y archivo `credentials.json`.

## 3. Características Clave
* **Privacidad garantizada:** Procesamiento 100% local a través de LM Studio.
* **Autenticación Segura:** Conexión a Gmail vía OAuth 2.0.
* **Integración:** Formato de peticiones estilo OpenAI API.

## 4. Instalación y Uso

1. Clonar el repositorio:

git clone https://github.com/HiddenUserDesigner/Local-Mail-Reader.git


2. Instalar dependencias necesarias:

pip install google-api-python-client google-auth-oauthlib requests


3. Colocar tu archivo de credenciales (`credentials.json`) en la raíz del proyecto.

4. Ejecutar el script:

python app.py
