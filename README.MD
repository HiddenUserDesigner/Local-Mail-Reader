# Local Mail Reader with IA

## 1. Description
Python script that connects to the official Gmail API to download recent emails and process their content using a local language model (such as Llama 3 in LM Studio). It allows users to ask questions and summarize their inbox interactively while maintaining complete data privacy (without sending information to external servers).

## 2. Requisitos Previos
* **Lenguaje:** Python 3.x
* **AI Environment: LM Studio (with the local server running on your preferred port)
* **Google API: Google Cloud account with the Gmail API enabled and a credentials.json file.

## 3. Características Clave
* **Guaranteed Privacy: 100% local processing through LM Studio.
* **Secure Authentication: Gmail connection via OAuth 2.0.
* **Integration: OpenAI API-style request format.

## 4. Installation and Usage

1. Clone the repository:

git clone https://github.com/HiddenUserDesigner/Local-Mail-Reader.git


2. Install the required dependencies:

pip install google-api-python-client google-auth-oauthlib requests

3. Place your credentials file (credentials.json) in the root directory of the project.

4. Run the script:

python app.py
