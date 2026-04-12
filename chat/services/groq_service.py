from groq import Groq
from django.conf import settings


def get_groq_response(message):
    try:
        # 🔑 Create client properly
        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful chatbot. Give short, direct, and useful answers. Do not introduce yourself."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "AI error"
