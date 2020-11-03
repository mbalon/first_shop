from flask import Flask
from flask_sqlalchemy import request
from flask.json import jsonify
from models import db, Producer, Product

app = Flask(__name__)

# connect with database
db_name = 'shop_24_10_20.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)



@app.route("/add_producer", methods=["POST"])
def add_producer():
    data = request.get_json()
    try:
        producer = Producer(name=data["name"])
        db.session.add(producer)
        db.session.commit()
        return jsonify(producer.to_dict())
    except KeyError:
        response = jsonify({"error": "Bad request", "missing field": "name"})
        response.status_code = 400
        return response


@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.get_json()
    try:
        product = Product(name=data["name"])
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict())
    except KeyError:
        response = jsonify({"error": "Bad request", "missing field": "name"})
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run()
