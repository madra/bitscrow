"""
Escrowcoins Tests
run with "manage.py test".
"""

from django.utils import unittest
from utils import send_simple_message
import signals
from userena.models import UserenaSignup


class Utils(unittest.TestCase):

    """utils method tests"""

    def test_send_email(self):
    	"""Test our email sending utility"""
    	self.assertEqual(200,send_simple_message('madradavid@gmail.com',
    		'madradavid@gmail.com','Testing Email',
    		 'Here is the message.')
    	);


class Signals(unittest.TestCase):

	"""test our signals"""

	def handle_activation_complete(self):
		"""Test signal triggered when activation complete"""
		pass

	def test_custome_logout(self):
		signals.custom_logout()




