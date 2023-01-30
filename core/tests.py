from django.test import TestCase
from rest_framework.test import APIClient
from .models import Blog
from .serializers import BlogSerializer


class BlogViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.blog = Blog.objects.create(
            title={'en': 'English title', 'fr': 'Titre français'},
            content='Blog content'
        )

    def test_create_blog(self):
        data = {
            'title_en': 'Another English title',
            'title_fr': 'Un autre titre français',
            'content': 'Another blog content',
        }
        response = self.client.post('/blogs/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blog.objects.count(), 2)

    def test_retrieve_blog(self):
        response = self.client.get(f'/blogs/{self.blog.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'title_en': 'English title',
            'title_fr': 'Titre français',
            'content': 'Blog content',
        })

    def test_update_blog(self):
        data = {
            'title_en': 'Updated English title',
            'title_fr': 'Titre français mis à jour',
            'content': 'Updated blog content',
        }
        response = self.client.put(f'/blogs/{self.blog.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, {
            'en': 'Updated English title',
            'fr': 'Titre français mis à jour',
        })
        self.assertEqual(self.blog.content, 'Updated blog content')

    def test_delete_blog(self):
        response = self.client.delete(f'/blogs/{self.blog.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Blog.objects.count(), 0)
