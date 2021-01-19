from django.test import TestCase

from .models import User, Tag, Article, Articletotag

class capstoneTestCase(TestCase):

    def setUp(self):

        # Test user
        self.user = User.objects.create_user(username='testuser', password='test123')
        login = self.client.login(username='testuser', password='test123')

        # Create articles
        a1 = Article.objects.create(article_by=self.user, title="TEST_TITLE1", synopsis="TEST_SYNOPSIS1", content="TEST_CONTENT1")
        a2 = Article.objects.create(article_by=self.user, title="TEST_TITLE2")

        # Create Tag
        t1= Tag.objects.create(tag_name='Art')
        t2= Tag.objects.create(tag_name='Music')
        
        # Tag Article to 'Art' tag created above
        Articletotag.objects.create(tag_obj=t1, article_obj=a1)

    def test_article_count(self):
        a1_count = Article.objects.filter(article_by=self.user).count()
        self.assertEqual(a1_count, 2)

    def test_article_tag(self):
        t1= Tag.objects.get(tag_name='Art')
        a1 = Article.objects.get(title="TEST_TITLE1")
        a2t1 = Articletotag.objects.get(article_obj=a1)
        
        self.assertEqual(t1.tag_name, a2t1.tag_obj.tag_name)
