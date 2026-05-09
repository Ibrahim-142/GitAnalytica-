from fastapi import FastAPI, HTTPException
from github_api import get_user, get_repos
from analyzer import analyze_repos, calculate_developer_score
from ai_summary import generate_summary

app = FastAPI(title="GitHub Profile Analyzer MVP")


@app.get("/analyze/{username}")
def analyze(username: str):

    try:
        user = get_user(username)
        repos = get_repos(username)

        analysis = analyze_repos(repos)
        developer_score = calculate_developer_score(
            followers=user.get("followers", 0),
            total_stars=analysis["total_stars"],
            public_repos=user.get("public_repos", 0),
            languages=analysis["languages"],
            repos=repos,
        )
        summary = generate_summary(
            {
                "username": username,
                "developer_score": developer_score,
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
            "developers_score": developer_score,
            "summary": summary,
            "followers": user.get("followers"),
            "following": user.get("following"),
            "public_repos": user.get("public_repos"),
            "total_stars": analysis["total_stars"],
            "languages": analysis["languages"],
            "top_repos": analysis["top_repos"],
            "all_repos": analysis["all_repos"],
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
