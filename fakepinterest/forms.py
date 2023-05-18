# criar os formularios do nosso site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

# estrutura que vai permitir criar os formularios - estrutura da classe

# DataRequired - campo obrigatorio
# ValidationError - quando der erro vai acusar
# Length - tamanho
# EqualTo - igualdade

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    # validar a função que eu quero dentro da classe
    # filter_by(email=email) - filtrando pelo email na busca no banco de dados
    # first() - lista que possui um único item
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        # Se já existe um usuario com o e-mail dessa lista, ele apresenta erro
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")

# FileField = enviar foto
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")