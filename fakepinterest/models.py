# criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
# UserMixin - a classe de usuario que vai gerenciar a estrutura de login
from flask_login import UserMixin

# vai receber o id do usuario e retornar quem é o usuario
# obrigatorio para criar a estrutura de login com flask
# Usuario.query - encontrando o usuario no banco de dados
# get(int(id_usuario)) - encontrando de acordo com o id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# database.Model - permite criar a tabela no banco de dados
# database.Column - criando a coluna na tabela do banco de dados
# relationship - relação da class Usuario com a class Foto
# primary_key=True - chave primaria
# nullable=False - não pode ser nulo
# unique=True - e-mail único
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

# database.DateTime - número de data
# default=datetime.utcnow() - horário do momento
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)