from openai import OpenAI

from config import GROQ_API_KEY

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")


def generate_summary(data: dict):

    prompt = f"""
    Analyze this GitHub developer profile.

    Username: {data['username']}

    Developer Score: {data['developer_score']}

    Languages:
    {data['languages']}

    Total Stars:
    {data['total_stars']}

    Public Repositories:
    {data['public_repos']}

    Top Repositories:
    {data['top_repos']}

    Write a professional recruiter-style summary
    describing this developer's strengths,
    technical focus, and activity level.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content
