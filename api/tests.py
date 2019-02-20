""" api/test.py """
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bucketlist, Schedule

 # Model Test - Bucketlist
class ModelBucketlistTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="wint")
        self.name = "Write world class code"
        self.bucketlist = Bucketlist(name=self.name, owner=user)

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)

# Model Test - Schedule
class ModelScheduleTestCase(TestCase):
    """This class defines the test suite for the Schedule model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.name = "Masuk sekolah pagi "
        self.day = "0"
        self.time = "0700"
        self.sound = "0"
        self.schedule = Schedule(name=self.name, day=self.day, time=self.time, sound=self.sound)

    def test_model_can_create_a_schedule(self):
        """Test the schedule model can create a schedule."""
        old_count = Schedule.objects.count()
        self.schedule.save()
        new_count = Schedule.objects.count()
        self.assertNotEqual(old_count, new_count)

 # View Test - Bucketlist
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""

        user = User.objects.create(username="wint")

        # Initialize client and force it to authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        # Since user model instance is not serializable, use its Id/PK
        self.bucketlist_data = {'name':'Go to Ibiza', 'owner':user.id}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json"
        )

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        response = new_client.get('/bucketlist/', kwargs={'pk':1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_create_a_bucketlist(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_bucketlist(self):
        """Test the api can get a given bucketlist."""
        bucketlist = Bucketlist.objects.get(id=1)
        response = self.client.get(
            reverse('details', kwargs={'pk':bucketlist.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_can_update_bucketlist(self):
        """Test the api can update a given bucketlist."""
        bucketlist = Bucketlist.objects.get()
        change_bucketlist = {'name':'something new 2'}
        res = self.client.put(
            reverse('details', kwargs={'pk':bucketlist.id}),
            change_bucketlist, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """"Test the api can delet a bucketlist."""
        bucketlist = Bucketlist.objects.get(id=1)
        response = self.client.delete(
            reverse('details', kwargs={'pk':bucketlist.id}), format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
