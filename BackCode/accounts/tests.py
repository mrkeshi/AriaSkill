from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test-password',
            first_name='Test',
            last_name='User',
            job_title='Backend Developer',
            about_me='I build APIs.',
            instagram_link='https://instagram.com/testuser',
            telegram_link='https://t.me/testuser',
            discord_link='https://discord.gg/testuser',
            linkedin_link='https://linkedin.com/in/testuser',
        )
        self.client.force_authenticate(user=self.user)

    def test_profile_response_includes_social_links(self):
        response = self.client.get(reverse('fetch_user'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_title'], 'Backend Developer')
        self.assertEqual(response.data['about_me'], 'I build APIs.')
        self.assertEqual(response.data['instagram_link'], 'https://instagram.com/testuser')
        self.assertEqual(response.data['telegram_link'], 'https://t.me/testuser')
        self.assertEqual(response.data['discord_link'], 'https://discord.gg/testuser')
        self.assertEqual(response.data['linkedin_link'], 'https://linkedin.com/in/testuser')

    def test_user_can_edit_own_profile(self):
        response = self.client.patch(reverse('edit_user_profile'), {
            'first_name': 'Updated',
            'job_title': 'API Engineer',
            'about_me': 'Updated profile text.',
            'instagram_link': 'https://instagram.com/updated',
            'telegram_link': 'https://t.me/updated',
            'discord_link': 'https://discord.gg/updated',
            'linkedin_link': 'https://linkedin.com/in/updated',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.job_title, 'API Engineer')
        self.assertEqual(self.user.about_me, 'Updated profile text.')
        self.assertEqual(self.user.instagram_link, 'https://instagram.com/updated')
        self.assertEqual(self.user.telegram_link, 'https://t.me/updated')
        self.assertEqual(self.user.discord_link, 'https://discord.gg/updated')
        self.assertEqual(self.user.linkedin_link, 'https://linkedin.com/in/updated')


class AdminUserManagementAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='MemberPass123!',
            first_name='Regular',
            last_name='Member',
        )
        self.other_user = User.objects.create_user(
            username='betauser',
            email='beta@example.com',
            password='BetaPass123!',
            first_name='Beta',
            last_name='Tester',
        )

    def test_admin_can_list_and_search_users(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('admin_user_list'), {'search': 'beta'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['email'], 'beta@example.com')

    def test_non_admin_cannot_access_user_management(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('admin_user_list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_deactivate_and_activate_user(self):
        self.client.force_authenticate(user=self.admin)

        deactivate_response = self.client.patch(
            reverse('admin_user_status', kwargs={'pk': self.user.pk}),
            {'is_active': False},
            format='json',
        )
        self.user.refresh_from_db()

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.is_active)

        activate_response = self.client.patch(
            reverse('admin_user_status', kwargs={'pk': self.user.pk}),
            {'is_active': True},
            format='json',
        )
        self.user.refresh_from_db()

        self.assertEqual(activate_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)

    def test_admin_cannot_deactivate_or_delete_own_account(self):
        self.client.force_authenticate(user=self.admin)

        deactivate_response = self.client.patch(
            reverse('admin_user_status', kwargs={'pk': self.admin.pk}),
            {'is_active': False},
            format='json',
        )
        delete_response = self.client.delete(reverse('admin_user_detail', kwargs={'pk': self.admin.pk}))

        self.admin.refresh_from_db()
        self.assertEqual(deactivate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(delete_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.admin.is_active)

    def test_admin_can_change_user_password(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            reverse('admin_user_password', kwargs={'pk': self.user.pk}),
            {
                'password': 'NewMemberPass123!',
                'password_confirm': 'NewMemberPass123!',
            },
            format='json',
        )

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('NewMemberPass123!'))

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(reverse('admin_user_detail', kwargs={'pk': self.user.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
