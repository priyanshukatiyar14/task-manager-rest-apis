from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from task.models import Task


class TaskListCreateTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123',
            role='user'
        )
        
        self.admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='AdminPass123',
            role='admin'
        )
        
        self.user_task = Task.objects.create(
            user=self.user,
            title='User Task 1',
            description='Description for user task 1',
            completed=False
        )
        
        self.admin_task = Task.objects.create(
            user=self.admin,
            title='Admin Task 1',
            description='Description for admin task 1',
            completed=True
        )

    def test_list_tasks_unauthenticated(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['username'], 'testuser')

    def test_list_tasks_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 2)

    def test_create_task_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'completed': False
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.json()['data']['title'], 'New Task')
        self.assertEqual(response.json()['data']['username'], 'testuser')

    def test_create_task_without_authentication(self):
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'completed': False
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_missing_title(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'description': 'Task description',
            'completed': False
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_minimal_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Minimal Task'
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['description'], '')
        self.assertEqual(response.json()['data']['completed'], False)


class TaskDetailTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123',
            role='user'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='TestPass123',
            role='user'
        )
        
        self.admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='AdminPass123',
            role='admin'
        )
        
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            completed=False
        )
        
        self.task_detail_url = reverse('task-detail', kwargs={'pk': self.task.id})

    def test_get_task_detail_as_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['title'], 'Test Task')

    def test_get_task_detail_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_detail_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_detail_unauthenticated(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_as_owner_patch(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'completed': True
        }
        response = self.client.patch(self.task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_update_task_as_owner_put(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'completed': True
        }
        response = self.client.put(self.task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertTrue(self.task.completed)

    def test_update_task_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'completed': True
        }
        response = self.client.patch(self.task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            'completed': True
        }
        response = self.client.patch(self.task_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task_as_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.task_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_nonexistent_task(self):
        self.client.force_authenticate(user=self.user)
        import uuid
        fake_url = reverse('task-detail', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskFilterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        
        Task.objects.create(
            user=self.user,
            title='Completed Task 1',
            description='First completed task',
            completed=True
        )
        Task.objects.create(
            user=self.user,
            title='Incomplete Task 1',
            description='First incomplete task',
            completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Completed Task 2',
            description='Second completed task',
            completed=True
        )

    def test_filter_completed_tasks(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?completed=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 2)
        for task in data['results']:
            self.assertTrue(task['completed'])

    def test_filter_incomplete_tasks(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?completed=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 1)
        self.assertFalse(data['results'][0]['completed'])


class TaskSearchTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        
        Task.objects.create(
            user=self.user,
            title='Buy groceries',
            description='Milk, eggs, bread',
            completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Call dentist',
            description='Schedule appointment',
            completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Buy birthday gift',
            description='For Sarah',
            completed=False
        )

    def test_search_in_title(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?search=buy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 2)

    def test_search_in_description(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?search=appointment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 1)
        self.assertIn('dentist', data['results'][0]['title'])

    def test_search_no_results(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?search=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 0)


class TaskOrderingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        import time
        self.task1 = Task.objects.create(
            user=self.user,
            title='First Task',
            description='Created first',
            completed=False
        )
        time.sleep(0.1)
        self.task2 = Task.objects.create(
            user=self.user,
            title='Second Task',
            description='Created second',
            completed=True
        )
        time.sleep(0.1)
        self.task3 = Task.objects.create(
            user=self.user,
            title='Third Task',
            description='Created third',
            completed=False
        )

    def test_order_by_created_at_descending(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?ordering=-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']['results']
        self.assertEqual(data[0]['title'], 'Third Task')
        self.assertEqual(data[2]['title'], 'First Task')

    def test_order_by_created_at_ascending(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?ordering=created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']['results']
        self.assertEqual(data[0]['title'], 'First Task')
        self.assertEqual(data[2]['title'], 'Third Task')

    def test_order_by_completed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?ordering=completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TaskPaginationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        
        for i in range(25):
            Task.objects.create(
                user=self.user,
                title=f'Task {i+1}',
                description=f'Description {i+1}',
                completed=False
            )

    def test_default_pagination(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 25)
        self.assertEqual(len(data['results']), 10)
        self.assertIsNotNone(data['next'])
        self.assertIsNone(data['previous'])

    def test_custom_page_size(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?page_size=20')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(len(data['results']), 20)

    def test_page_size_exceeds_maximum(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?page_size=102')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_second_page(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(len(data['results']), 10)
        self.assertIsNotNone(data['previous'])

    def test_invalid_page_size(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?page_size=invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_page_size(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.task_list_url}?page_size=-5')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskCombinedFiltersTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_list_url = reverse('task-list-create')
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        
        Task.objects.create(
            user=self.user,
            title='Buy groceries',
            description='Milk and eggs',
            completed=False
        )
        Task.objects.create(
            user=self.user,
            title='Buy gifts',
            description='Birthday presents',
            completed=True
        )
        Task.objects.create(
            user=self.user,
            title='Call plumber',
            description='Fix sink',
            completed=False
        )

    def test_filter_and_search_combined(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f'{self.task_list_url}?completed=false&search=buy'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['title'], 'Buy groceries')

    def test_filter_search_and_ordering_combined(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f'{self.task_list_url}?completed=false&search=buy&ordering=-created_at&page_size=5'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_create_task(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            completed=False
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)
        self.assertFalse(task.completed)

    def test_task_string_representation(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description'
        )
        self.assertEqual(str(task), 'Test Task')

    def test_task_created_at_auto_set(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        self.assertIsNotNone(task.created_at)

    def test_task_updated_at_auto_set(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        self.assertIsNotNone(task.updated_at)

    def test_task_default_completed_false(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task'
        )
        self.assertFalse(task.completed)

    def test_task_blank_description(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description=''
        )
        self.assertEqual(task.description, '')

    def test_task_ordering(self):
        import time
        task1 = Task.objects.create(user=self.user, title='First')
        time.sleep(0.1)
        task2 = Task.objects.create(user=self.user, title='Second')
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0].title, 'Second')  # Newest first
        self.assertEqual(tasks[1].title, 'First')
