from django.shortcuts import reverse
from rest_framework.test import APITestCase
from articles.models import Article
from users.models import CustomUser


class ArticleTests(APITestCase):
    fixtures = ['initial_data']

    def test_create_article(self):
        self.client.login(username='menbawy', password='men@1234')
        response = self.client.post(
            reverse('article-list'), {'title': 'good', 'body': 'ggood'})
        self.assertEqual(response.status_code, 201)

    def test_create_article_missing_data(self):
        count = Article.objects.count()
        self.client.login(username='menbawy', password='men@1234')
        response = self.client.post(reverse('article-list'), {'title': 'good'})
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), count)

    def test_create_article_no_user(self):
        count = Article.objects.count()
        response = self.client.post(
            reverse('article-list'), {'title': 'good', 'body': 'ggodd'})
        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), count)

    def test_edit_article(self):
        logged = self.client.login(username='menbawy', password='men@1234')
        self.assertTrue(logged)
        self.client.post(reverse('article-update', kwargs={'pk': 12}),
                         {'title': 'good22', 'body': 'ggood'})
        self.assertEqual(Article.objects.get(id=12).title, 'good22')

    def test_edit_article_notowner(self):
        logged = self.client.login(username='menbawy', password='men@1234')
        self.assertTrue(logged)
        self.client.post(reverse('article-update', kwargs={'pk': 14}),
                         {'title': 'good22', 'body': 'ggood'})
        self.assertNotEqual(Article.objects.get(id=14).title, 'good22')


# class UserTests(APITestCase):
#     fixtures = ['initial_data']

#     def test_create_user(self):
#         count = CustomUser.objects.count()
#         logged = self.client.login(username='admin', password='admin@1234')
#         self.assertTrue(logged)
#         response = self.client.post(reverse(
#             'user-list'), {'username': 'apitester', 'email': 'api@appp.com',
#                            'password': 'api@1234'})
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(count+1, CustomUser.objects.count())
