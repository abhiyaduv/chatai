from groq import Groq
from django.conf import settings

def get_groq_response(message):
    try:
        if not settings.GROQ_API_KEY:
            return "API key missing"

        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {str(e)}"
