import httpx
from app.core.config import GITHUB_BASE_URL


# ---------- USER ----------
async def get_user(username: str):

    url = f"{GITHUB_BASE_URL}/users/{username}"

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(url)

        if res.status_code != 200:
            raise Exception(f"User {username} not found")

        return res.json()


# ---------- REPOS ----------
async def get_repos(username: str):

    all_repos = []
    page = 1

    async with httpx.AsyncClient(timeout=10) as client:

        while True:

            url = f"{GITHUB_BASE_URL}/users/{username}/repos?per_page=100&page={page}"
            res = await client.get(url)

            if res.status_code != 200:
                raise Exception(f"Failed to fetch repos for {username}")

            data = res.json()

            if not data:
                break

            all_repos.extend(data)
            page += 1

    return all_repos
