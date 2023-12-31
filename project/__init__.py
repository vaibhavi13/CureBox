from flask import Flask, request,url_for,redirect,session,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = 'project/static/images/'
    app.config['SECRET_KEY'] = 'root'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:deva@localhost:5432/PatientInsuranceManagement'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    mail.init_app(app)
    # app.config['SECRET_KEY'] = 'root'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/test'
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USERNAME'] = "carebox28@gmail.com"
    # app.config['MAIL_PASSWORD'] = "fbovsoxuziblozxy"
    # mail = Mail(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    from project.models.User import User
    from project.main.routes import main


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from project.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)
    from project.models.User import User
    # blueprint for non-auth parts of app
    app.register_blueprint(main)

    from project.doctor.doctorUtility import doctorUtility as doctorUtility_blueprint
    app.register_blueprint(doctorUtility_blueprint)

    
    from project.patient.patientUtility import patientUtility as patientUtility_blueprint
    app.register_blueprint(patientUtility_blueprint)

    
    from project.insuranceProvider.insuranceProviderUtility import insuranceProviderUtility as insuranceProviderUtility_blueprint
    app.register_blueprint(insuranceProviderUtility_blueprint)

    from project.common.commonUtility import commonUtility as commonUtility_blueprint
    app.register_blueprint(commonUtility_blueprint)

    #from project import db, create_app, models
    with app.app_context():
        db.create_all()
        db.session.commit()


    return app