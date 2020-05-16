from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . import forms
import hashlib
import datetime
from django.utils import timezone

# Create your views here.

# 哈希密码,让后台不知道密码
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

# 创建确认码对象
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code

#发送邮件认证
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives
    subject = '来自蔡高畅的注册确认邮件'
    text_content = '''如果你看到这个邮件,就证明发送失败了,请联系管理员'''
#连接地址采用127.0.0.1,     点击返回认证界面       有效期时间在setting设置
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.cgc.com</a>，\
                   </p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(request):
    if not request.session.get('is_login', None):    #不在登陆状态就返回登陆页面
        return redirect('sale_good:showImg')
    return render(request, 'sale_good/sale_good.html')



def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('sale_good:showImg')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)


        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)

            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name


                return redirect('sale_good:showImg')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('sale_good:showImg')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)     #从forms里获取数据
        message = "请检查填写的内容！"
        if register_form.is_valid():         #获取到数据了,根据不同情况做出反应
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            xiaoqu = register_form.cleaned_data.get('xiaoqu')
            if password1 != password2:       #两次输入密码不一样
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:                #从数据库抽取用户名数据，判断是否存在已有用户名
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)      #判断邮箱是否存在
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())
                # 将输入\选择的数据 保存入数据库
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.xiaoqu = xiaoqu      #选择的选项 保存入数据库内
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")


def user_confirm(request):
    code = request.GET.get('code', None)    #获取确认码
    message = ''

    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time    #点击认证的时间
    now = now = timezone.now()  #datetime.datetime.now()       取得当下的时间
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):     #当下时间大于点击认证的时间+有效期限时间,过期
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:   #  正常
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())

