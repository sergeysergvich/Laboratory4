from flask import Flask, request, render_template, redirect
from flask import session
import os

app = Flask(__name__) # Создаем экземпляр приложения Flask
# Генерируем и устанавливаем секретный ключ для безопасной передачи сессий
app.config['SECRET_KEY'] = os.urandom(20).hex()

users = {} # Инициализируем словарь для хранения пользователей

# Загрузка пользователей из файла
with open('users.txt', 'r') as f:
    for line in f:
        username, password = line.strip().split(':')
        users[username] = password

@app.route('/') # Определение маршрута для главной страницы
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST']) # Определение маршрута для страницы входа в систему
def login():
    if session.get('logged', False): # Проверяем, авторизован ли уже пользователь
        return redirect('/home')

    try: # Получаем имя пользователя и пароль из формы входа
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        return redirect('/')

    if username in users and users[username] == password: # Проверяем, существует ли пользователь и верен ли пароль
        session['logged'] = True
        session.modified = True
        return redirect('/home')
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/home') # Определение маршрута для главной страницы после входа
def home():
    if not session.get('logged', False): # Проверяем, авторизован ли пользователь
        return redirect('/')
    return 'Welcome to the home page!'

# Сохранение пользователей в файл
def save_users():
    with open('users.txt', 'w') as f:
        for username, password in users.items():
            f.write(f'{username}:{password}\n')

if __name__ == '__main__':
    app.run(debug=True)