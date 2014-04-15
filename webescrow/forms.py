from django.forms import ModelForm
from models import Transaction


class TransactionForm(ModelForm):
	"""Form for the escrow transaction"""
	
	class Meta:
		model = Transaction
		#fields = ['sender','buyer','escrower']