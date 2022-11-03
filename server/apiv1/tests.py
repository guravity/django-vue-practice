from django.test import TestCase, Client
from apiv1.models import Category, Book

# Create your tests here.


class TestApiPosts(TestCase):
    '''本のAPIテスト'''
    # 1. fixtureを読み込む
    fixtures = ['apiv1/fixtures/test/test_api_books.json']

    def test_1(self):
        '''本一覧が取得できるか'''
        client = Client()
        response = client.get(
            # 2. urlを指定
            '/api/v1/books/',
            #   # 3. ヘッダに認証トークンを付与する
            #   HTTP_AUTHORIZATION=f"Token 7e033a902ac180e0231fced74ba58fcd658c7bbf"
        )
        self.assertEqual(200, response.status_code)
        print(response.json)
        self.assertEqual(
            [
                {
                    "id": 1,
                    "title": "1冊目の本",
                    "content": "1冊目の本感想",
                    "created_at": "2022-10-03T05:10:40.097000+09:00",
                    "updated_at": "2022-10-05T14:22:57.007000+09:00",
                    "published_at": "2011-07-25", # TODO:秒のカンマ以下6桁ゼロ埋めだと合わない
                    "categories": [
                        {
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
                            "name": "カテゴリ1",
                            "slug": "category1",
                        }
                    ]
                },
            ],
            response.json()
        )

    # def test_2(self): # カテゴリ検索機能→django-filter
    #     client = Client()
    #     response = client.get(
    #         '/api/v1/books/',
    #         {#クエリ
    #             'category'
    #         }
    #     )
