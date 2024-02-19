from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Stuff


clstuffTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_stuff = Stuff.objects.create(
            name="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_stuff.save()

    def test_things_model(self):
        stuff = Stuff.objects.get(id=1)
        actual_owner = str(stuff.owner)
        actual_name = str(stuff.name)
        actual_description = str(stuff.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_stuff_list(self):
        url = reverse("stuff_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stuff = response.data
        self.assertEqual(len(stuff), 1)
        self.assertEqual(stuff[0]["name"], "rake")

    def test_get_stuff_by_id(self):
        url = reverse("stuff_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stuff = response.data
        self.assertEqual(stuff["name"], "rake")

    def test_create_stuff(self):
        url = reverse("stuff_list")
        data = {"owner": 1, "name": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stuff = Stuff.objects.all()
        self.assertEqual(len(stuff), 2)
        self.assertEqual(Stuff.objects.get(id=2).name, "spoon")

    def test_update_stuff(self):
        url = reverse("stuff_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "rake",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stuff = Stuff.objects.get(id=1)
        self.assertEqual(stuff.name, data["name"])
        self.assertEqual(stuff.owner.id, data["owner"])
        self.assertEqual(stuff.description, data["description"])

    def test_delete_stuff(self):
        url = reverse("stuff_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        stuff = Stuff.objects.all()
        self.assertEqual(len(stuff), 0)