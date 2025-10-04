class Config:

    """
     Configuration class for the Flask application.
    """

    SQLALCHEMY_DATABASE_URI = 'sqlite:///project2.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'your_secret_key_here'

    SECURITY_PASSWORD_SALT = 'your_password_salt_here'