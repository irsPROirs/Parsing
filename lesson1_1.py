import requests

username = 'irsPROirs'
pas = '65bf426bd5edc4500240ea31e5ab11db9a92590f'
target = 'irsPROirs'
url = f'https://api.github.com/users/{target}/repos'
r = requests.get(url, auth=(username, pas))
repos = r.json()
for re in repos:
    print(re['name'])
