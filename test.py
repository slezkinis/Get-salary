import requests


headers = {
    'X-Api-App-Id': 'v3.r.136904076.5b2277b0262282dca0f02c33c74a21924e5f7424.be10ea58f779cf61ed289c50609ee58ecc89c24c'
}
payload = {
    'town': 4,
    'catalogues': 48
}
response = requests.get('https://api.superjob.ru/3.0/vacancies', headers=headers, params=payload)
response.raise_for_status()
vacancies = response.json()
for about_profession in vacancies['objects']:
    print(f"{about_profession['profession']}, {about_profession['town']['title']}")
