import json
import datetime
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation


# --------------------------------------------------------------------------- #
#  Simple rule-based AI brain (no external API key required)                  #
# --------------------------------------------------------------------------- #

GREETINGS = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "howdy"]
FAREWELLS  = ["bye", "goodbye", "see you", "take care", "cya", "later"]

def ai_brain(text: str) -> str:
    t = text.lower().strip()

    # greetings
    if any(g in t for g in GREETINGS):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning! 🌅 I'm ARIA – your AI assistant. How can I help you today?"
        elif hour < 18:
            return "Good afternoon! ☀️ I'm ARIA. What can I do for you?"
        else:
            return "Good evening! 🌙 I'm ARIA. How may I assist you tonight?"

    # farewells
    if any(f in t for f in FAREWELLS):
        return "Goodbye! 👋 It was a pleasure talking with you. Have a wonderful day!"

    # time & date
    if "time" in t:
        return f"The current time is ⏰ {datetime.datetime.now():%I:%M %p}."
    if "date" in t or "today" in t:
        return f"Today is 📅 {datetime.datetime.now():%A, %B %d, %Y}."

    # weather placeholder
    if "weather" in t:
        conditions = ["sunny ☀️", "cloudy ☁️", "partly cloudy 🌤️", "rainy 🌧️", "windy 💨"]
        return (f"I don't have live weather data, but I can tell you it looks "
                f"{random.choice(conditions)} based on my imagination! 😄 "
                f"Check a weather service for the real forecast.")

    # jokes
    if "joke" in t or "funny" in t:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡",
            "Why did the developer go broke? Because he used up all his cache! 💸",
            "What's a computer's favorite snack? Microchips! 🍟",
        ]
        return random.choice(jokes)

    # identity
    if any(w in t for w in ["who are you", "your name", "what are you", "introduce"]):
        return ("I'm ARIA – Artificial Responsive Intelligent Assistant 🤖. "
                "I'm built with Django and powered by your browser's Web Speech API. "
                "Ask me anything!")

    # capabilities
    if any(w in t for w in ["what can you do", "help", "capabilities", "commands"]):
        return ("I can: 🕐 tell you the time & date, 😂 crack jokes, 🌤️ pretend to check weather, "
                "💬 have a friendly chat, 🧠 answer general questions, and much more! "
                "Just speak or type!")

    # thanks
    if any(w in t for w in ["thank", "thanks", "appreciate"]):
        return "You're very welcome! 😊 Always happy to help."

    # maths – very basic
    if any(op in t for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]):
        return "I can't compute complex math yet, but try Python's built-in calculator in the console! 🧮"

    # Django / Python question
    if "django" in t:
        return ("Django is a high-level Python web framework that encourages rapid development "
                "and clean, pragmatic design. 🐍 It follows the MTV (Model-Template-View) pattern. "
                "You're running Django right now – how meta! 😄")
    if "python" in t:
        return ("Python is a versatile, readable programming language loved by developers worldwide. 🐍 "
                "It's great for web dev, data science, AI, automation, and more!")

    # AI / ML questions
    if any(w in t for w in ["ai", "artificial intelligence", "machine learning", "deep learning"]):
        return ("AI is transforming everything! 🤖 Machine learning lets computers learn from data, "
                "while deep learning uses neural networks inspired by the human brain. "
                "I'm a tiny example of AI in action!")

    # motivational
    if any(w in t for w in ["motivat", "inspire", "quote"]):
        quotes = [
            "\"The only way to do great work is to love what you do.\" – Steve Jobs 💡",
            "\"In the middle of every difficulty lies opportunity.\" – Albert Einstein 🌟",
            "\"Code is like humor. When you have to explain it, it's bad.\" – Cory House 😄",
            "\"First, solve the problem. Then, write the code.\" – John Johnson 🔧",
        ]
        return random.choice(quotes)

    # default smart-ish fallback
    fallbacks = [
        f"Interesting question about '{text[:40]}...' 🤔 I'm still learning, but I'd love to explore that with you!",
        f"Hmm, '{text[:30]}' — that's a great topic! I don't have a perfect answer yet, but keep asking! 💭",
        f"Great point! I'm processing '{text[:35]}...' — my neural pathways are still growing. Try rephrasing? 🧠",
    ]
    return random.choice(fallbacks)


# --------------------------------------------------------------------------- #
#  Django Views                                                                #
# --------------------------------------------------------------------------- #

def index(request):
    recent = Conversation.objects.all()[:10]
    return render(request, "voiceai/index.html", {"history": recent})


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_msg = data.get("message", "").strip()
            if not user_msg:
                return JsonResponse({"error": "Empty message"}, status=400)

            response = ai_brain(user_msg)

            Conversation.objects.create(
                user_message=user_msg,
                ai_response=response,
            )

            return JsonResponse({"response": response, "user": user_msg})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST only"}, status=405)


def history(request):
    convos = list(
        Conversation.objects.values("user_message", "ai_response", "timestamp")[:20]
    )
    # make timestamp JSON-serialisable
    for c in convos:
        c["timestamp"] = c["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse({"history": convos})
