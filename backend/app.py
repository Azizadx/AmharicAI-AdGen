from endpoint import main_app
from flask import Flask

app = Flask(__name__)

app.register_blueprint(main_app)


if __name__ == '__main__':
    app.run()