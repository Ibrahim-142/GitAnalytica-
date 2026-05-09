import requests

BASE_URL = "https://api.github.com"


def get_user(username: str):

    url = f"{BASE_URL}/users/{username}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_repos(username: str):

    all_repos = []

    page = 1
    per_page = 100

    while True:

        url = (
            f"{BASE_URL}/users/{username}/repos"
            f"?per_page={per_page}&page={page}"
        )

        response = requests.get(url)
        response.raise_for_status()

        repos = response.json()

        if not repos:
            break

        all_repos.extend(repos)

        page += 1

    return all_repos