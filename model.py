from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)



def init_db():
    with db.session.begin_nested():
        sample_products = [
            {
                "name": "Nordic Chair",
                "image_url": "product-1.png",
                "description": "Sample description for Nordic Chair.",
                "price": 50.00
            },
            {
                "name": "Kruzo Aero Chair",
                "image_url": "product-2.png",
                "description": "Sample description for Kruzo Aero Chair.",
                "price": 78.00
            },
            {
                "name": "Ergonomic Chair",
                "image_url": "product-3.png",
                "description": "Sample description for Ergonomic Chair.",
                "price": 43.00
            },
            {
                "name": "Wingback Chair",
                "image_url": "product-4.png",
                "description": "Sample description for Wingback Chair.",
                "price": 54.00
            }
        ]

        for product_data in sample_products:
            existing_product = Product.query.filter_by(name=product_data["name"]).first()
            if not existing_product:
                new_product = Product(**product_data)
                db.session.add(new_product)
    db.session.commit()
