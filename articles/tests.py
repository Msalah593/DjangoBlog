from django.test import TestCase
from django.urls import reverse
from .models import Article
from django.db.models import Q
from users.models import CustomUser

class TestArticleUpdateView(TestCase):
    fixtures=['initial_data']
    def test_update_article_pass(self):
        self.client.login(username='menbawy',password='men@1234')
        url=reverse('article-update',kwargs={'pk':14})
        response=self.client.post(url,
                                    {'title':'good','body':'good'})
        self.assertNotEqual(Article.objects.get(id=14).title,'good')
    def test_update_article_fail(self):
        self.client.login(username='menbawy',password='men@1234')
        url=reverse('article-update',kwargs={'pk':12})
        response=self.client.post(url,
                                    {'title':'good','body':'good'})
        self.assertEqual(Article.objects.get(id=12).title,'good')
class TestArticleListView(TestCase):
    fixtures=['initial_data']
    def test_search(self):
        url = "%s?q=test" % reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.context['articles'].count(),5)
class TestArticleCreateView(TestCase):
    fixtures=['initial_data']
    def test_create(self):
        self.client.login(username='admin',password='admin@1234')
        count=Article.objects.count()
        response=self.client.post(reverse('createarticle'),
            {'title': 'good to see you', 'body' : 'thank you' })
        self.assertEqual(Article.objects.count(),count+1)
        self.assertEqual(response.status_code,302)    
class TestSmokeTests(TestCase):
    fixtures=['initial_data']
    def test_home(self):
        url=reverse('home')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
    def test_create_article(self):
        url=reverse('createarticle')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
    def test_article_detial(self):
        url=reverse('article-detail',kwargs={'id':12})
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        url=reverse('article-detail',kwargs={'id':0})
        response=self.client.get(url)
        self.assertEqual(response.status_code,404)
    def test_update_article(self):
        url=reverse('article-update',kwargs={'pk':12})
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        url=reverse('article-update',kwargs={'pk':0})
        response=self.client.get(url)
        self.assertEqual(response.status_code,404)
    def test_user_article_list(self):
        url=reverse('user-articles',args=('menbawy',))
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        url=reverse('user-articles',args=('nouser',))
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)