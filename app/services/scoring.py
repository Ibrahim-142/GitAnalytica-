from datetime import datetime, timezone


def calculate_score(user, analysis, repos):

    score = 0

    # -------------------------
    # 1. Repo quality (MOST IMPORTANT)
    # -------------------------
    # normalize stars so small devs are not punished
    star_score = min(analysis["total_stars"] * 2, 25)
    score += star_score

    # -------------------------
    # 2. Consistency (repo activity + count)
    # -------------------------
    repo_count = user.get("public_repos", 0)
    score += min(repo_count * 1.2, 20)

    # -------------------------
    # 3. Language diversity (skills signal)
    # -------------------------
    lang_score = len(analysis["languages"]) * 3
    score += min(lang_score, 15)

    # -------------------------
    # 4. Activity (soft scoring, not binary)
    # -------------------------
    recent = 0

    for r in repos:
        updated = r.get("updated_at")
        if not updated:
            continue

        dt = datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )

        days = (datetime.now(timezone.utc) - dt).days

        if days < 30:
            recent += 1

    # normalize activity (NOT binary anymore)
    activity_score = min(recent * 2, 15)
    score += activity_score

    # -------------------------
    # 5. Bonus: meaningful contribution signal
    # -------------------------
    fork_penalty = sum(1 for r in repos if r.get("fork"))
    score -= min(fork_penalty * 1, 5)

    # -------------------------
    # FINAL NORMALIZATION
    # -------------------------
    return max(0, min(int(score), 100))
