from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()


class IntegrationTests(APITestCase):

    def test_full_api_flow(self):

        # 1. Register
        register_url = reverse("register")

        register_data = {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "12345"
        }

        register_response = self.client.post(
            register_url,
            register_data
        )

        self.assertEqual(
            register_response.status_code,
            status.HTTP_201_CREATED
        )

        # 2. Login
        login_url = reverse("login")

        login_response = self.client.post(
            login_url,
            {
                "username": "admin",
                "password": "12345"
            }
        )

        self.assertEqual(
            login_response.status_code,
            status.HTTP_200_OK
        )

        # 3. Token olish
        token_url = reverse("token")

        token_response = self.client.post(
            token_url,
            {
                "username": "admin",
                "password": "12345"
            }
        )

        self.assertEqual(
            token_response.status_code,
            status.HTTP_200_OK
        )

        token = token_response.data["token"]

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token
        )

        # 4. Post yaratish
        post_url = reverse("post-list")

        create_response = self.client.post(
            post_url,
            {
                "title": "Integration Test",
                "content": "Integration Content"
            }
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED
        )

        post_id = create_response.data["id"]

        # 5. Post olish
        detail_url = reverse(
            "post-detail",
            args=[post_id]
        )

        get_response = self.client.get(detail_url)

        self.assertEqual(
            get_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            get_response.data["title"],
            "Integration Test"
        )

        # 6. Update
        update_response = self.client.put(
            detail_url,
            {
                "title": "Updated Title",
                "content": "Updated Content"
            }
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            update_response.data["title"],
            "Updated Title"
        )