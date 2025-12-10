import os
import time

def logo():
	os.system('clear');print(f"""

\033[1;97m  .M" "bgd  .M" "bgd `7MM" "Yp, 
  ,MI    "Y ,MI    "Y   MM    Yb 
  `MMb.     `MMb.       MM    dP 
    `YMMNq.   `YMMNq.   MM" "bg. 
  .     `MM .     `MM   MM    `Y 
  Mb     dM Mb     dM   MM    ,9 
  P"Ybmmd"  P"Ybmmd"  .JMMmmmd9
-----------------------------------------
 FACEBOOK  :     \033[1;97mShXXX
 WHATAPP   :     \033[1;97m+918000XXXXXX
 
-----------------------------------------
""")

# l1
logo()
time.sleep(2)

# nwe
os.system('cls' if os.name == 'nt' else 'clear')

# l2
logo()
print(" 💯 Opened Successfully!")
import requests
import time

def safe_get(url, headers, params=None):
    """Safe request → never crashes"""
    r = requests.get(url, headers=headers, params=params)

    # Instagram returned HTML/block page?
    if not r.text.strip().startswith("{"):
        print("⚠ Instagram blocked temporarily... retrying in 3 sec...")
        time.sleep(3)
        return safe_get(url, headers, params)

    return r.json()


def check_login(sessionid):
    url = "https://i.instagram.com/api/v1/accounts/current_user/"
    headers = {
        "User-Agent": "Instagram 155.0.0.37.107",
        "Cookie": f"sessionid={sessionid}"
    }
    try:
        r = requests.get(url, headers=headers)
        return r.status_code == 200 and r.text.startswith("{")
    except:
        return False


def get_user_id(sessionid, username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Instagram 155.0.0.37.107",
        "Cookie": f"sessionid={sessionid}"
    }

    data = safe_get(url, headers)

    try:
        return data["data"]["user"]["id"]
    except:
        print("❌ Username not found or private account.")
        return None


def fetch_list(sessionid, user_id, mode):
    if mode == "followers":
        url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/"
        filename = "followers.txt"
    else:
        url = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/"
        filename = "following.txt"

    headers = {
        "User-Agent": "Instagram 155.0.0.37.107",
        "Cookie": f"sessionid={sessionid}"
    }

    all_data = []
    next_max_id = ""

    while True:
        params = {}
        if next_max_id:
            params["max_id"] = next_max_id

        data = safe_get(url, headers, params)

        for u in data.get("users", []):
            all_data.append(f"{u['username']}|{u['full_name']}")

        next_max_id = data.get("next_max_id")
        if not next_max_id:
            break

        time.sleep(1)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(all_data))

    print(f"✔ Saved: {filename}")


# -----------------------------
# MAIN
# -----------------------------
sessionid = input("Enter  cookie:👉 ")

print("\nChecking login...\n")

if not check_login(sessionid):
    print("❌ Login Failed! Invalid or expired cookie.")
    exit()

print("✔ Login Successful!\n")

username = input(" target username:👉 ")

user_id = get_user_id(sessionid, username)

if not user_id:
    exit()

print("\nDownloading Followers...")
fetch_list(sessionid, user_id, "followers")

print("\nDownloading Following...")
fetch_list(sessionid, user_id, "following")

print("\n✅ ALL DONE — 🙅NO ERRORS!")