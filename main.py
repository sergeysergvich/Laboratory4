import unittest
import app


class FlaskTest(unittest.TestCase): # Создаем класс для тестов от unittest.TestCase.

    def test_index(self): # Тестирование доступности главной страницы.
        tester = app.app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self): # Проверяем, загружается ли страница входа.
        tester = app.app.test_client(self)
        response = tester.get('/login', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_correct_login(self): # Проверяем процесс входа с правильными учетными данными.
        tester = app.app.test_client(self)
        response = tester.post('/login', data=dict(username='testuser', password='testpass'), follow_redirects=True)
        self.assertIn(b'Welcome to the home page!', response.data) # Проверяем наличие приветствия на странице.

    def test_incorrect_login(self): # Проверяем процесс входа с неправильными учетными данными.
        tester = app.app.test_client(self)
        response = tester.post('/login', data=dict(username='wronguser', password='wrongpass'), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_home_requires_login(self): # Проверяем, что для доступа к домашней странице требуется вход в систему.
        tester = app.app.test_client(self)
        response = tester.get('/home', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_users_loaded_from_file(self): # Проверяем, правильно ли загружены пользователи из файла.
        self.assertEqual(app.users['testuser'], 'testpass')

    def test_users_saved_to_file(self): # Тестируем сохранение информации о пользователях в файл.
        app.users['newuser'] = 'newpass' # Добавляем нового пользователя.
        app.save_users()
        with open('users.txt', 'r') as f:
            lines = [x.strip() for x in f]
            self.assertIn('newuser:newpass', lines) #Проверяем, что новый пользователь сохранен.
        app.users.pop('newuser') # Возвращаем файл пользователей в исходное состояние для избежания побочных эффектов теста.
        app.save_users()


if __name__ == '__main__':
    unittest.main()