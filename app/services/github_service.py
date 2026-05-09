import requests
from app.core.config import GITHUB_BASE_URL


def get_user(username: str):
    url = f"{GITHUB_BASE_URL}/users/{username}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()


def get_repos(username: str):

    repos = []
    page = 1

    while True:
        url = f"{GITHUB_BASE_URL}/users/{username}/repos?per_page=100&page={page}"
        res = requests.get(url)
        res.raise_for_status()

        data = res.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos
