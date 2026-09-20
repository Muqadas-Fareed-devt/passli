from django.test import TestCase, Client
from django.urls import reverse

class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status_and_template(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/landing.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Passli')
        self.assertContains(response, 'Personal Document Vault')
