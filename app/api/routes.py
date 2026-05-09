from fastapi import APIRouter, HTTPException

from app.services.github_service import get_user, get_repos
from app.services.analyzer import analyze_repos
from app.services.scoring import calculate_score
from app.services.ai_summary import generate_summary
from app.services.comparison import compare_users
from app.services.ai_summary import generate_comparison_summary

router = APIRouter()


@router.get("/analyze/{username}")
def analyze(username: str):

    try:
        user = get_user(username)
        repos = get_repos(username)

        analysis = analyze_repos(repos)

        score = calculate_score(user, analysis, repos)

        summary = generate_summary(
            {
                "developer_score": score,
                "languages": analysis["languages"],
                "total_stars": analysis["total_stars"],
                "public_repos": user.get("public_repos", 0),
                "top_repos": analysis["top_repos"],
            }
        )

        return {
            "username": username,
            "name": user.get("name"),
            "bio": user.get("bio"),
            "followers": user.get("followers"),
            "following": user.get("following"),
            "public_repos": user.get("public_repos"),
            "developer_score": score,
            "languages": analysis["languages"],
            "top_repos": analysis["top_repos"],
            "all_repos": analysis["all_repos"],
            "summary": summary,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/compare/{user1}/{user2}")
def compare(user1: str, user2: str):

    try:
        data = compare_users(user1, user2)

        ai_analysis = generate_comparison_summary(data)

        return {**data, "analysis": ai_analysis}

    except Exception as e:
        return {"error": str(e)}
