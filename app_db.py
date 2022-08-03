# biblioteca que auxilia a inserir dados dentro do bd sem código SQL
# pip install flask-sqlalchemy

from flask import Flask # Permite criar o API
from flask_sqlalchemy import SQLAlchemy #Permite nos criar o BD

#CRIAR O API FLASK
app = Flask(__name__) # A API receberá o nome do arquivo atual


#CRIAR UMA INSTANCIA DE SQLALCHEMY
app.config['SECRET_KEY'] = 'ASJHGDA445423253232' #Gerará um acesso de autenticação único na aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # É assim, pois nosso banco está local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db: SQLAlchemy #Define o tipo da variável para evitar possíveis erros

#DEFINIR A ESTRUTURA DA TABELA "POSTAGEM"
class Postagem(db.Model): #Db.Model é a informação que passo pra falar que vamos criar as tabelas dessa classe
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))  #relacionamento pelo nome da tabela

class Autor(db.Model):
    __tablename__= 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String) 
    email = db.Column(db.String) 
    senha = db.Column(db.String) 
    admin = db.Column(db.Boolean) 
    postagens = db.relationship('Postagem') #Nessa caso aqui eu passo o nome da classe para relacionar quantas postagens fez cada autor

#Comando utilizado para criar o banco de dados
def inicializar_banco():

    db.drop_all() # apaga qualquer estrutura prévia que exista
    db.create_all() # criando as tabelas

    #Criando usuários administradores
    autor = Autor(nome='mauro',email='mauro@gmail.com',senha='123', admin=True)
    db.session.add(autor) # Adicionar o autor no bd
    db.session.commit()

if __name__ == '__main__':
    inicializar_banco() # Para o banco não apagar tudo e gerar tudo toda vez

#DEFINIR A ESTRUTURA DA TABELA "AUTOR"