from flask import Flask

from server.routes.status import status_dp
from server.routes.users import users_bp
from server.routes.error import error_db
def create_app():
  app = Flask(__name__)

  app.config['SQLALCHEMY_DATBASE_URI'] = 'postgresql://postgres:my-password@localhost:5432:serverdb'
  db.app = app
  db.init_app(app)
  db.create_all()
  
  app.register_blueprint(status_dp)
  app.register_blueprint(users_bp)
  app.register_blueprint(error_db)




  return app