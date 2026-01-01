from flask import Flask
from routes.paste import paste_bp

app = Flask(__name__)
app.register_blueprint(paste_bp)

if __name__ == "__main__":
    app.run(debug=True)
