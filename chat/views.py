from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage
from .services.groq_service import get_groq_response


# 🏠 Home Page
def home(request):
    sessions = ChatSession.objects.all().order_by('-created_at')
    return render(request, "chat.html", {"sessions": sessions})


# 💬 Chat API
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            message = request.POST.get("message")
            session_id = request.POST.get("session_id")

            # Create new session if not exists
            if not session_id or session_id == "null":
                session = ChatSession.objects.create()
            else:
                session = get_object_or_404(ChatSession, id=session_id)

            bot_response = get_groq_response(message)

            ChatMessage.objects.create(
                session=session,
                user_message=message,
                bot_response=bot_response
            )

            return JsonResponse({
                "response": bot_response,
                "session_id": session.id
            })

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"response": "Server error"})

    return JsonResponse({"response": "Invalid request"})


# 🔄 Load messages of a session
def load_chat(request, session_id):
    messages = ChatMessage.objects.filter(session_id=session_id)

    data = []
    for m in messages:
        data.append({
            "user": m.user_message,
            "bot": m.bot_response
        })

    return JsonResponse({"messages": data})


# 🗑 Delete one chat session
def delete_chat(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    session.delete()
    return JsonResponse({"status": "deleted"})


# 🧹 Clear current chat
def clear_chat(request, session_id):
    ChatMessage.objects.filter(session_id=session_id).delete()
    return JsonResponse({"status": "cleared"})
