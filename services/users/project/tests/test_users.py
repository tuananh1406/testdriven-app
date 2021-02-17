# coding: utf-8
import json
import unittest

from project import db

from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Kiểm thử cho User Service"""
    def test_users(self):
        """
        Kiểm tra ping đến hệ thống
        """
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """
        Kiểm tra chắc chắn người dùng mới có thể được
        thêm vào cơ sở dữ liệu
        """
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps({
                        'username': 'michael',
                        'email': 'michael@email.com',
                        }),
                    content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('was added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """
        Kiểm tra nếu gửi đối tượng JSON trống phải báo lỗi
        """
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps({}),
                    content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Kiểm tra nếu đối tượng JSON không có khóa username phải báo lỗi
        """
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps({'email': 'michael@email.com'}),
                    content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """
        Báo lỗi nếu email đã tồn tại
        """
        with self.client:
            self.client.post(
                    '/users',
                    data=json.dumps({
                        'username': 'michael',
                        'email': 'michael@email.com',
                        }),
                    content_type='application/json',
                )
            response = self.client.post(
                    '/users',
                    data=json.dumps({
                        'username': 'michael',
                        'email': 'michael@email.com',
                        }),
                    content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """
        Kiểm tra thử lấy thông tin 1 người dùng
        """
        user = add_user(username='michael', email='michael@email.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@email.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """
        Kiểm tra trường hợp id người dùng là chuỗi
        """
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """
        Kiểm tra trường hợp nhập id người dùng không chính xác
        """
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """
        Kiểm tra lấy thông tin nhiều người dùng
        """
        add_user('michael', 'michael@email.com')
        add_user('fletcher', 'fletcher@email.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn('michael', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn('fletcher', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """
        Kiểm tra trang chủ hiển thị đúng khi chưa thêm người dùng vào csdl
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users</p>', response.data)

    def test_main_with_users(self):
        """
        Kiểm tra hiển thị trang chủ khi có người dùng trong csdl
        """
        add_user('michael', 'michael@email.com')
        add_user('fletcher', 'fletcher@email.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users</p>', response.data)
            self.assertIn(b'michael', response.data)
            self.assertIn(b'fletcher', response.data)

    def test_main_add_user(self):
        """
        Kiểm tra thêm người dùng mới ở trang chủ
        """
        with self.client:
            response = self.client.post(
                    '/',
                    data=dict(
                        username='michael',
                        email='michael@email.com',
                    ),
                    follow_redirects=True,
                )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users</p>', response.data)
            self.assertIn(b'michael', response.data)

if __name__ == '__main__':
    unittest.main()
