from datetime import datetime, timezone


def calculate_score(user, analysis, repos):

    score = 0

    # followers
    score += min(user.get("followers", 0) * 2, 20)

    # stars
    score += min(analysis["total_stars"] * 3, 30)

    # repos
    score += min(user.get("public_repos", 0), 20)

    # languages
    score += min(len(analysis["languages"]) * 2, 10)

    # activity
    active = False

    for r in repos:
        updated = r.get("updated_at")
        if not updated:
            continue

        dt = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )

        if (datetime.now(timezone.utc) - dt).days < 30:
            active = True
            break

    if active:
        score += 20

    return min(score, 100)
