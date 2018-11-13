import requests

class Geetest3():
    def __init__(self, address="127.0.0.1", port=3333):
        self.url = f"http://{address}:{port}"
    
    def crack(self, gt, challenge, success=1):
        try:
            return requests.get(f"{self.url}/crack?gt={gt}&challenge={challenge}&success={success}").json()
        except:
            return None
    
    def status(self):
        try:
            return requests.get(f"{self.url}/status").json()
        except:
            return None
