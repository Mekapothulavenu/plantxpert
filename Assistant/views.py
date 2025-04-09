from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Assistant.models import ChatMessage
import google.generativeai as genai
from agriapp.settings import GENERATIVE_AI_KEY
import markdown

# Configure AI Model
genai.configure(api_key=GENERATIVE_AI_KEY)

def assistant(request):
    """Clear previous chat and render chatbot page."""
    ChatMessage.objects.all().delete()  # Clear chat history on page load
    return render(request, 'assistant.html')  # No messages passed

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '').strip()
        user_name = request.POST.get('user_name', '').strip()

        if not user_message:
            return JsonResponse({'bot_response': "Please enter a message."})

        message_lower = user_message.lower()

        # Greetings
        greetings = ["hi", "hello", "hey", "yo"]
        if message_lower in greetings:
            if user_name:
                return JsonResponse({'bot_response': f"Hello {user_name}! 👋 How can I assist you with your farming or gardening today?"})
            else:
                return JsonResponse({'bot_response': "Hello! 👋 May I know your name before we begin?"})

        # Identity questions
        if "your name" in message_lower or "who are you" in message_lower:
            return JsonResponse({'bot_response': "I am PlantXpert Assistant 🌱, your smart agricultural guide. How can I help you today?"})

        # Prompt for Gemini
        prompt = (
            f"{user_name + ' asked: ' if user_name else ''}"
            f"{user_message}\n\n"
            "Please answer in clear, simple language suitable for farmers or beginners. "
            "Use clear points or paragraphs. Avoid markdown syntax like **. Focus on practical advice."
        )

        # AI response
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        bot_response = response.text.strip() if response else "I'm sorry, I couldn't understand your question."

        # Convert Markdown to clean HTML (optional)
        clean_html = markdown.markdown(bot_response)

        # Save to DB
        ChatMessage.objects.create(user_message=user_message, bot_response=clean_html)

        return JsonResponse({'bot_response': clean_html})
