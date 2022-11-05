from django.test import TestCase, Client
from apiv1.models import Category, Book
from django.utils.timezone import localtime, localdate


class TestBookApiBooks(TestCase):
    '''本のAPIテスト'''

    AUTH_URL = '/api/v1/api-token-auth/'
    TARGET_URL = '/api/v1/books/'
    fixtures = ['apiv1/fixtures/test/test_api_books.json']

    def test_1(self):
        '''GET 本一覧が取得できるか'''
        client = Client()
        response = client.get(
            self.TARGET_URL,
        )
        expected_json_dict_list = [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "username": 'testuser',
                    "email": "testuser@test.com",
                },
                "title": "1冊目の本",
                "content": "1冊目の本感想",
                "created_at": "2022-10-03T05:10:40.097000+09:00",
                "updated_at": "2022-10-05T14:22:57.007000+09:00",
                "published_at": "2011-07-25",
                "categories": [
                    {
                        "id": 1,
                        "name": "カテゴリ1",
                        "slug": "category1",
                    }
                ]
            },
            {
                "id": 2,
                "user": {
                    "id": 1,
                    "username": 'testuser',
                    "email": "testuser@test.com",
                },
                "title": "2冊目の本",
                "content": "2冊目の本感想",
                "created_at": "2022-10-12T05:10:40.097000+09:00",
                "updated_at": "2022-11-03T14:12:57.007000+09:00",
                "published_at": "2020-04-10",
                "categories": [
                    {
                        "id": 2,
                        "name": "カテゴリ2",
                        "slug": "category2",
                    }
                ]
            },
            {
                "id": 3,
                "user": {
                    "id": 1,
                    "username": 'testuser',
                    "email": "testuser@test.com",
                },
                "title": "3冊目の本",
                "content": "3冊目の本感想",
                "created_at": "2022-10-19T05:10:40.097000+09:00",
                "updated_at": "2022-10-30T14:16:57.007000+09:00",
                "published_at": "2010-11-18",
                "categories": [
                    {
                        "id": 1,
                        "name": "カテゴリ1",
                        "slug": "category1",
                    }
                ]
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json_dict_list)

    def test_2(self):
        '''GET カテゴリフィルタ動いているか'''
        client = Client()
        response = client.get(
            self.TARGET_URL,
            {  # クエリ
                'category': 'category1'
            }
        )
        expected_json_dict_list = [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "username": 'testuser',
                    "email": "testuser@test.com",
                },
                "title": "1冊目の本",
                "content": "1冊目の本感想",
                "created_at": "2022-10-03T05:10:40.097000+09:00",
                "updated_at": "2022-10-05T14:22:57.007000+09:00",
                "published_at": "2011-07-25",
                "categories": [
                    {
                        "id": 1,
                        "name": "カテゴリ1",
                        "slug": "category1",
                    }
                ]
            },
            {
                "id": 3,
                "user": {
                    "id": 1,
                    "username": 'testuser',
                    "email": "testuser@test.com",
                },
                "title": "3冊目の本",
                "content": "3冊目の本感想",
                "created_at": "2022-10-19T05:10:40.097000+09:00",
                "updated_at": "2022-10-30T14:16:57.007000+09:00",
                "published_at": "2010-11-18",
                "categories": [
                    {
                        "id": 1,
                        "name": "カテゴリ1",
                        "slug": "category1",
                    }
                ]
            },
        ]
        self.assertEqual(response.json(), expected_json_dict_list)

    def test_3(self):
        '''GET idで本の取得ができるか'''
        client = Client()
        response = client.get(self.TARGET_URL+'1/')
        expected_json_dict = {
            "id": 1,
            "user": {
                "id": 1,
                "username": 'testuser',
                "email": "testuser@test.com",
            },
            "title": "1冊目の本",
            "content": "1冊目の本感想",
            "created_at": "2022-10-03T05:10:40.097000+09:00",
            "updated_at": "2022-10-05T14:22:57.007000+09:00",
            "published_at": "2011-07-25",
            "categories": [
                {
                    "id": 1,
                    "name": "カテゴリ1",
                    "slug": "category1",
                }
            ],
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_4(self):
        '''POST 本を追加できるか'''
        client = Client()

        # トークン取得
        token_response = client.post(
            self.AUTH_URL,
            data={
                "username": "testuser",
                "password": "password",
                "email": "testuser@test.com",
            },
            content_type='application/json',
        )
        # トークン認証のチェック
        self.assertEqual(token_response.status_code, 200)
        self.assertTrue('token' in token_response.json())
        token = token_response.json()['token']

        params = {
            'title': 'post本',
            'content': 'post感想',
            'category_ids': [1],
            "published_at": "2019-12-09",
        }

        response = client.post(
            self.TARGET_URL,
            params,
            content_type='application/json',
            format='json',
            HTTP_AUTHORIZATION=f"Token {token}"
        )
        # ステータスコードの確認
        self.assertEqual(response.status_code, 201)
        # DBのレコード数の確認
        self.assertEqual(Book.objects.count(), 3+1)

        # 追加したレコードの取得
        book = Book.objects.get(title='post本')
        expected_json_dict = {
            'id': book.id,
            'user': {
                "id": 1,
                "username": "testuser",
                "email": "testuser@test.com",
            },
            'title': 'post本',
            'content': 'post感想',
            'created_at': str(localtime(book.created_at)).replace(' ', 'T'),
            'updated_at': str(localtime(book.updated_at)).replace(' ', 'T'),
            "published_at": "2019-12-09",
            'categories': [
                {
                    "id": 1,
                    "name": "カテゴリ1",
                    "slug": "category1",
                }
            ],
        }
        # レスポンスの中身の確認(JSON)
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_5(self):
        '''PUT 本の情報を更新(全部)できるか'''
        client = Client()
        # トークン取得
        token_response = client.post(
            self.AUTH_URL,
            data={
                "username": "testuser",
                "password": "password",
                "email": "testuser@test.com",
            },
            content_type='application/json',
        )
        # トークン認証のチェック
        self.assertEqual(token_response.status_code, 200)
        self.assertTrue('token' in token_response.json())
        token = token_response.json()['token']

        params = {
            'title': 'put本',
            'content': 'put感想',
            'category_ids': [2],
            "published_at": "2011-07-26",
        }
        response = client.put(
            self.TARGET_URL+'1/',
            params,
            content_type='application/json',
            format='json',
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # DBのレコード数の確認
        self.assertEqual(Book.objects.count(), 3)
        # 変更したレコードの取得
        book = Book.objects.get(id=1)
        expected_json_dict = {
            "id": 1,
            'user': {
                "id": 1,
                "username": "testuser",
                "email": "testuser@test.com",
            },
            "title": "put本",
            "content": "put感想",
            "created_at": "2022-10-03T05:10:40.097000+09:00",
            "updated_at": str(localtime(book.updated_at)).replace(' ', 'T'),
            "published_at": "2011-07-26",
            "categories": [
                {
                    "id": 2,
                    "name": "カテゴリ2",
                    "slug": "category2",
                }
            ]
        }
        # レスポンスの中身の確認(JSON)
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_6(self):
        '''PUT レコードがない場合に404が返ってくるか'''
        client = Client()
        # トークン取得
        token_response = client.post(
            self.AUTH_URL,
            data={
                "username": "testuser",
                "password": "password",
                "email": "testuser@test.com",
            },
            content_type='application/json',
        )
        # トークン認証のチェック
        self.assertEqual(token_response.status_code, 200)
        self.assertTrue('token' in token_response.json())
        token = token_response.json()['token']

        params = {
            'title': 'put本',
            'content': 'put感想',
            'category_ids': [2],
            "published_at": "2011-07-26",
        }
        response = client.put(
            self.TARGET_URL+'4/',
            params,
            content_type='application/json',
            format='json',
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        # ステータスコードの確認
        self.assertEqual(response.status_code, 404)

    def test_7(self):
        '''PATCH 本の情報を更新(一部)できるか'''
        client = Client()
        # トークン取得
        token_response = client.post(
            self.AUTH_URL,
            data={
                "username": "testuser",
                "password": "password",
                "email": "testuser@test.com",
            },
            content_type='application/json',
        )
        # トークン認証のチェック
        self.assertEqual(token_response.status_code, 200)
        self.assertTrue('token' in token_response.json())
        token = token_response.json()['token']

        params = {
            'title': 'patch本',
            'category_ids': [1, 2],
        }
        response = client.patch(
            self.TARGET_URL+'1/',
            params,
            content_type='application/json',
            format='json',
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)
        # DBのレコード数の確認
        self.assertEqual(Book.objects.count(), 3)
        # 変更したレコードの取得
        book = Book.objects.get(id=1)
        expected_json_dict = {
            "id": 1,
            'user': {
                "id": 1,
                "username": "testuser",
                "email": "testuser@test.com",
            },
            "title": "patch本",
            "content": "1冊目の本感想",
            "created_at": "2022-10-03T05:10:40.097000+09:00",
            "updated_at": str(localtime(book.updated_at)).replace(' ', 'T'),
            "published_at": "2011-07-25",
            "categories": [
                {
                    "id": 1,
                    "name": "カテゴリ1",
                    "slug": "category1",
                },
                {
                    "id": 2,
                    "name": "カテゴリ2",
                    "slug": "category2",
                }
            ]
        }
        # レスポンスの中身の確認(JSON)
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_8(self):
        """DELETE 本を削除できるか"""
        client = Client()
        # トークン取得
        token_response = client.post(
            self.AUTH_URL,
            data={
                "username": "testuser",
                "password": "password",
                "email": "testuser@test.com",
            },
            content_type='application/json',
        )
        # トークン認証のチェック
        self.assertEqual(token_response.status_code, 200)
        self.assertTrue('token' in token_response.json())
        token = token_response.json()['token']

        response = client.delete(
            self.TARGET_URL+'1/',
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        # ステータスコードの確認
        self.assertEqual(response.status_code, 204)
        # DBのレコード数の確認
        self.assertEqual(Book.objects.count(), 2)
        # レスポンスの中身の確認(空)
        self.assertEqual(response.content, b'')

# TODO: Category APIのテスト
# TODO: 認証周りのテスト
# client.login(username="testuser", password="password")
# Tokenのテスト
