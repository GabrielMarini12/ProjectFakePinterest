from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

# criar o banco
with app.app_context():
    database.create_all()