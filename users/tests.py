from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User, UserImage, Ticket
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


class UrlTest(APITestCase):

    def setUp(self):

        # employee_permissions = Permission.objects.filter(
        #     codename__in=['view_ticket', 'add_ticket', 'change_ticket', 'delete_ticket'])
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

    def test_superuser_can_see_users(self):
        self.__jwt_auth(self.u_super)
        r_users = self.client.get('/api/v1/users/users/', format='json')
        self.assertEqual(r_users.status_code,
                         200)

    def test_superuser_can_create_users(self):
        self.__jwt_auth(self.u_super)
        create_user_data = {
            'username': 'test_'+self.u_super.username,
            'first_name': 'test',
            'last_name': 'testian',
            'email': 'test@test.test',
            'gender': 'Male',
        }
        r_users_add = self.client.post(
            '/api/v1/users/users/', data=create_user_data, format='json')
        self.assertEqual(r_users_add.status_code,
                         201)

    def test_superuser_can_change_user(self):
        self.__jwt_auth(self.u_super)
        user = User.objects.create(username='user', password='qagsqhaydxsw')
        r_users_change = self.client.patch(
            '/api/v1/users/users/'+str(user.id)+'/', data={'username': 'test2', 'fist_name': 'test2', 'last_name': 'testian2'}, format='json')
        self.assertEqual(r_users_change.status_code,
                         200)

    def test_can_edit_profile(self):
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)

            r_edit_profile = self.client.patch(
                '/api/v1/users/EditProfile', data={'username': 'test2', 'fist_name': 'test22', 'last_name': 'testian2'}, format='json')
            self.assertEqual(r_edit_profile.status_code, 200)

    def test_can_add_and_remove_image(self):
        self.__jwt_auth(self.u_end)
        end_user = self.u_end
        image = open('files/aicon.png', 'rb')
        r_user_image_add = self.client.post(
            '/api/v1/users/usersImage/', data={'path': image})
        self.assertEqual(r_user_image_add.status_code, 201)
        r_user_image_remove = self.client.delete(
            '/api/v1/users/usersImage/'+str(r_user_image_add.data['id'])+'/')
        self.assertEqual(r_user_image_remove.status_code, 204)

    def test_cant_remove_other_user_image(self):
        # create another user
        other_user = User.objects.create(
            username='u_other', password='mmmmm46456456456')
        end_user = self.u_end

        # authenticate with other user
        self.__jwt_auth(other_user)

        # add image for u_end
        with open('files/aicon.png', 'rb') as image:
            r_user_image_add = self.client.post(
                '/api/v1/users/usersImage/', data={'path': image})

        # test other user can not remove u_end image
        self.__jwt_auth(end_user)
        r_user_image_remove = self.client.delete(
            '/api/v1/users/usersImage/'+str(r_user_image_add.data['id'])+'/')
        self.assertEqual(r_user_image_remove.status_code, 404)

        # remove created image
        self.__jwt_auth(self.u_super)
        self.client.delete(
            '/api/v1/users/usersImage/'+str(r_user_image_add.data['id'])+'/')

    def test_can_add_ticket(self):
        self.__jwt_auth(self.u_end)
        r_add_tickets = self.client.post('/api/v1/users/tickets/', data={'message_type': 'Management',
                                                                         'subject': 'test',
                                                                         'user': self.u_end.id,
                                                                         'text': 'hello world!',
                                                                         }, format='json')
        self.assertEqual(r_add_tickets.status_code, 201)

    def test_can_see_own_tickets(self):
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            r_tickets = self.client.get(
                '/api/v1/users/tickets/', format='json')
            self.assertEqual(r_tickets.status_code, 200)

    def test_can_saw_one_ticket_of_own(self):
        other_user = User.objects.create(
            username='u_other_user', password='mmmmm46456456456')
        for user in [self.u_super, self.u_employee, self.u_end]:
            self.__jwt_auth(user)
            own_ticket = Ticket.objects.create(
                subject='own_ticket', user=user, text='its my own', message_type='Support', status='Waiting')
            r_ticket_own = self.client.get(
                '/api/v1/users/tickets/'+str(own_ticket.id)+'/', format='json')
            self.assertEqual(r_ticket_own.status_code, 200)
            # create another admin user
            other_user_ticket = Ticket.objects.create(
                subject='own_ticket', user=other_user, text='its my own', message_type='Support', status='Waiting')
            r_ticket_other = self.client.get(
                '/api/v1/users/tickets/'+str(other_user_ticket.id)+'/', format='json')
            self.assertEqual(r_ticket_other.status_code, 404)

    def test_can_saw_permission(self):
        expected_statuses = [200, 403, 403]
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            sub_user = User.objects.create(
                username='u_sub'+str(idx), password='mmmmm46456456456')
            r_permission_list = self.client.get(
                '/api/v1/users/UserPermissionList/'+str(sub_user.id), format='json')
            self.assertEqual(r_permission_list.status_code,
                             expected_statuses[idx])

    def test_can_change_permission(self):
        expected_statuses = [204, 403, 403]
        for idx, user in enumerate([self.u_super, self.u_employee, self.u_end]):
            self.__jwt_auth(user)
            sub_user = User.objects.create(
                username='u_sub'+str(idx), password='mmmmm46456456456')
            r_permission_change = self.client.patch(
                '/api/v1/users/ChangeUserPermissionList/'+str(sub_user.id), data={'permission_id': [1, 2, 3, 4]}, format='json')
            self.assertEqual(r_permission_change.status_code,
                             expected_statuses[idx])

    def test_negetive_score(self):
        self.__jwt_auth(self.u_super)
        user = User.objects.create(username='user', password='qagsqhaydxsw')
        r_users_change = self.client.patch(
            '/api/v1/users/changeUserBanStatus/'+str(user.id)+'/', format='json')
        self.assertEqual(r_users_change.status_code,
                         204)
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.negetive_score, 10)
