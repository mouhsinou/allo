from flask import Flask, request, jsonify
from flask_cors import CORS
from apiMoneyFusion import PaymentClient

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis Flutter

client = PaymentClient(api_key_url="https://www.pay.moneyfusion.net/AlloPro/3165671b962b6273/pay/")

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON in request body'}), 400
    
    print("Données reçues:", data)  # Debug
    
    try:
        payment = client.create_payment(
            total_price=data['total_price'],
            articles=data['articles'],
            numero_send=data['numero_send'],
            nom_client=data['nom_client'],
            user_id=data['user_id'],
            order_id=data['order_id'],
            return_url=data['return_url']
        )
        print("Réponse MoneyFusion:", payment)  # Debug
        return jsonify(payment)
    except Exception as e:
        print("Erreur lors de l'appel MoneyFusion:", str(e))  # Debug
        return jsonify({'error': str(e)}), 500

@app.route('/get_payment/<token>', methods=['GET'])
def get_payment(token):
    payment_info = client.get_payment(token)
    return jsonify(payment_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)