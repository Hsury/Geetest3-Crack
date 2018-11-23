import requests
import time
from api import Geetest3

def main(address="127.0.0.1", port=3333):
    geetest3 = Geetest3(address=address, port=port)
    while True:
        captcha = get_captcha()
        if captcha:
            result = geetest3.crack(gt=captcha.get('gt'), challenge=captcha.get('challenge'), success=captcha.get('success'))
            status = geetest3.status()
            print("=" * 100)
            print(f"Captcha: {captcha}")
            print(f"Result: {result}")
            print(f"Status: {status}")
            print("=" * 100)
        time.sleep(1)

def get_captcha():
    try:
        response = requests.get("https://passport.bilibili.com/web/captcha/combine?plat=5").json()
        if response.get('code') == 0 and response.get('data', {}).get('type') == 1:
            return response.get('data', {}).get('result')
    except:
        pass
    return None

if __name__ == "__main__":
    main()
