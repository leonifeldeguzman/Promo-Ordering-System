from flask import Flask, render_template
from routes.promo_routes import promo_routes

app = Flask(__name__)

app.register_blueprint(promo_routes)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)