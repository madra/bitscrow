from django.db import models
from datetime import datetime
#for user
from django.contrib.auth.models import User
from decimal import Decimal


# Transaction Model
class Transaction(models.Model):
    '''
    Transaction Model
    '''

    user = models.ForeignKey(User)
    sender = models.EmailField(max_length=70, blank=False)
    buyer = models.EmailField(max_length=70, blank=False)
    escrower = models.EmailField(max_length=70, blank=False)
    added = models.DateTimeField(default=datetime.now)
    expires = models.DateTimeField(null=True, blank=True)
    is_sender = models.BooleanField(default=True)
    amount = models.IntegerField(blank=False)
    helptext = models.TextField(blank=True)
    condition_description = models.TextField()
    condition_document = models.BooleanField(default=False, verbose_name = "Requires Document")
    is_complete = models.BooleanField(default=False, verbose_name = "Is Complete")
    terms_agreed = models.BooleanField(default=False)
    terms_agreed_date = models.DateTimeField(null=True, blank=True)
    CURRENCY_CHOICES = (
        ('BTC', 'Bitcoin'),
        ('LTC', 'Litecoin'),
    )
    currency = models.CharField(max_length=15, choices=CURRENCY_CHOICES, default=True, blank=True)

    def get_invoice_number(self):
        '''
        invoice number
        '''
        return str(self.pk^0xABCDEFAB)

    @models.permalink
    def get_unique_url(self):
        '''
        direct link to transaction
        '''
        return('transaction', [ str(self.pk^0xABCDEFAB) ])

    def get_status(self):
        '''
        get the status of the transaction
        '''
        if self.is_complete:
            return "Is complete"
        else:
            return "In progress"

    def __unicode__(self):
        return self.get_invoice_number()


#for storing money
class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        try:
           return super(CurrencyField, 
            self).to_python(
            value).quantize(Decimal("0.01")
            )
        except AttributeError:
           return None


class Complaint(models.Model):
    """
    Model for when a user files a complaint
    """
    SECTION_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=datetime.now)
    resolved = models.DateTimeField(null=True, blank=True)
    text = models.TextField(blank=True)

        