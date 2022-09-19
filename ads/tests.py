from django.test import TestCase

from rest_framework.test import APITestCase

from users.models import User

from rest_framework_simplejwt.tokens import RefreshToken

import datetime

from .models import *

from django.contrib.auth.models import Permission


class UrlTest(APITestCase):
    def setUp(self):
        self.u_super = User.objects.create(
            username='u_super', password='mmmmm46456456456', is_superuser=True)
        self.u_employee = User.objects.create(
            username='u_employee', password='mmmmm46456456456', is_staff=True)

        self.u_end = User.objects.create(
            username='u_end', password='mmmmm46456456456')

    def __jwt_auth(self, user):
        refresh_token = RefreshToken().for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(refresh_token.access_token))

    def test_can_see_own_ads(self):

        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_ads_list = self.client.get('/api/v1/ads/ads/', format='json')
            self.assertEqual(r_ads_list.status_code, 200)

    def test_can_see_own_ad(self):
        category = Category.objects.create(name='test')
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            ad = Ad.objects.create(
                title='test', user=user, price=10000, category=category)
            r_ad = self.client.get(
                '/api/v1/ads/ads/'+str(ad.id)+'/', format='json')
            self.assertEqual(r_ad.status_code, 200)

    def test_can_add_own_ad(self):
        category = Category.objects.create(name='test')
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_ad_add = self.client.post(
                '/api/v1/ads/ads/', data={'title': 'test', 'user': user.id, 'price': 10000, 'category': category.id, 'properties': []}, format='json')
            self.assertEqual(r_ad_add.status_code, 201)

    def test_can_change_own_ad(self):
        category = Category.objects.create(name='test')
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            ad = Ad.objects.create(
                title='test', user=user, price=10000, category=category)
            r_ad_change = self.client.patch(
                '/api/v1/ads/ads/'+str(ad.id)+'/', data={'title': 'test', 'user': user.id, 'price': 10000, 'properties': []}, format='json')
            self.assertEqual(r_ad_change.status_code, 200)

    def test_can_remove_own_ad(self):
        category = Category.objects.create(name='test')
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            ad = Ad.objects.create(
                title='test', user=user, price=10000, category=category)
            r_ad_remove = self.client.delete(
                '/api/v1/ads/ads/'+str(ad.id)+'/', format='json')
            self.assertEqual(r_ad_remove.status_code, 204)

    def test_can_see_categories(self):
        expected_status = [200, 200, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_category', 'add_category', 'change_category', 'delete_category'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_categories_list = self.client.get(
                '/api/v1/ads/adminCategories/', format='json')
            self.assertEqual(r_categories_list.status_code,
                             expected_status[idx])

    def test_can_see_single_category(self):
        category = Category.objects.create(name='test')
        expected_status = [200, 200, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_category', 'add_category', 'change_category', 'delete_category'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_category = self.client.get(
                '/api/v1/ads/adminCategories/'+str(category.id)+'/', format='json')
            self.assertEqual(r_category.status_code, expected_status[idx])

    def test_can_add_category(self):
        expected_status = [201, 201, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_category', 'add_category', 'change_category', 'delete_category'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_category_add = self.client.post(
                '/api/v1/ads/adminCategories/', data={'name': 'test'}, format='json')
            self.assertEqual(r_category_add.status_code, expected_status[idx])

    def test_can_change_category(self):
        category = Category.objects.create(name='test')
        expected_status = [200, 200, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_category', 'add_category', 'change_category', 'delete_category'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_category_change = self.client.patch(
                '/api/v1/ads/adminCategories/'+str(category.id)+'/', data={'name': 'test2'}, format='json')
            self.assertEqual(r_category_change.status_code,
                             expected_status[idx])

    def test_can_remove_category(self):
        expected_status = [204, 204, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_category', 'add_category', 'change_category', 'delete_category'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            category = Category.objects.create(name='test')
            r_category_remove = self.client.delete(
                '/api/v1/ads/adminCategories/'+str(category.id)+'/',  format='json')
            self.assertEqual(r_category_remove.status_code,
                             expected_status[idx])

    def test_can_see_ads(self):
        expected_status = [200, 200, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_ad', 'add_ad', 'change_ad', 'delete_ad'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_ads_list = self.client.get(
                '/api/v1/ads/adminAds/', format='json')
            self.assertEqual(r_ads_list.status_code, expected_status[idx])

    def test_can_see_single_ad(self):
        expected_status = [200, 200, 403]
        category = Category.objects.create(name='test')
        other_user = User.objects.create(username='other', password="12345678")
        ad = Ad.objects.create(
            title='test', user=other_user, price=10000, category=category)
        employee_permissions = Permission.objects.filter(
            codename__in=['view_ad', 'add_ad', 'change_ad', 'delete_ad'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_ad = self.client.get(
                '/api/v1/ads/adminAds/'+str(ad.id)+'/', format='json')
            self.assertEqual(r_ad.status_code, expected_status[idx])

    def test_can_change_ad(self):
        expected_status = [200, 200, 403]
        category = Category.objects.create(name='test')
        employee_permissions = Permission.objects.filter(
            codename__in=['view_ad', 'add_ad', 'change_ad', 'delete_ad'])
        self.u_employee.user_permissions.set(employee_permissions)
        other_user = User.objects.create(username='other', password="12345678")
        ad = Ad.objects.create(
            title='test', user=other_user, price=10000, category=category)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)

            r_ad_change = self.client.patch(
                '/api/v1/ads/adminAds/'+str(ad.id)+'/', data={'title': 'test', 'user': user.id, 'price': 10000, 'properties': []}, format='json')
            self.assertEqual(r_ad_change.status_code, expected_status[idx])

    def test_can_remove_ad(self):
        expected_status = [204, 204, 403]
        category = Category.objects.create(name='test')
        employee_permissions = Permission.objects.filter(
            codename__in=['view_ad', 'add_ad', 'change_ad', 'delete_ad'])
        self.u_employee.user_permissions.set(employee_permissions)
        other_user = User.objects.create(username='other', password="12345678")

        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            ad = Ad.objects.create(
                title='test', user=other_user, price=10000, category=category)
            r_ad_remove = self.client.delete(
                '/api/v1/ads/adminAds/'+str(ad.id)+'/', format='json')
            self.assertEqual(r_ad_remove.status_code, expected_status[idx])

    def test_can_see_properties(self):
        expected_status = [200, 200, 403]
        employee_permissions = Permission.objects.filter(
            codename__in=['view_property', 'add_property', 'change_property', 'delete_property'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_properties_list = self.client.get(
                '/api/v1/ads/adminProperties/', format='json')
            self.assertEqual(r_properties_list.status_code,
                             expected_status[idx])

    def test_can_see_single_property(self):
        expected_status = [200, 200, 403]
        category = Category.objects.create(name='test')
        prop = Property.objects.create(
            name='test', category=category)
        employee_permissions = Permission.objects.filter(
            codename__in=['view_property', 'add_property', 'change_property', 'delete_property'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_property = self.client.get(
                '/api/v1/ads/adminProperties/'+str(prop.id)+'/', format='json')
            self.assertEqual(r_property.status_code, expected_status[idx])

    def test_can_add_property(self):
        expected_status = [201, 201, 403]
        category = Category.objects.create(name='test')
        employee_permissions = Permission.objects.filter(
            codename__in=['view_property', 'add_property', 'change_property', 'delete_property'])
        self.u_employee.user_permissions.set(employee_permissions)
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            r_property_add = self.client.post(
                '/api/v1/ads/adminProperties/', data={'name': 'test', 'category': category.id}, format='json')
            self.assertEqual(r_property_add.status_code, expected_status[idx])

    def test_can_change_property(self):
        expected_status = [200, 200, 403]
        category = Category.objects.create(name='test')
        prop = Property.objects.create(
            name='test', category=category)
        employee_permissions = Permission.objects.filter(
            codename__in=['view_property', 'add_property', 'change_property', 'delete_property'])
        self.u_employee.user_permissions.set(employee_permissions)
        other_user = User.objects.create(username='other', password="12345678")

        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)

            r_property_change = self.client.patch(
                '/api/v1/ads/adminProperties/'+str(prop.id)+'/', data={'title': 'test', 'properties': []}, format='json')
            self.assertEqual(r_property_change.status_code,
                             expected_status[idx])

    def test_can_remove_property(self):
        expected_status = [204, 204, 403]
        category = Category.objects.create(name='test')

        employee_permissions = Permission.objects.filter(
            codename__in=['view_property', 'add_property', 'change_property', 'delete_property'])
        self.u_employee.user_permissions.set(employee_permissions)
        other_user = User.objects.create(username='other', password="12345678")

        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            prop = Property.objects.create(
                name='test', category=category)
            r_property_remove = self.client.delete(
                '/api/v1/ads/adminProperties/'+str(prop.id)+'/', format='json')
            self.assertEqual(r_property_remove.status_code,
                             expected_status[idx])
