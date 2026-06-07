from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project, Skill

User = get_user_model()


class AdminProjectManagementAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='AdminPass123!',
            is_staff=True,
        )
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='OwnerPass123!',
            first_name='Project',
            last_name='Owner',
        )
        self.other_owner = User.objects.create_user(
            username='otherowner',
            email='other@example.com',
            password='OtherPass123!',
        )
        self.skill = Skill.objects.create(name='Django', slug='django')
        self.project = Project.objects.create(
            user=self.owner,
            title='Admin Search Project',
            description='A backend dashboard project',
            project_type='Backend',
            status='pending',
        )
        self.project.skills.add(self.skill)
        self.other_project = Project.objects.create(
            user=self.other_owner,
            title='Mobile Portfolio',
            description='A mobile showcase',
            project_type='Mobile',
            status='approved',
        )

    def test_admin_can_list_and_search_projects(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(reverse('admin-project-list'), {'search': 'django'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['slug'], self.project.slug)

    def test_non_admin_cannot_access_project_management(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(reverse('admin-project-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_activate_and_deactivate_project(self):
        self.client.force_authenticate(user=self.admin)

        activate_response = self.client.patch(
            reverse('admin-project-status', kwargs={'slug': self.project.slug}),
            {'is_active': True},
            format='json',
        )
        self.project.refresh_from_db()

        self.assertEqual(activate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project.status, 'approved')

        deactivate_response = self.client.patch(
            reverse('admin-project-status', kwargs={'slug': self.project.slug}),
            {'is_active': False},
            format='json',
        )
        self.project.refresh_from_db()

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project.status, 'rejected')

    def test_admin_can_delete_project(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(reverse('admin-project-detail', kwargs={'slug': self.project.slug}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_public_list_only_includes_approved_projects(self):
        response = self.client.get(reverse('public-project-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['slug'], self.other_project.slug)

    def test_owner_can_retrieve_own_pending_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(reverse('project-detail', kwargs={'slug': self.project.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.project.slug)
