# importando do arquivo fakepinterest o __init__
from fakepinterest import app

# criando a aplicação
# simular o servidor local
# se vc está executando este arquivos mesmo ele roda
if __name__ == "__main__":
    app.run(debug=True)
