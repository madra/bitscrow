from userena.signals import activation_complete
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.dispatch import receiver
import settings

@receiver(activation_complete)
def handle_activation_complete(sender, **kwargs):
	'''logout when a user has just activated there acount'''
	user = kwargs.get("user")
	user = User.objects.get(pk=user.id)

def custom_logout():
	request = {}
	request['next_page'] = settings.LOGIN_URL
	logout(request);
	


