from collections import defaultdict
from datetime import datetime, timezone


def analyze_repos(repos: list):

    languages = defaultdict(int)
    total_stars = 0
    clean_repos = []

    for repo in repos:

        if repo.get("fork"):
            continue

        lang = repo.get("language")
        if lang:
            languages[lang] += 1

        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)

        total_stars += stars

        clean_repos.append(
            {
                "name": repo["name"],
                "stars": stars,
                "forks": forks,
                "updated_at": repo.get("updated_at"),
                "language": lang,
            }
        )

    # -------------------------
    # ranking function (FIXED INDENTATION)
    # -------------------------
    def rank_repo(repo):

        score = 0

        score += repo.get("stars", 0) * 2
        score += repo.get("forks", 0) * 3

        updated = repo.get("updated_at")

        if updated:
            try:
                dt = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=timezone.utc
                )

                days = (datetime.now(timezone.utc) - dt).days

                if days < 30:
                    score += 10
                elif days < 90:
                    score += 5

            except:
                pass

        if repo.get("language"):
            score += 2

        return score

    # -------------------------
    # FIX: top_repos was missing
    # -------------------------
    top_repos = sorted(clean_repos, key=rank_repo, reverse=True)[:5]

    return {
        "languages": dict(languages),
        "total_stars": total_stars,
        "top_repos": top_repos,
        "all_repos": clean_repos,
    }
