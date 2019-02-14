from django.shortcuts import render, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


# 后台首页
def index(request):

    return render(request, 'myadmin/index.html')


# 后台登陆
def user_login(request):
    if request.method == 'GET':
        return render(request, 'myadmin/login.html')
    elif request.method == 'POST':
        # 验证登陆密码
        # 使用django提供的后台用户验证方法
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            # 登录
            login(request, user)
            return HttpResponse('<script>location="'+reverse('index')+'"</script>')

        return HttpResponse('<script>alert("用户名或密码不正确");location="'+reverse('user_login')+'"</script>')


# 后台退出
def user_logout(request):
    # 退出登录
    logout(request)
    return HttpResponse('<script>alert("欢迎下次使用~再见~");location="'+reverse('user_login')+'"</script>')


# 头像上传
def uploads(myfiles):
    import time, random
    from web.settings import BASE_DIR
    filename = str(time.time()) + str(random.randint(1000, 99999)) + '.' + myfiles.name.split('.').pop()
    # 打开文件
    openfile = open(BASE_DIR + '/static/pics/' + filename, 'wb+')
    # .chunks() 分块写入
    for c in myfiles.chunks():
        openfile.write(c)
    openfile.close()
    return '/static/pics/'+filename