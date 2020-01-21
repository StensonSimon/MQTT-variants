from MQTTSNclient import Client
import struct
import time
import sys
import socket
from mbedtls import tls
import datetime as dt
from mbedtls import hash as hashlib
from mbedtls import pk
from mbedtls import x509

now = dt.datetime.utcnow()
ca0_key = pk.RSA()
_ = ca0_key.generate()
ca0_csr = x509.CSR.new(ca0_key, "CN=Trusted CA", hashlib.sha256())
ca0_crt = x509.CRT.selfsign(ca0_csr, ca0_key,not_before=now, not_after=now + dt.timedelta(days=90), serial_number=0x123456, basic_constraints=x509.BasicConstraints(True, 1))

ca1_key = pk.ECC()
_ = ca1_key.generate()
ca1_csr = x509.CSR.new(ca1_key, "CN=Intermediate CA", hashlib.sha256())

ca1_crt = ca0_crt.sign(ca1_csr, ca0_key, now, now + dt.timedelta(days=90), 0x123456, basic_constraints=x509.BasicConstraints(ca=True, max_path_length=3))

ee0_key = pk.ECC()
_ = ee0_key.generate()
ee0_csr = x509.CSR.new(ee0_key, "CN=End Entity", hashlib.sha256())

ee0_crt = ca1_crt.sign(ee0_csr, ca1_key, now, now + dt.timedelta(days=90), 0x987654)


trust_store = tls.TrustStore()
trust_store.add(ca0_crt)

dtls_cli_ctx = tls.ClientContext(tls.DTLSConfiguration(trust_store=trust_store,validate_certificates=True,))

dtls_cli = dtls_cli_ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM),server_hostname=None)

from contextlib import suppress
def block(callback, *args, **kwargs):
     while True:
         with suppress(tls.WantReadError, tls.WantWriteError):
             return callback(*args, **kwargs)


class Callback:

    def published(self, MsgId):
        print("Published")

def connect_gateway():
    try:
        while True:
            try:
                aclient.connect()
                dtls_cli.connect(("192.168.1.9", 4433))
                block(dtls_cli.do_handshake)
                print('Connected to gateway...')
                break
            except:
                print('Failed to connect to gateway, reconnecting...')
                time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit()

def register_topic():
    global topic1
    topic1 = aclient.register("topic1")
    print("topic1 registered.")

aclient = Client("client_sn_pub", "192.168.1.9", port=4433)
aclient.registerCallback(Callback())
connect_gateway()

topic1 = None
register_topic()

payload1 = 'Hello World!'

while True:
    block(dtls_cli.send, payload1)
    block(dtls_cli.recv, 4096)
    time.sleep(2)

aclient.disconnect()
dtls_cli.close()
print("Disconnected from gateway.")
