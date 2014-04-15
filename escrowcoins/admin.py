from django.contrib import admin
from webescrow.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    #list_display = ('Transaction',)
    exclude=('terms_agreed_date', )
    readonly_fields = ('user', 'sender', 'buyer', 'terms_agreed',
     'currency', 'condition_document', 'amount', 'expires',
     'condition_description',
     )
    title = ('decade born'),
    fields = ('user', 'sender', 
    	'buyer','currency', 'amount', 
        'condition_description', 'condition_document', 'expires',
        'is_complete'
        )
    search_fields = ['sender']
admin.site.register(Transaction, TransactionAdmin)