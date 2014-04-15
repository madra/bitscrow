"""
accounts Tests
run with "manage.py test".
"""

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from userena.tests.profiles.test import ProfileTestCase
from userena.models import UserenaSignup


class Auth(APITestCase):

    """Userena Authentication tests"""

    def test_email_data(self):
         # Setup userena permissions
        UserenaSignup.objects.check_permissions()
