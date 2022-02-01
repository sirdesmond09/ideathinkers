import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()

# Create your tests here.
class UserTestcase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="johndoe", first_name="Doe", last_name="John", password="qwertyuiop", email="desmond@test.com", phone="09049494954")

    def test_model_data(self):
        user = User.objects.all().first()
        self.assertEqual(str(user), 'johndoe')
        self.assertEqual(check_password('qwertyuiop', user.password), True)