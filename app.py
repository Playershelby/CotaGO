from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sslify import SSLify
import ssl
import sqlite3
from contextlib import closing

# Server configuration
app = Flask(__name__)
sslify = SSLify(app)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Cambia 'database.db' por la ruta de tu base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Function to validate data
def validar_dados(data, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in data or not data[campo]:
            return False, f'{campo.capitalize()} é obrigatório'
    return True, None

# Route for the home page (Login)
@app.route('/', methods=['POST', 'GET'])
def home_page():
    return render_template('Login.html')

# Route for logout
@app.route('/logout')
def logout():
    # Implementar lógica de logout aquí
    return redirect(url_for('home_page'))

# Route for the registration page
@app.route('/cadastro')
def cadastro_page():
    return render_template('Cadastro.html')

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

# Route for adding users
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

# Initialize the database (implementar esta función según sea necesario)
def init_db():
    with closing(get_db_connection()) as conn:
        # Aquí puedes crear las tablas si no existen
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

# Start the server with HTTPS
if __name__ == '__main__':
    init_db()  # Initialize the database
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/home/FF/CotaGO/cert.pem', '/home/FF/CotaGO/key.pem')
    app.run(host='0.0.0.0', port=3000, ssl_context=context)