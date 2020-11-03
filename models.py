from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Producer(db.Model):
    """This class contain information about producer of products"""

    __tablename__ = "producer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    product = db.relationship("Product", back_populates='producer')

    def __repr__(self):
        return f"<Producer(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Product(db.Model):
    """This class contain information about products available in shop"""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    description = db.Column(db.String)
    price = db.Column(db.Float)

    producer = db.relationship("Producer", back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {"id": self.id, "name": self.name}

