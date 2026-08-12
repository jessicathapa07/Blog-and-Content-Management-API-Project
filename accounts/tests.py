from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient


@override_settings(ALLOWED_HOSTS=["testserver"])
class AccountsFlowTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_register_login_profile_and_password_change_flow(self):
		register_response = self.client.post(
			"/api/accounts/register/",
			{
				"username": "accounts_user",
				"email": "accounts@example.com",
				"password": "TempPass123!",
				"password2": "TempPass123!",
			},
			format="json",
		)
		self.assertEqual(register_response.status_code, 201)

		login_response = self.client.post(
			"/api/accounts/login/",
			{
				"username": "accounts_user",
				"password": "TempPass123!",
			},
			format="json",
		)
		self.assertEqual(login_response.status_code, 200)
		self.assertIn("access", login_response.data)

		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

		profile_response = self.client.get("/api/accounts/profile/")
		self.assertEqual(profile_response.status_code, 200)
		self.assertEqual(profile_response.data["user"]["username"], "accounts_user")

		update_response = self.client.put(
			"/api/accounts/profile/",
			{
				"first_name": "Account",
				"last_name": "User",
				"bio": "Updated bio",
				"location": "Lagos",
			},
			format="json",
		)
		self.assertEqual(update_response.status_code, 200)
		self.assertEqual(update_response.data["data"]["user"]["first_name"], "Account")
		self.assertEqual(update_response.data["data"]["profile"]["bio"], "Updated bio")

		change_password_response = self.client.post(
			"/api/accounts/change-password/",
			{
				"old_password": "TempPass123!",
				"new_password": "NewPass123!",
			},
			format="json",
		)
		self.assertEqual(change_password_response.status_code, 200)

		self.client.credentials()
		relogin_response = self.client.post(
			"/api/accounts/login/",
			{
				"username": "accounts_user",
				"password": "NewPass123!",
			},
			format="json",
		)
		self.assertEqual(relogin_response.status_code, 200)

		self.assertTrue(User.objects.filter(username="accounts_user").exists())

	def test_signup_alias_uses_register_flow(self):
		signup_response = self.client.post(
			"/api/accounts/signup/",
			{
				"username": "signup_user",
				"email": "signup@example.com",
				"password": "TempPass123!",
				"password2": "TempPass123!",
			},
			format="json",
		)

		self.assertEqual(signup_response.status_code, 201)
		self.assertTrue(User.objects.filter(username="signup_user").exists())
