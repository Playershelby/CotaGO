import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sslify import SSLify
import ssl
import sqlite3
from contextlib import closing
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import db, User

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Server configuration
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('models.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to validate data
def validar_dados(data, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in data or not data[campo]:
            return False, f'{campo.capitalize()} é obrigatório'
    return True, None

# Initialize the database
def init_db():
    with closing(get_db_connection()) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cotacoes (
                id TEXT PRIMARY KEY,
                valor REAL NOT NULL
            )
        ''')
        conn.commit()

# Route for user Login
@app.route('/', methods=['GET', 'POST'])
def _page():
    if request.method == 'POST':
        # Log the incoming request headers
        app.logger.debug(f'Request Headers: {request.headers}')  

        # Handle user login
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            login_user(user)

    else:
        # Render the login page
        return render_template('Login.html')

# Route for user logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message='Logout bem-sucedido'), 200

#Route for the home
@app.route('/home')
def home_page():
    return render_template('home.html')

# Route for the registration page
@app.route('/cadastro')
def cadastro_page():
    return render_template('Cadastro.html')

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='Usuário registrado com sucesso'), 201

# Route for adding quotes
@app.route('/cotações', methods=['POST'])
def adicionar_cotacao():
    data = request.json
    is_valid, error_message = validar_dados(data, ['id', 'valor'])

    if not is_valid:
        return jsonify({'error': error_message}), 400

    with closing(get_db_connection()) as conn:
        conn.execute('INSERT INTO cotacoes (id, valor) VALUES (?, ?)', (data['id'], data['valor']))
        conn.commit()
    
    return jsonify(data), 201

# Route for deleting quotes
@app.route('/cotações/<string:id>', methods=['DELETE'])
def deletar_cotacao(id):
    with closing(get_db_connection()) as conn:
        conn.execute('DELETE FROM cotacoes WHERE id = ?', (id,))
        conn.commit()
    return '', 204

# # Route for adding users
@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    data = request.json
    is_valid, error_message = validar_dados(data, ['id', 'nome'])

    if not is_valid:
        return jsonify({'error': error_message}), 400

    with closing(get_db_connection()) as conn:
        conn.execute('INSERT INTO usuarios (id, nome) VALUES (?, ?)', (data['id'], data['nome']))
        conn.commit()
    
    return jsonify(data), 201

# Route for updating users
@app.route('/usuarios/<string:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.json
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'error': 'Nome é obrigatório'}), 400

    with closing(get_db_connection()) as conn:
        usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
        if usuario is None:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        conn.execute('UPDATE usuarios SET nome = ? WHERE id = ?', (nome, id))
        conn.commit()
    
    return jsonify({'id': id, 'nome': nome})

# Route for deleting users
@app.route('/usuarios/<string:id>', methods=['DELETE'])
def deletar_usuario(id):
    with closing(get_db_connection()) as conn:
        conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()
    return '', 204

# Start the server with HTTPS
if __name__ == '__main__':
    init_db()  # Initialize the database
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/home/FF/CotaGO/cert.pem', '/home/FF/CotaGO/key.pem')
    app.run(host='0.0.0.0', port=3000, ssl_context=context)
# Adicione logs para verificar quem está fazendo a requisição
@app.before_request
def log_request_info():
    app.logger.debug(f'Request Path: {request.path}')
    app.logger.debug(f'Request Method: {request.method}')
    app.logger.debug(f'Request Headers: {request.headers}')
    app.logger.debug(f'Request Body: {request.get_data(as_text=True)}')
