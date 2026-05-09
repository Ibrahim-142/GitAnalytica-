from openai import OpenAI
from app.core.config import GROQ_API_KEY

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in environment variables")

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


def format_languages(languages: dict):
    return "\n".join([f"- {k}: {v}" for k, v in languages.items()])


def format_repos(repos: list):
    repos = repos[:5]
    return "\n".join([f"- {r['name']} (⭐ {r['stars']})" for r in repos])


def generate_summary(payload: dict):

    prompt = f"""
Analyze this GitHub developer profile:

Score: {payload['developer_score']}

Languages:
{format_languages(payload['languages'])}

Total Stars: {payload['total_stars']}
Public Repos: {payload['public_repos']}

Top Repositories:
{format_repos(payload['top_repos'])}

Write a short recruiter-style summary.
"""

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"AI summary unavailable: {str(e)}"


def generate_comparison_summary(data: dict):

    prompt = f"""
You are a technical hiring assistant.

Compare two developers and explain why one is better.

User1:
- {data['user1']}

User2:
- {data['user2']}

Winner: {data['winner']}

Explain:
1. Why winner is better
2. Strengths of both
3. One improvement suggestion each

Keep it short and recruiter-friendly.
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return res.choices[0].message.content
