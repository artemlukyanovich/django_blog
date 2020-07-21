from django.test import TestCase

# Create your tests here.


class BlogListViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/blogs/')
        self.assertEqual(resp.status_code, 200)