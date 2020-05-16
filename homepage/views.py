from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . import forms
import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
#留言板功能
def message_board(request):
    messages = models.Message.objects.all()    #将数据库里的留言信息表示在留言板上
    return render(request, 'homepage/message_board.html', {'messages' : messages})
def create(request):
    return render(request, 'homepage/create.html')
def save(request):
    username = request.POST.get("username")
    title = request.POST.get("title")
    content = request.POST.get("content")
    publish = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = models.Message(title=title, content=content, username=username, publish=publish)
    message.save()
    return HttpResponseRedirect('/homepage/message_board/')

def home(request):
    return render(request,'homepage/home.html')

def search(request):
    #strip 去除空格等
    search_word = request.GET.get('wd','').strip()
    condition = None
    #分词：按空格  $(and) |(or) ~(not)
    for word in  search_word.split(' '):
        if condition is None:
            condition = Q(title_icontains=word)
        else:
            condition = condition | Q(title_icontains=word)
    search_message = []
    if condition is not None:
        # 筛选：搜索
        search_message = models.Message.objects.filter(title__icontains=search_word)
    #分页
    paginator = Paginator(search_message,20)
    page_num = request.GET.get('page',1)
    page_of_message = paginator.get_page(page_num)

    context = {}
    context['search_word'] = search_word
    context['search_message_count'] = search_message.count()
    context['page_of_message'] = page_of_message
    return render(request,'homepage/search.html',context)


def showImg(request):
    imgs =models.Photo.objects.all() # 从数据库中取出所有的图片路径
    context = {
        'imgs' : imgs
    }
    return render(request, 'homepage/home.html', locals())