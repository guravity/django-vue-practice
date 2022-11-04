from django.test import TestCase, Client
from apiv1.models import Category, Book
from django.utils.timezone import localtime, localdate

# Create your tests here.


class TestApiBooks(TestCase):
    '''本のAPIテスト'''

    TARGET_URL = '/api/v1/books/'
    fixtures = ['apiv1/fixtures/test/test_api_books.json']

    def test_1(self):
        '''本一覧が取得できるか'''
        client = Client()
        response = client.get(
            self.TARGET_URL,
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [
                {
                    "id": 1,
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
            ],
            response.json()
        )

    def test_2(self):
        '''カテゴリフィルタ動いているか'''
        client = Client()
        response = client.get(
            self.TARGET_URL,
            {  # クエリ
                'category': 'category1'
            }
        )
        self.assertEqual(
            [
                {
                    "id": 1,
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
            ],
            response.json()
        )

    def test_3(self):
        '''POSTメソッドで本を追加できるか'''
        client = Client()

        params = {
            'title': 'post本',
            'content': 'post感想',
            'categories': [{'id':1,}],
            "published_at": "2019-12-09",
        }

        response = client.post(
            self.TARGET_URL,
            params,
            content_type='application/json',
            format='json',
        )

        self.assertEqual(201, response.status_code)

        # DBのレコード数の確認
        self.assertEqual(Book.objects.count(), 3+1)
        # POSTメソッドで追加したレコードの取得
        book = Book.objects.get(title='post本')
        expected_json_dict = {
            'id': book.id,
            'title': 'post本',
            'content': 'post感想',
            'created_at': str(localtime(book.created_at)).replace(' ', 'T'),
            'updated_at': str(localtime(book.updated_at)).replace(' ', 'T'),
            "published_at": "2019-12-09",
            'categories': [  # TODO: postレスポンスの外部キー
                {
                    "id": 1,
                    "name": "カテゴリ1",
                    "slug": "category1",
                }
            ],
        }
        self.assertJSONEqual(response.content, expected_json_dict)