import requests
import subprocess

API_KEY = "YOUR_API_KEY"

ip = input("Enter IP to check and block: ")

url = "https://api.abuseipdb.com/api/v2/check"

querystring = {
    'ipAddress': ip,
    'maxAgeInDays': '90'
}

headers = {
    'Accept': 'application/json',
    'Key': API_KEY
}

response = requests.get(url, headers=headers, params=querystring, timeout=10)

data = response.json()

abuse_score = data["data"]["abuseConfidenceScore"]

print(f"Abuse Score: {abuse_score}")

if abuse_score > 50:
    print("Malicious IP detected. Blocking...")
    
    subprocess.run([
        "sudo",
        "iptables",
        "-A",
        "INPUT",
        "-s",
        ip,
        "-j",
        "DROP"
    ])

    print(f"{ip} blocked successfully.")

else:
    print("IP appears safe.")
