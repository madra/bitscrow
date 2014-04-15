EscrowCoins
=============================
Secure Bitcoin and LiteCoin Escrow Service Written in Django
Builtin MailGun and Analytics Support

Requirements for Webescrow app
==============================

Requirements
============

Python 2.7 (http://python.org),
python-ecdsa (https://github.com/warner/python-ecdsa)
ssss (http://point-at-infinity.org/ssss/),
Django (https://www.djangoproject.com/),
OpenSSL (https://www.openssl.org/),
pyOpenSSL (https://launchpad.net/pyopenssl),
GPG (http://gnupg.org/),
and a SMTP server properly configured.

Setup
=====
Add `local_settings.py` to hold your local settings
configurations. Make sure the program `ssss-split` is found at
the place specified by `ssss_split` at `settings.py`.
