from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis le front-end

# Configuration Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
 

mail = Mail(app)



@app.route('/api/send-mail', methods=['POST'])
def send_mail():
    if request.method == "POST" : 
        
        try:
            data = request.json
            print("Requête reçue :", request.json)

            required_field = ['name' ,'email' , 'message']

            for field in required_field :
                if field not in data :
                    print("Tout les champs sont requis")
                    return jsonify({"message" :"Tous les champs sont requis"}) , 400
                
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
        
            html_content = render_template('email_template.html', name=name, email=email, message=message)
            msg = Message(
                subject=f"Message de {name} via le formulaire de contact",
                recipients=['lgcompany176@gmail.com '],  # 
                body=f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}" , 
                html = html_content
            )
            mail.send(msg)
            print('Le message a bien été envoyé ...')
            return   jsonify({"message": "Email envoyé avec succès"}), 200
           
        except Exception as e:
            print('Ereur lors de envoi ... : ' ,  str(e))
            return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 500
 

if __name__ == '__main__':
    app.run(debug=True , use_reloader = True)
