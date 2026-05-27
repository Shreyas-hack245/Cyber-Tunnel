import requests

ip = input("Enter IP Address: ")

url = "https://api.abuseipdb.com/api/v2/check"

querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '90'
}

headers = {
    'Accept': 'application/json',
    'Key': 'YOUR_API_KEY''
}

response = requests.get(url, headers=headers, params=querystring, timeout=10)

print(response.json())
