from collections import defaultdict
from datetime import datetime, timezone

def analyze_repos(repos: list):

    language_count = defaultdict(int)
    total_stars = 0

    all_repos = []

    for repo in repos:

        # skip forked repos
        if repo.get("fork"):
            continue

        lang = repo.get("language")

        if lang:
            language_count[lang] += 1

        stars = repo.get("stargazers_count", 0)

        total_stars += stars

        repo_data = {
            "name": repo["name"],
            "stars": stars,
            "forks": repo.get("forks_count", 0),
            "language": lang,
            "updated_at": repo.get("updated_at")
        }

        all_repos.append(repo_data)

    # top repos
    top_repos = sorted(
        all_repos,
        key=lambda x: x["stars"],
        reverse=True
    )[:5]

    return {
        "languages": dict(language_count),
        "total_stars": total_stars,
        "top_repos": top_repos,
        "all_repos": all_repos
    }
def calculate_developer_score(
    followers: int,
    total_stars: int,
    public_repos: int,
    languages: dict,
    repos: list
):

    score = 0

    # followers score
    score += min(followers * 2, 20)

    # stars score
    score += min(total_stars * 3, 30)

    # public repos score
    score += min(public_repos, 20)

    # language diversity
    score += min(len(languages) * 2, 10)

    # recent activity
    active_recently = False

    for repo in repos:

        updated_at = repo.get("updated_at")

        if updated_at:

            updated_date = datetime.strptime(
                updated_at,
                "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)

            days_ago = (
                datetime.now(timezone.utc) - updated_date
            ).days

            if days_ago <= 30:
                active_recently = True
                break

    if active_recently:
        score += 20

    return min(score, 100)