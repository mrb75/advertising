from rest_framework.test import APITestCase
from ads.models import Ad, Category, Message
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UrlTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password="12345678")
        self.other_user = User.objects.create(
            username='other', password="12345678")

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))

    def test_can_read_ads(self):
        r_ads = self.client.get('/api/v1/website/ads/', format='json')
        self.assertEqual(r_ads.status_code, 200)

    def test_can_filter_ads(self):
        category = Category.objects.create(name="test")
        ad1 = Ad.objects.create(
            title="test1", category=category, user=self.user, price=1000)
        ad2 = Ad.objects.create(
            title="test2", category=category, user=self.user, price=2000)
        r_ads = self.client.get(
            '/api/v1/website/ads/?price__lte=1200', format='json')
        self.assertEqual(r_ads.status_code, 200)

    def test_can_see_single_ad(self):
        category = Category.objects.create(name="test")
        ad = Ad.objects.create(
            title="test", category=category, user=self.user, price=2000, is_verified=True)
        r_ad = self.client.get(
            '/api/v1/website/ads/'+str(ad.id)+'/', format='json')
        self.assertEqual(r_ad.status_code, 200)

    def test_can_see_categories(self):
        r_categories = self.client.get(
            '/api/v1/website/categories/', format='json')
        self.assertEqual(r_categories.status_code, 200)

    def test_can_see_single_category(self):
        category = Category.objects.create(name="test")
        r_category = self.client.get(
            '/api/v1/website/categories/'+str(category.id)+'/', format='json')
        self.assertEqual(r_category.status_code, 200)

    def test_can_see_messages(self):
        self.__jwt_auth(self.user)
        r_messages = self.client.get(
            '/api/v1/website/messages/', format='json')
        self.assertEqual(r_messages.status_code, 200)

    def test_can_see_single_message(self):
        self.__jwt_auth(self.user)
        category = Category.objects.create(name="test")
        ad = Ad.objects.create(
            title="test", category=category, user=self.other_user, price=2000)
        message = Message.objects.create(
            sender=self.user, ad=ad, text="hello are you test?", user=self.other_user)
        r_messages = self.client.get(
            '/api/v1/website/messages/'+str(message.id)+'/', format='json')
        self.assertEqual(r_messages.status_code, 200)

    def test_can_send_message(self):
        self.__jwt_auth(self.user)
        category = Category.objects.create(name="test")
        ad = Ad.objects.create(
            title="test", category=category, user=self.other_user, price=2000)
        r_message_send = self.client.post(
            '/api/v1/website/messagesOperations/', data={'ad': ad.id, 'text': 'test text.', 'user': self.other_user.id}, format='json')
        self.assertEqual(r_message_send.status_code, 201)

    def test_can_edit_message(self):
        self.__jwt_auth(self.user)
        category = Category.objects.create(name="test")
        ad = Ad.objects.create(
            title="test", category=category, user=self.other_user, price=2000)
        message = Message.objects.create(
            sender=self.user, ad=ad, text="hello are you test?", user=self.other_user)
        r_message_change = self.client.patch(
            '/api/v1/website/messagesOperations/'+str(message.id)+'/', data={'ad': ad.id, 'text': 'test text.'}, format='json')
        self.assertEqual(r_message_change.status_code, 200)

    def test_can_remove_message(self):
        self.__jwt_auth(self.user)
        category = Category.objects.create(name="test")
        ad = Ad.objects.create(
            title="test", category=category, user=self.other_user, price=2000)
        message = Message.objects.create(
            sender=self.user, ad=ad, text="hello are you test?", user=self.other_user)
        r_message_change = self.client.delete(
            '/api/v1/website/messagesOperations/'+str(message.id)+'/', format='json')
        self.assertEqual(r_message_change.status_code, 204)
