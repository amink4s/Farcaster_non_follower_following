import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()
NEYNAR_API = os.environ["NEYNAR_API"]
url = "https://api.neynar.com/v2/farcaster/following/"
headers = {"x-api-key": NEYNAR_API}
params = {"fid": 477126, "limit": 100}

users = []

while True:
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        print(f"Error: {r.status_code}, {r.text}")
        break

    data = r.json()
    users.extend(data.get("users", []))

    next_page = data.get("next")
    cursor = next_page["cursor"] if next_page else None
    if not cursor:
        break
    params["cursor"] = cursor

with open("following.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["fid", "username", "display_name"])  

    for item in users:
        user = item["user"]
        writer.writerow([
            user.get("fid"),
            user.get("username"),
            user.get("display_name")
        ])

print(f"Total following retrieved: {len(users)}")
print("following saved to following.csv")
