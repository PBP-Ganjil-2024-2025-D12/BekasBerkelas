from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from forum.models import Question, Reply
from product_catalog.models import Car

# Create your views here.
def show_forum(request) :
    context = {}
    return render(request, 'show_forum.html', context)

@csrf_exempt
@require_POST
@login_required(login_url='/auth/login')
def create_question_ajax(request) :
    user = request.user
    car_id = request.POST.get('car_id')
    title = strip_tags(request.POST.get('title'))
    content = strip_tags(request.POST.get('content'))
    car = get_object_or_404(Car, pk=car_id)
    
    new_question = Question(
        user = user,
        car = car,
        title = title,
        content = content
    )
    
    if (not title.strip() or not content.strip()) :
        return HttpResponse(b'BAD REQUEST', status=400)
    else :
        new_question.save()
    
    return HttpResponse(b'CREATED', status=201)

@csrf_exempt
@require_POST
@login_required(login_url='/auth/login')
def create_reply_ajax(request) :
    user = request.user
    question_id = request.POST.get('question_id')
    content = strip_tags(request.POST.get('content'))
    question = get_object_or_404(Question, pk=question_id)
    
    new_reply = Reply(
        user = user,
        question = question,
        content = content
    )
    
    if (not content.strip()) :
        return HttpResponse(b'BAD REQUEST', status=400)
    else :
        new_reply.save()
    
    return HttpResponse(b'CREATED', status=201)

@login_required(login_url='/auth/login')
def show_question_n_replies(request, id) :
    question = get_object_or_404(Question, pk=id)
    replies = Reply.objects.filter(question=question)
    
    if request.method == 'GET' :
        context = {
            'question': question,
            'replies': replies
        }
        return render(request, 'forum_detail.html', context)
    
    return HttpResponse(b'BAD REQUEST', status=400)