from threading import Thread
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os
from time import sleep

mail = Mail()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Erreur lors de la récupération de la clé secrete"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.getenv('MAIL_USERNAME')
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    SSL_DISABLE = True
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Par défaut : 587 pour TLS
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass

class DeveloppementConfig(Config):
    DEBUG = True

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DeveloppementConfig)
    app.url_map.strict_slashes = False
    app.jinja_env.globals.update(zip=zip)

    # Initialisation des extensions
    mail.init_app(app)

    return app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

app = create_app()
CORS(app)

@app.route('/api/send-mail', methods=['POST'])
def send_mail():
    if request.method == "POST":
        try:
            data = request.json
            print("Requête reçue :", request.json)

            required_fields = ['name', 'email', 'message']
            for field in required_fields:
                if field not in data:
                    return jsonify({"message": "Tous les champs sont requis"}), 400

            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            html_content = render_template('email_template.html', name=name, email=email, message=message)

            msg = Message(
                subject=f"Message de {name} via le formulaire de contact",
                sender=os.getenv('MAIL_USERNAME'),  # Expéditeur
                recipients=[os.getenv('MAIL_USER')],  # Destinataire
                body=f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}",
                html=html_content
            )

            # Envoyer l'e-mail dans un thread séparé
            thread = Thread(target=send_async_email, args=(app, msg))
            thread.start()

            print('Le message a bien été envoyé...')
            sleep(2)
            return jsonify({"message": "Email envoyé avec succès"}), 200

        except Exception as e:
            print('Erreur lors de l\'envoi :', str(e))
            return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(host="0.0.0.0", port=port)
