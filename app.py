import os
from flask import Flask, render_template
from routes.promo_routes import promo_routes
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.register_blueprint(promo_routes)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)