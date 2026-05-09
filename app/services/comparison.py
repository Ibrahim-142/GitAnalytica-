from app.services.github_service import get_user, get_repos
from app.services.analyzer import analyze_repos
from app.services.scoring import calculate_score


def compare_users(user1: str, user2: str):

    # user 1
    u1 = get_user(user1)
    r1 = get_repos(user1)
    a1 = analyze_repos(r1)
    s1 = calculate_score(u1, a1, r1)

    # user 2
    u2 = get_user(user2)
    r2 = get_repos(user2)
    a2 = analyze_repos(r2)
    s2 = calculate_score(u2, a2, r2)

    return {
        "user1": {
            "username": user1,
            "score": s1,
            "stars": a1["total_stars"],
            "repos": u1.get("public_repos"),
            "languages": a1["languages"],
        },
        "user2": {
            "username": user2,
            "score": s2,
            "stars": a2["total_stars"],
            "repos": u2.get("public_repos"),
            "languages": a2["languages"],
        },
        "winner": user1 if s1 > s2 else user2 if s2 > s1 else "tie",
    }
