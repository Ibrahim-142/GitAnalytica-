import asyncio
from app.services.github_service import get_user, get_repos
from app.services.analyzer import analyze_repos
from app.services.scoring import calculate_score


async def build_profile(username: str):

    user = await get_user(username)
    repos = await get_repos(username)

    analysis = analyze_repos(repos)
    score = calculate_score(user, analysis, repos)

    return {
        "username": username,
        "score": score,
        "stars": analysis["total_stars"],
        "repos": user.get("public_repos"),
        "languages": analysis["languages"],
    }


async def compare_users(user1: str, user2: str):

    # ⚡ RUN BOTH USERS IN PARALLEL
    u1_data, u2_data = await asyncio.gather(build_profile(user1), build_profile(user2))

    winner = (
        user1
        if u1_data["score"] > u2_data["score"]
        else user2 if u2_data["score"] > u1_data["score"] else "tie"
    )

    return {"user1": u1_data, "user2": u2_data, "winner": winner}
