from django.shortcuts import render
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from forum.models import Question, Reply
from product_catalog.models import Car
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
def show_forum(request) :
    cars = Car.objects.all()
    
    context = {
        'cars' : cars
    }
    
    return render(request, 'show_forum.html', context)

def get_questions_json(request):
    sort_by = request.GET.get('sort', 'terbaru')
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    questions = Question.objects.all().order_by('-created_at')
    
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
        
    if category:
        questions = questions.filter(category=category)
        
    if sort_by == 'terbaru':
        pass
    elif sort_by == 'populer':
        questions = questions.annotate(reply_count=Count('reply')).order_by('-reply_count', '-created_at')
        
    paginator = Paginator(questions, 10)
    page = request.GET.get('page', 1)
    questions_page = paginator.get_page(page)
    
    questions_data = json.loads(serializers.serialize('json', questions_page))
    for item in questions_data:
        question = Question.objects.get(pk=item['pk'])
        item['fields']['username'] = question.user.username
        item['fields']['reply_count'] = question.reply_set.count()
        item['fields']['created_at'] = question.created_at.strftime("%d %b %Y")

    return JsonResponse({
        'questions': questions_data,
        'total_pages': paginator.num_pages,
        'current_page': int(page)
    })
    
@csrf_exempt
@require_POST
@login_required(login_url='/auth/login')
def create_question_ajax(request) :
    user = request.user
    car_id = request.POST.get('car_id')
    title = strip_tags(request.POST.get('title'))
    content = strip_tags(request.POST.get('content'))
    category = request.POST.get('category')
    car = get_object_or_404(Car, pk=car_id)
    
    new_question = Question(
        user = user,
        car = car,
        title = title,
        category = category,
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