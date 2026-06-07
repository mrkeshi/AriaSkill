from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from activity.models import Activity, ActivityType
from activity.services import ActivityService
from projects.models import Project

User = get_user_model()


def auth_header(user):
    refresh = RefreshToken.for_user(user)
    return {'HTTP_AUTHORIZATION': f'JWT {refresh.access_token}'}


def make_user(username='testuser', password='TestPass123!'):
    return User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password=password,
        is_active=True,
    )


def make_project(user, title='My Project', project_type='Frontend', slug=None):
    project = Project(
        user=user,
        title=title,
        project_type=project_type,
        description='A test project',
        status='approved',
    )
    if slug:
        project.slug = slug
    project.save()
    return project


def make_activity(user, activity_type=ActivityType.LOGIN_SUCCESS, is_seen=False, deleted=False):
    a = Activity.objects.create(
        user=user,
        type=activity_type,
        title='Test',
        description='Test description',
        is_seen=is_seen,
    )
    if deleted:
        a.deleted_at = timezone.now()
        a.save(update_fields=['deleted_at'])
    return a


# ─────────────────────────────────────────────
# Service-level tests
# ─────────────────────────────────────────────

class ActivityServiceTest(APITestCase):

    def setUp(self):
        self.user = make_user()

    def test_login_success_creates_activity(self):
        a = ActivityService.login_success(self.user)
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.LOGIN_SUCCESS)
        self.assertEqual(a.user, self.user)

    def test_login_failed_creates_activity(self):
        a = ActivityService.login_failed(self.user, identifier='test@example.com')
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.LOGIN_FAILED)
        self.assertEqual(a.metadata['identifier'], 'test@example.com')

    def test_password_changed_creates_activity(self):
        a = ActivityService.password_changed(self.user)
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.PASSWORD_CHANGED)

    def test_project_published_creates_activity(self):
        project = make_project(self.user)
        a = ActivityService.project_published(self.user, project)
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.PROJECT_PUBLISHED)
        self.assertEqual(a.related_project, project)

    def test_project_documentation_downloaded_creates_activity(self):
        project = make_project(self.user)
        a = ActivityService.project_documentation_downloaded(self.user, project)
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.PROJECT_DOCUMENTATION_DOWNLOADED)

    def test_external_comment_creates_activity(self):
        owner = make_user('owner')
        commenter = make_user('commenter')
        project = make_project(owner)

        # Simulate a minimal comment object
        class FakeComment:
            id = 99

        a = ActivityService.external_project_comment_created(commenter, project, FakeComment(), related_user=owner)
        self.assertIsNotNone(a)
        self.assertEqual(a.type, ActivityType.EXTERNAL_PROJECT_COMMENT_CREATED)
        self.assertEqual(a.user, commenter)

    def test_unauthenticated_user_returns_none(self):
        from django.contrib.auth.models import AnonymousUser
        result = ActivityService.login_success(AnonymousUser())
        self.assertIsNone(result)

    def test_feed_excludes_soft_deleted(self):
        make_activity(self.user)
        make_activity(self.user, deleted=True)
        qs = ActivityService.feed_for(self.user)
        self.assertEqual(qs.count(), 1)

    def test_recent_returns_at_most_6(self):
        for i in range(10):
            make_activity(self.user)
        recent = ActivityService.recent_for(self.user)
        self.assertEqual(len(recent), 6)

    def test_mark_seen_updates_flag(self):
        a = make_activity(self.user, is_seen=False)
        ActivityService.mark_seen(a, True)
        a.refresh_from_db()
        self.assertTrue(a.is_seen)

    def test_soft_delete_sets_deleted_at(self):
        a = make_activity(self.user)
        ActivityService.delete(a)
        a.refresh_from_db()
        self.assertIsNotNone(a.deleted_at)
        # Still exists in DB but excluded from feed
        self.assertEqual(ActivityService.feed_for(self.user).count(), 0)


# ─────────────────────────────────────────────
# API endpoint tests
# ─────────────────────────────────────────────

class ActivityRecentEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()
        self.other = make_user('other')

    def test_recent_returns_6_items(self):
        for _ in range(10):
            make_activity(self.user)
        response = self.client.get('/api/activities/recent/', **auth_header(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        self.assertEqual(len(data), 6)

    def test_recent_requires_auth(self):
        response = self.client.get('/api/activities/recent/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recent_does_not_include_other_users(self):
        make_activity(self.other)
        make_activity(self.user)
        response = self.client.get('/api/activities/recent/', **auth_header(self.user))
        ids_returned = [item['id'] for item in response.data['data']]
        other_ids = list(Activity.objects.filter(user=self.other).values_list('id', flat=True))
        for oid in other_ids:
            self.assertNotIn(oid, ids_returned)


class ActivityListEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()
        self.other = make_user('other2')

    def test_list_requires_auth(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_paginated(self):
        for _ in range(15):
            make_activity(self.user)
        response = self.client.get('/api/activities/', **auth_header(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['data']
        # DRF pagination wraps in count/results
        self.assertIn('results', data)
        self.assertIn('count', data)

    def test_list_excludes_soft_deleted(self):
        make_activity(self.user)
        make_activity(self.user, deleted=True)
        response = self.client.get('/api/activities/', **auth_header(self.user))
        self.assertEqual(response.data['data']['count'], 1)

    def test_filter_by_type(self):
        make_activity(self.user, activity_type=ActivityType.LOGIN_SUCCESS)
        make_activity(self.user, activity_type=ActivityType.PASSWORD_CHANGED)
        url = f'/api/activities/?type={ActivityType.LOGIN_SUCCESS}'
        response = self.client.get(url, **auth_header(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['data']['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['type'], ActivityType.LOGIN_SUCCESS)

    def test_filter_by_is_seen_false(self):
        make_activity(self.user, is_seen=False)
        make_activity(self.user, is_seen=True)
        response = self.client.get('/api/activities/?is_seen=false', **auth_header(self.user))
        results = response.data['data']['results']
        self.assertTrue(all(not r['is_seen'] for r in results))

    def test_filter_by_is_seen_true(self):
        make_activity(self.user, is_seen=False)
        make_activity(self.user, is_seen=True)
        response = self.client.get('/api/activities/?is_seen=true', **auth_header(self.user))
        results = response.data['data']['results']
        self.assertTrue(all(r['is_seen'] for r in results))

    def test_ordering_unseen_first(self):
        make_activity(self.user, is_seen=True)
        make_activity(self.user, is_seen=False)
        make_activity(self.user, is_seen=False)
        response = self.client.get('/api/activities/', **auth_header(self.user))
        results = response.data['data']['results']
        # First items should have is_seen=False
        self.assertFalse(results[0]['is_seen'])
        self.assertFalse(results[1]['is_seen'])
        self.assertTrue(results[2]['is_seen'])

    def test_user_cannot_see_others_activities(self):
        make_activity(self.other)
        response = self.client.get('/api/activities/', **auth_header(self.user))
        self.assertEqual(response.data['data']['count'], 0)


class ActivityMarkSeenEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()
        self.other = make_user('other3')

    def test_mark_seen_success(self):
        a = make_activity(self.user, is_seen=False)
        response = self.client.patch(
            f'/api/activities/{a.pk}/mark-seen/',
            {'is_seen': True},
            format='json',
            **auth_header(self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        a.refresh_from_db()
        self.assertTrue(a.is_seen)

    def test_mark_seen_defaults_to_true(self):
        a = make_activity(self.user, is_seen=False)
        response = self.client.patch(
            f'/api/activities/{a.pk}/mark-seen/',
            {},
            format='json',
            **auth_header(self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        a.refresh_from_db()
        self.assertTrue(a.is_seen)

    def test_cannot_mark_seen_other_user_activity(self):
        a = make_activity(self.other)
        response = self.client.patch(
            f'/api/activities/{a.pk}/mark-seen/',
            {'is_seen': True},
            format='json',
            **auth_header(self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ActivityDeleteEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()
        self.other = make_user('other4')

    def test_delete_soft_deletes(self):
        a = make_activity(self.user)
        response = self.client.delete(
            f'/api/activities/{a.pk}/',
            **auth_header(self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        a.refresh_from_db()
        self.assertIsNotNone(a.deleted_at)

    def test_deleted_activity_excluded_from_feed(self):
        a = make_activity(self.user)
        self.client.delete(f'/api/activities/{a.pk}/', **auth_header(self.user))
        response = self.client.get('/api/activities/', **auth_header(self.user))
        self.assertEqual(response.data['data']['count'], 0)

    def test_cannot_delete_other_user_activity(self):
        a = make_activity(self.other)
        response = self.client.delete(
            f'/api/activities/{a.pk}/',
            **auth_header(self.user),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        a.refresh_from_db()
        self.assertIsNone(a.deleted_at)


class ActivityUnseenCountEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()

    def test_unseen_count(self):
        make_activity(self.user, is_seen=False)
        make_activity(self.user, is_seen=False)
        make_activity(self.user, is_seen=True)
        response = self.client.get('/api/activities/unseen-count/', **auth_header(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['unseen_count'], 2)


class ActivityMarkAllSeenEndpointTest(APITestCase):

    def setUp(self):
        self.user = make_user()

    def test_mark_all_seen(self):
        for _ in range(5):
            make_activity(self.user, is_seen=False)
        response = self.client.patch('/api/activities/mark-all-seen/', **auth_header(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['updated'], 5)
        self.assertEqual(Activity.objects.filter(user=self.user, is_seen=False).count(), 0)
