import os
import subprocess

import escrowcoins.settings as settings


def split(secret, n, m):
    cmd = settings.SSSS_SPLIT
    proc = subprocess.Popen([cmd, "-t", str(n), "-n", str(m), "-w", "s", "-q"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate(secret)
    shares = stdout.strip().split()
    return shares

def combine(secrets, n):
    cmd = settings.SSSS_COMBINE
    secret =''
    for strn in secrets:
    	secret +='\n '+strn 
    #print secret
    proc = subprocess.Popen([cmd, "-t", str(n), "-q"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate(secret)
    shares = stdout.strip().split()
    return shares

#print combine(['s-2-e1751fe547677698abe9411028854553e7d6320d8fc409556230375e9e387d199684284bbbe59cb664642dc79125bc6a9206d3','s-3-118dfa5e47b318ffb0d2990cdd0639074c6fe445ec88f09a6100c1b4af8144dc5ff34398a519ed2d43599497f670810fa87fbe','s-1-f07c3128461bc43186a529353600c1ae1b1c48d52a11030467612c60ccf33757cd1d943e98e10e1b0d22e63738dafbc5dc8d4f'],3)