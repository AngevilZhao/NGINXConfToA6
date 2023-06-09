import OpenSSL
import time
# from dateutil import parser

cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, 
             open("/Users/11133435/PycharmProjects/NGINXConfToA6/tests/test_cases/t1/cert/server.crt").read())
certIssue = cert.get_issuer()

print ("证书版本:            ",cert.get_version() + 1)

print ("证书序列号:          ",hex(cert.get_serial_number()))

print ("证书中使用的签名算法: ",cert.get_signature_algorithm().decode("UTF-8"))

print ("颁发者:              ",certIssue.commonName)

print(cert.get_notBefore())

print(certIssue.__dict__)