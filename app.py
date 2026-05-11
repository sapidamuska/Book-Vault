from flask import Flask
from config import Config
from models import db, User
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
register_routes(app)

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password="admin123",
            email="admin@bookvault.com",
            role="admin",
            approved=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)