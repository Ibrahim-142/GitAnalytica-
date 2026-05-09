from collections import defaultdict


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
        total_stars += stars

        clean_repos.append(
            {
                "name": repo["name"],
                "stars": stars,
                "forks": repo.get("forks_count", 0),
                "updated_at": repo.get("updated_at"),
                "language": lang,
            }
        )

    top_repos = sorted(clean_repos, key=lambda x: x["stars"], reverse=True)[:5]

    return {
        "languages": dict(languages),
        "total_stars": total_stars,
        "top_repos": top_repos,
        "all_repos": clean_repos,
    }
