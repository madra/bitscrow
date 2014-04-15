# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response,render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
import webescrow.escrowhandler as escrowhandler
import settings as settings
import os
from webescrow.forms import TransactionForm
from webescrow.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from webescrow import mailer
from userena.models import UserenaSignup
from userena.decorators import secure_required
from decorators import logged_out_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def render_view(request,template,data):
    '''
    wrapper for rendering views , loads RequestContext
    @request  request object
    @template  string
    @data  tumple
    '''
    return render_to_response(
        template,data,
        context_instance=RequestContext(request)
        )

def landing_page(request):
    '''
    handles the index page , loads homepage when user is logged in
    @request  request object
    '''	
    if request.user.is_authenticated():
        return home_page(request)
    return render_view(request,'index.html',{})

@login_required
def home_page(request):
    '''
    serves the escrow app , when the user is logged in
    @request  request object
    '''
    errors, result, notification =(' ',False,{})
    if not os.path.exists(settings.SSSS_SPLIT):
        raise Exception("%s doesn't exist, check settings.py" % settings.SSSS_SPLIT)
    if request.method == "POST":
        post_values = request.POST.copy()
        post_values['user'] = request.user.pk
        post_values['added'] = datetime.now().date()
        post_values['is_complete'] = False
        

        if not post_values['expires']:
            post_values['expires'] = datetime.now().date()
        else:
            post_values['expires'] = datetime.strptime(post_values['expires'], '%m-%d-%Y')


        if not 'encypt_emails' in post_values:
            post_values['encypt_emails'] = False
        form = TransactionForm(post_values)   
        if form.is_valid():
            transaction = form.save()
            #response = escrowhandler.post_handler(post_values, request);
            if post_values['is_sender']:
                email = post_values['buyer']
                role = 'Seller'
            else:
                email = post_values['seller']
                role = 'Buyer'
            escrow_link = settings.BASE_URL+''+transaction.get_unique_url()+'agreeterms'
            """Send an email asking the user to agree terms"""
            invoice_number = transaction.get_invoice_number()
            response = mailer.agreeTermsEmail(email,role,escrow_link,invoice_number,post_values['helptext'])
            if response:
                messages.success(request, 'The Escrow was successfully created , An email was sent to %s , once they agree to the Escrow terms you will be notified and the escrow will be marked active.'% email)
        else:
            messages.error(request, form.errors)
    now = datetime.now()        
    date_today = now.strftime("%m-%d-%Y")
    return render_view(request,'home.html',{'TransactionForm':TransactionForm,
        'escroweremail':settings.ESCROWER_EMAIL,
        'date_today ':date_today })


@login_required
def list_transactions(request):
    '''
    List transactions
    @request  request object
    '''
    if not request.user.is_authenticated:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    transactions_list = Transaction.objects.all().filter(user=request.user.pk) 
    paginator = Paginator(transactions_list , 15)
    page = request.GET.get('page')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        transactions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        transactions = paginator.page(paginator.num_pages)

    return render_view(request,'transactions.html',
        {'transactions':transactions}
        )


@login_required
def list_transaction(request,name):
    '''
    List transactions
    @request  request object
    @name string transaction hashed name
    '''
    id = int(name)^0xABCDEFAB
    transactions = get_object_or_404(Transaction.objects.filter(id=id),id=id)
    secondbar_notice = 'Buyer Escrow'
    if transactions.is_sender:
        secondbar_notice = 'Sender Escrow'
    return render_view(request,'transaction.html',
        {'transaction':transactions,'secondbar_notice':secondbar_notice},
        )


@login_required
def transaction_agree_terms(request,name):
    '''
    Agree transaction terms
    @request  request object
    @name string transaction hashed name
    '''
    id = int(name)^0xABCDEFAB
    transaction = get_object_or_404(Transaction.objects.filter(id=id),id=id)
    '''Terms have already been agreed , we relocate'''
    f04 = False
    print transaction
    if transaction.terms_agreed:
        f04 = True
    if transaction.is_sender:
        if transaction.sender == request.user.email:
            f04 = True
    else:
        if transaction.buyer == request.user.email:
            f04 = True 
    if f04:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    if request.method == "POST":
        post_values = request.POST.copy()
        if post_values['agree_terms']:
            '''user has agreed to terms ,do ahead and create shares'''
            if escrowhandler.post_handler(post_values, request):
                '''update the values to show that the user has agreed'''
                Transaction.objects.filter(id=id).update(terms_agreed=True)
                #print transaction.get_unique_url()
                #transaction.update(terms_agreed=True)
                messages.success(request, 'The Escrow was successfully created,please check your inbox to find your part of the shares')
                return redirect(transaction.get_unique_url())
        else:
            '''user has not agreed terms ,figure out what to do'''
            pass
    return render_view(request,'agree_transaction.html',
        {'transaction':transaction,
        'escroweremail':settings.ESCROWER_EMAIL},   
        )


@login_required
def transaction_complaint(request, name):
    '''
    Agree transaction terms
    @request  request object
    @name string transaction hashed name
    '''
    id = int( name )^0xABCDEFAB
    transaction = get_object_or_404(Transaction.objects.filter(id=id), id=id)
    '''File a Complaint'''
    return render_view(request,'file_complaint.html', 
        {'transaction':transaction},   
        )


@login_required
def add_complaint(request):
    '''
    Add Complaint
    @request request object()
    '''
    transactions = Transaction.objects.all().filter(user=request.user.pk) 
    return render_view(request,'complaint.html',
        {'transactions':transactions},
        )


@logged_out_required
def activate_account(request, activation_key,
             template_name='userena/activate_fail.html',
             success_url=None, extra_context=None):
    """
    Activate a user with an activation key.
    Overide userena activation 
    """
    user = UserenaSignup.objects.activate_user(activation_key)
    if user:
        '''login after activation only if specified in settings'''
        if settings.USERENA_ACTIVATION_LOGIN:
            # Sign the user in.
            auth_user = authenticate(identification=user.email,
                check_password=False)
            login(request, auth_user)
        else:
            messages.success(request, 'Your account was successfully activated , please login to continue')
            return redirect(settings.LOGIN_URL)
    else:
        messages.error(request, 'The Activation code expired')
        return redirect(settings.BASE_URL)