# precisa ter esse arquivo obrigatorio para criar o projeto utilizando Flask
from flask import Flask
# importando o banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# criação so site
# criando o app Flask com o nome que o app vai ter
app = Flask(__name__)
# criando o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# garante a segurança do app
app.config["SECRET_KEY"] = "a3190c71717b80582c2b580d8bc02528"
# quando for salvar uma imagem no site, vai salvar dentro dessa pasta
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

# importação de outros arquivos no __init__ ocorre no final
from fakepinterest import routes
