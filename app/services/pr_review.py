import httpx
from app.core.config import GITHUB_BASE_URL, GITHUB_TOKEN
from openai import OpenAI
from app.core.config import GROQ_API_KEY

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def parse_pr_url(url: str):
    # Example:
    # https://github.com/user/repo/pull/12

    parts = url.replace("https://github.com/", "").split("/")

    owner = parts[0]
    repo = parts[1]
    pr_number = parts[3]

    return owner, repo, int(pr_number)


async def get_pr_files(owner: str, repo: str, pr_number: int):

    url = f"{GITHUB_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(url, headers=headers)

        if res.status_code != 200:
            raise Exception(f"Failed to fetch PR files: {res.text}")

        return res.json()


client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


def generate_review(pr_files):

    diff_text = ""

    for f in pr_files[:5]:
        diff_text += f"\nFile: {f['filename']}\n"
        diff_text += f.get("patch", "") + "\n"

    prompt = f"""
You are a senior software engineer.

Review this pull request diff:

{diff_text}

Give:
1. Code quality
2. Bugs or risks
3. Improvements
4. Should it be merged? (yes/no/maybe)

Be concise.
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return res.choices[0].message.content
