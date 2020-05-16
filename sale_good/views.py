from django.shortcuts import render, redirect
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def saleindex(request):
    return render(request,'sale_good/sale_good.html',locals())
def salegood(request):
    if request.method == 'POST':
    #描述的信息、图片
        content = request.POST.get('content')
        img = request.FILES.get('img')
        name = request.FILES.get('img').name
    #金额种类
        money = request.POST.get('money')
        email = request.POST.get('email')
        sort = request.POST.get('sort')
        sme = models.salegood( description=content, money = money , email = email, sort = sort ,img_url=img,name=name)
        sme.save()
    return render(request,'sale_good/sale_good.html',locals())
# 主页显示缩略图
def showImg(request):
    imgs =models.salegood.objects.all() # 从数据库中取出所有的图片路径
    sort = models.salegood.objects.all().values('sort')

    context = {
        'imgs' : imgs,
        'sort' : sort
    }
    return render(request, 'sale_good/showImg.html', locals())


# 分页
def listing(request):
    contact_list = models.salegood.objects.all()
    paginator = Paginator(contact_list, 3) # 每页显示25条

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'sale_good/showImg.html', {'contacts': contacts})


