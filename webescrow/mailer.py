'''
Escrow Mailer template
'''
import smtplib

import gpg

from escrowcoins.utils import *
import escrowcoins.settings as settings

# Configure the following according to your preference and server.
SERVER = settings.SERVER_HOST
FROM = "<"+settings.ESCROW_SENDER+">"
SUBJECT = settings.ESCROW_SUBJECT
PATH = settings.BASE_URL


TEMPLATE_BASE = """You are receiving this message because someone started a bitcoin escrow
at %(fromwhere)s and indicated you to represent %(part)s
in the process.
%(msg)s
"""

TEMPLATE_BUYER = TEMPLATE_BASE % {'part': 'the buyer',
        'fromwhere': PATH, 'msg': """
To complete your part in the process, send the amount previously
combined to the address %s.

After the seller does his part you should provide the following key
in order to give access to the amount paid:

%s

Do not share this key with anyone else except with the buyer after he
has done his part (i.e. sent you some product, or any other agreement you had).
"""}



TEMPLATE_SELLER = TEMPLATE_BASE % {'part': 'the seller',
        'fromwhere': PATH, 'msg': """
The address %s was generated
for this process and it is expected that the buyer sends bitcoins to it.
Wait until the buyer sends the amount agreed, then you can proceed to do
your part.

After the buyer paid the amount agreed and you have done your part,
contact the buyer and ask for the key he received. Combine his key with
yours (shown below) using http://point-at-infinity.org/ssss/ to obtain
the private key for the address mentioned above.

Your key:

%s

Do not share this key with anyone else."""}
TEMPLATE_ESCROWER = TEMPLATE_BASE % {'part': 'the escrower',
        'fromwhere': PATH, 'msg': """
The address %s was generated
for this process and it is expected that the buyer sends bitcoins to it.

You don't need to do anything for now.

In case the buyer sends funds to the address above, but does not share his
key, you can decide to whom you should give your key. If the seller did
his part in the process, it is expected that you give the following key
to him, otherwise give it to the buyer so he can recover the bitcoins sent.

Your key:

%s

Do not share this key with anyone else."""}




def send(email, note, body, subject):
    if note:
        subject = '%s - %s' % (subject, note)
        footer = '\n\nEscrow note: %s' % note
    else:
        footer = ''
    message = """\
From: %s
To: %s
Subject: %s

%s%s
""" % (FROM, email, subject, body, footer)
    #server = smtplib.SMTP(SERVER)
    #server.sendmail(FROM, [email], message)
    #server.quit()
    return send_simple_message(email, FROM, message, subject)  



def agreeTermsEmail(email, part, escrow_link, invoice_no, note):
    ''' 
    Email for Buyer or Seller To Agree to terms
    '''
    body = TEMPLATE_BASE % {'part': part,
                'fromwhere': escrow_link, 'msg': """

For this Escrow to be Started you need to agree to the terms indicated here %s

""" % (escrow_link)}
    subject = SUBJECT+' #%s' %invoice_no
    return send(email,note, body, subject)


def sharesMail(data):
        '''
        Create Bitcoin Address and Shares
        Send Email 
        '''
        note, share, addr, part, email, use_gpg = data 
        print "Got work, sending to email %s" % email
        if part.lower() == 'escrower':
            body = TEMPLATE_ESCROWER % (addr, share)
        elif part.lower() == 'buyer':
            body = TEMPLATE_BUYER % (addr, share)
        elif part.lower() == 'seller':
            body = TEMPLATE_SELLER % (addr, share)
        else:
            body = TEMPLATE_BASE % {'part': part,
                'fromwhere': PATH, 'msg': """
The address %s was generated
for this process and it is expected that any funds are sent to it.

This is a custom n-m split and it is assumed that you know your role in
the process.

Your key:

%s
""" % (addr, share)}

        if int(use_gpg):
            body_new, err = gpg.encrypt(body, email)
            if err:
                print "GPG failed, sending in plain text: %s" % err
            else:
                body = body_new
        subject = SUBJECT        
        return send(email, note, body, subject)
