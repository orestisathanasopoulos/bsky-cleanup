import requests
import json
from datetime import datetime
import time

USERNAME = "handle"  # Replace with your @ Bluesky handle without
APP_PASSWORD = 'password' # Replace with your app password - generated in your account settings


START_DATE = "YYYY-MM-DD"  # Format: YYYY-MM-DD
END_DATE = "YYYY-MM-DD"    # Format: YYYY-MM-DD

BASE_URL = "https://bsky.social/xrpc"



def authenticate():
    url = f"{BASE_URL}/com.atproto.server.createSession"
    payload = {
        "identifier": USERNAME,
        "password": APP_PASSWORD
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Authenticated as {USERNAME}")
        return data["accessJwt"]
    else:
        print(f"❌ Authentication failed: {response.text}")
        exit(1)


def fetch_posts(access_token):
    url = f"{BASE_URL}/app.bsky.feed.getAuthorFeed"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"actor": USERNAME, "limit": 100}

    all_posts = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Error fetching posts: {response.text}")
            exit(1)

        data = response.json()
        all_posts.extend(data.get("feed", []))

        if "cursor" in data:
            params["cursor"] = data["cursor"]
        else:
            break

    print(f"📥 Fetched {len(all_posts)} posts.")
    return all_posts


def filter_posts_by_date(posts, start_date, end_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    filtered_posts = []
    for post in posts:
        created_at = datetime.strptime(
            post["post"]["indexedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if start_dt <= created_at <= end_dt:
            filtered_posts.append({
                "rkey": post["post"]["uri"].split("/")[-1],
                "date": created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

    print(f"📌 Found {len(filtered_posts)} posts in the date range.")
    return filtered_posts


def delete_post(access_token, rkey):
    url = f"{BASE_URL}/com.atproto.repo.deleteRecord"
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    payload = {
        "repo": USERNAME,
        "collection": "app.bsky.feed.post",
        "rkey": rkey
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"🗑️ Deleted post {rkey}")
    else:
        print(f"❌ Failed to delete {rkey}: {response.text}")


if __name__ == "__main__":
    token = authenticate()
    posts = fetch_posts(token)
    posts_to_delete = filter_posts_by_date(posts, START_DATE, END_DATE)

    for post in posts_to_delete:
        time.sleep(1)
        delete_post(token, post["rkey"])
