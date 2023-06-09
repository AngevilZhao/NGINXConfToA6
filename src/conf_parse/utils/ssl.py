# import OpenSSL

class SSLCrt():
    def __init__(self, file_path: str):
        self.file_path = file_path

        self.crt = None

        # self.version = None
        # self.serial_number = None
        # self.signature_algorithm = None
        # # 证书颁发者
        # self.common_name = None
        # self.start_time = None
        # self.end_time = None


    def parse(self):
        with open(self.file_path, "r") as f:
            self.crt = f.read()
        # cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, 
        #      self.crt)
        # certIssue = cert.get_issuer()
        # self.version = cert.get_version()
        # self.serial_number = cert.get_serial_number()
        # self.signature_algorithm = cert.get_signature_algorithm()
        # self.common_name = certIssue.commonName
        # self.start_time = cert.get_notBefore()
        # self.end_time = cert.get_notAfter()


class SSLKey():
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

        self.key = None

    def parse(self):
        with open(self.file_path, "r") as f:
            self.key = f.read()