from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from api.models import Department
from api.serializers import DepartmentSerializer


class DepartmentTests(APITestCase):
    def setUp(self):
        self.url = reverse('department-list')

        self.department = Department.objects.create(name="Regional")

    def test_list_department(self):
        """
        Ensure we can list departments
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = DepartmentSerializer(instance=self.department).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data[0])

    def test_retrieve_department(self):
        """
        Ensure we can retrieve department
        """
        url = self.url + str(self.department.department_id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = DepartmentSerializer(instance=self.department).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_not_found_department(self):
        """
        Ensure we can throw an exception when not found departments
        """
        url = self.url + str(1000) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
