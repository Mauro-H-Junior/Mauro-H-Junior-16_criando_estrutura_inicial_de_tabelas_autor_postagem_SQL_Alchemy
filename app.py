
from flask import Flask, jsonify, request
from app_db import Autor, Postagem, app, db
import json
# Rota padrão - GET https://localhost:5000
from functools import wraps #Para validar o token para postagens 
from flask import make_response
import jwt
from datetime import datetime, timedelta

#--------------------- POSSO APLICAR ESSA FUNÇÃO A ALGUMA ROTA QUE NECESSITE DE DECORAÇÃO
def token_obrigatório(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #Verificar se token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluído'}, 401)
        # Se temos um token, validar acesso consultando o BD
        try:
         
            resultado = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()

        except:
            return jsonify({'mensagem': 'Token é invalido'}, 401)
        return f(autor, *args, **kwargs)
    return decorated

#-------------------------------------------

@app.route('/postagem')
@token_obrigatório
def obter_postagens(autor):
    postagens = Postagem.query.all()

    list_postagens = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        list_postagens.append(postagem_atual)
    return jsonify({'postagens': list_postagens})

# Obter postagem por id - GET https://localhost:5000/postagem/1


@app.route('/postagem/<int:id_postagem>', methods=['GET'])
@token_obrigatório
def obter_postagem_por_indice(autor,id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor

    return jsonify({'postagens': postagem_atual})

# Criar uma nova postagem - POST https://localhost:5000/postagem


@app.route('/postagem', methods=['POST'])
@token_obrigatório
def nova_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(
        titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])

    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso'})

# Alterar uma postagem existente - PUT https://localhost:5000/postagem/1


@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
@token_obrigatório
def alterar_postagem(autor,id_postagem):
    postagem_alterada = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = postagem_alterada['titulo']
    except:
        pass
    try:
        postagem.id_autor = postagem_alterada['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucessso'})

# Excluir uma postagem - DELETE - https://localhost:5000/postagem/1


@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
@token_obrigatório
def excluir_postagem(autor,id_postagem):
    postagem_a_ser_excluida = Postagem.query.filter_by(
        id_postagem=id_postagem).first()
    if not postagem_a_ser_excluida:
        return jsonify({'mensagem': 'Não foi encontrado uma postagem com este id'})
    db.session.delete(postagem_a_ser_excluida)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem excluída com sucesso!'})

#----------------------------------------------------

@app.route('/autores')
@token_obrigatório
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})


@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatório
def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Autor não encontrado!')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify({'autor': autor_atual})

# Criar novo autor


@app.route('/autores', methods=['POST'])
@token_obrigatório
def novo_autor(autor):
    print('caiu')
    novo_autor = request.get_json()
    autor = Autor(
        nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])

    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso'}, 200)


@ app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatório
def alterar_autorautor(autor,id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem': 'Este usuário não foi encontrado'})
    try:
        autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
        autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
        autor.senha = usuario_a_alterar['senha']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Usuário alterado com sucesso!'})


@ app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatório
def excluir_autor(autor,id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'mensagem': 'Este autor não foi encontrado'})
    db.session.delete(autor_existente)
    db.session.commit()

    return jsonify({'mensagem': 'Autor excluído com sucesso!'})

#---------------------------------------
from flask import make_response
import jwt
from datetime import datetime, timedelta

# #CRIANDO ROTA DE LOGIN

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login Inválido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'}) #Ultimo parametro obrigatório para aparecer uma tela de login
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login Inválido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'}) #Ultimo parametro obrigatório para aparecer uma tela de login
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow() + 
        timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
        # econde_token = bytes(token,encoding='utf-8')
        # return jsonify({'token':econde_token.decode('utf-8')})
    return make_response('Login Inválido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'}) #Ultimo parametro obrigatório para aparecer uma tela de login

if __name__ == '__main__': # Para funcionar corretamente no Heroku
    app.run(port=5000, host='localhost', debug=True)