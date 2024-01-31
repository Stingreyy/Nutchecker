from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()

    return app, db

app, db = create_app()

migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    manufacturer = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))

# Skapa uppladdningsmappen om den inte finns
import os
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        manufacturer = request.form['manufacturer']
        ingredients = request.form['ingredients']

        # Hämta bilden från formuläret
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            else:
                file_path = None
        else:
            file_path = None

        new_product = Product(name=name, manufacturer=manufacturer, ingredients=ingredients, image_path=file_path)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_products.html')

if __name__ == '__main__':
    app.run(debug=True)
