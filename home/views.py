from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import template
from chat_db.models import User, Chat, Message
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
import time

mutation = list(Chat.objects.all().values())[0]['current_mutation']
counter = 1

def has_mutated(request):
    chatMutation = list(Chat.objects.all().values())[0]['current_mutation']
    global mutation
    global counter

    has_chat_mutated = False

    if (chatMutation != mutation and counter == 1):
      has_chat_mutated = True
      counter += 1
    elif (counter == 2):
      has_chat_mutated = True
      mutation = chatMutation
      counter = 1

    return JsonResponse(has_chat_mutated, safe=False)

def get_messages(request):
    messages = Message.objects.all()
    data = {'messages': list(messages.values())}
    # data = {'messages': list(messages)}
    # print(data.messages)
    # print(messages)
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
# Create your views here.
def addMessage(request):
    data = json.load(request)

    user = User.objects.get(user_id=int(data['user_id']))
    chat = Chat.objects.get(chat_id=int(data['chat_id']))

    message = Message(user=user, chat=chat, content=data['message'], type="text")
    message.save()

    chat.current_mutation = uuid.uuid4()
    chat.save()

    return HttpResponseRedirect("/")

def pages(request):
  # try:
    users = User.objects.all()

    chats = Chat.objects.all()

    messages = Message.objects.all()

    context ={
        "users": list(users.values()),
        "chats": chats,
        "messages": messages,
    }

    requested_html = request.path.split('/')[-1]
    
    if not requested_html or requested_html == '':
        requested_html = 'index.html'

    try:

        html_file = loader.get_template( requested_html )
        return HttpResponse(html_file.render(context, request))    

    except template.TemplateDoesNotExist:

        return HttpResponse("template not found = " + requested_html, status=404)

    except:
        return HttpResponse("Error 500" , status=500)