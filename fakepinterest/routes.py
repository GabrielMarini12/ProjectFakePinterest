# criar as rotas do nosso site (os links)
# render_templete = vai buscar o arquivo html dentro da pasta templates
# url_for = permite direcionar o link através do nome da função e não com a rota
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
import os

# colocando o site no ar
# rota principal do nosso site (home page) / tela de login
# methods=["GET", "POST"] - sempre que estivermos usando um formulario pegando inf dos usuarios (method="POST" no html)
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    # validando os dados de acordo com a classe quando ele envia o formulario
    if form_login.validate_on_submit():
        # procurando usuario cujo email é igual ao do formulario
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # se encontrou algum usuario, entao vai continuar
        # verificando se a senha esta certa ou não
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # fazer o login do usuario e redirecionar ele para pagina dele
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)

# tela de criar conta
@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    # validando os dados de acordo com a classe quando ele envia o formulario
    if form_criarconta.validate_on_submit():
        # criptografar a senha do usuario, por segurança
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # se for valido vai criar o usuario
        usuario = Usuario(username=form_criarconta.username.data,
                          senha=senha, email=form_criarconta.email.data)
        # armazenando a variavel dentro do banco de dados
        database.session.add(usuario)
        # executando as alterações no banco de dados
        database.session.commit()
        # fazendo o login do usuario antes de redirecionar
        # remember=True = lembrar que o usuario ja esta logado (caso feche a pagina e abra novamente)
        login_user(usuario, remember=True)
        # função do flask - redirecionar o usuario para o perfil dele
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

# o valor que estiver no link (<usuario>) é o que sera passado para o html
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
# só pode ser acessado quando o usuario esta logado
@login_required
def perfil(id_usuario):
    # saber se o usuario esta vendo o perfil dele mesmo
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo o perfil dele
        form_foto = FormFoto()
        # se o formulario foi preenchido corretamente
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na past fotos_posts
            # (os.path.abspath(os.path.dirname(__file__)) - local do proprio arquivo
            # salvar o arquivo dentro da pasta certa
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome_seguro)
            arquivo.save(caminho)
            # registrar o arquivo no banco de dados
            # criar a foto no banco com o item "imagem" sendo o nome do arqivo
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    # ta vendo o perfil de outro usuario
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

# current_user - usuario que ja esta logado
@app.route("/logout")
@login_required
def logout():
    # vai deslogar o usuario que estiver logado
    logout_user()
    # redirecionando o usuario para homepage (tela de login)
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    # pegando todas as fotos do banco de dados para aparecer no feed
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)