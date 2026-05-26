from flask import Flask, render_template
from routes.promo_routes import promo_routes

app = Flask(__name__)
port = int(os.getenv('PORT', 8080))  # Use PORT from Railway, default to 8080
app.run(host='0.0.0.0', port=port)
app.secret_key = "supersecretkey"
app.register_blueprint(promo_routes)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)