from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de données pour les demandes de suppression
class SuppressionDemande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True, unique=True)
    confirmation_code = db.Column(db.String(64), unique=True)
    status = db.Column(db.String(64))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'confirmation_code': self.confirmation_code,
            'status': self.status
        }

# Création de la table au premier lancement
@app.before_first_request
def create_tables():
    db.create_all()

# Route pour traiter les demandes de suppression
@app.route('/suppression', methods=['POST'])
def create_suppression_demande():
    data = request.get_json()
    demande = SuppressionDemande(user_id=data['user_id'], confirmation_code=data['confirmation_code'], status='en attente')
    db.session.add(demande)
    db.session.commit()
    return jsonify(demande.to_dict()), 201

# Route pour vérifier l'état d'une demande
@app.route('/suppression/<confirmation_code>', methods=['GET'])
def get_demande_status(confirmation_code):
    demande = SuppressionDemande.query.filter_by(confirmation_code=confirmation_code).first()
    if demande is None:
        return jsonify({'message': 'Demande non trouvée'}), 404
    return jsonify(demande.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
