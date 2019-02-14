from django.shortcuts import render, HttpResponse, reverse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin.models import *

# Create your views here.


# 查找分类下的所有商品
def search_goods(data):
    data2 = Types.objects.filter(pid=data)
    goodslist = []
    for j in data2:
        goodslist.append(j.goods_set.all())
    return goodslist


# 首页
def app_index(request):
    # 一级分类
    data = Types.objects.filter(pid=0)
    for i in data:
        # 二级分类
        i.items = Types.objects.filter(pid=i.id)
    # 查找所有手机
    phone = search_goods(1)
    # 查找智能设备
    aigoods = search_goods(2)
    # 查找数码影音
    audiogoods = search_goods(9)
    # 查找所有热销
    hotgoods = Goods.objects.filter(status=1)

    context = {
        'data':data,'phone':phone,
        'aigoods':aigoods,'audiogoods':audiogoods,
        'hotgoods':hotgoods,
    }
    return render(request, 'myapp/index.html', context)


# 注册
def app_register(request):
    if request.method == 'POST':
        # 获取数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        # 判断验证码是否正确
        if data['msgcode'] != request.session['msgcode']:
            return HttpResponse('<script>alert("验证码不正确!");location.href="'+reverse('app_register')+'"</script>')

        try:
            # 去除data中的验证码
            data.pop('msgcode')
            # 去除session中的验证码
            del request.session['msgcode']
            # 判断手机号是否已经注册
            if Users.objects.get(phone=data['phone']):
                return HttpResponse('<script>alert("该手机号已注册,请直接登陆");location.href="'+reverse('app_login')+'"</script>')
        except:
            # 密码加密
            data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
            # 设置默认头像
            data['pic'] = '/static/pics/user.jpg'
            Users.objects.create(**data)
            return HttpResponse('<script>alert("注册成功!请登陆");location.href="'+reverse('app_login')+'"</script>')
    else:
        return render(request, 'myapp/register.html')


# 登陆
def app_login(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            # 判断验证码
            if (request.POST['verifycode']).upper() != (request.session.get('verifycode')).upper():
                return HttpResponse('<script>alert("验证码错误");location.href="'+reverse('app_login')+'"</script>')
            # 通过手机号获取用户
            userinfo = Users.objects.get(phone=data['phone'])
            # 判断用户状态
            if userinfo.status == 1:
                return HttpResponse('<script>alert("账号已被禁用,请与客服联系进行解禁!");location.href="'+reverse('app_login')+'"</script>')
            if check_password(data['password'], userinfo.password):
                request.session['user'] = {'id':userinfo.id,'username':userinfo.username,'status':userinfo.status}
                return HttpResponse('<script>alert("登陆成功!");location.href="' + reverse('app_index') + '"</script>')
            else:
                return HttpResponse('<script>alert("用户名或密码错误!");location.href="' + reverse('app_login') + '"</script>')
        except:
            return HttpResponse('<script>alert("用户名或密码错误!");location.href="'+reverse('app_login')+'"</script>')
    else:
        return render(request, 'myapp/login.html')


# 登出
def app_logout(request):
    del request.session['user']
    return HttpResponse('<script>alert("退出成功");location.href="' + reverse('app_index') + '"</script>')


# 商品列表页
def app_list(request,goodsid):
    # 获取当前对象
    ob = Types.objects.get(id=goodsid)
    # 判断是是否为一级分类
    if ob.pid == 0:
        # 获取分类下的所有子分类
        typelist = Types.objects.filter(pid=goodsid)
        # 获取子分类下的所有商品
        goodslist = []
        for i in typelist:
            for j in i.goods_set.all():
                goodslist.append(j)
    else:
        # 获取当前分类的父级分类
        ob = Types.objects.get(id=ob.pid)
        # 获取所有子分类
        typelist = Types.objects.filter(pid=ob.id)
        # 获取相应分类下的所有商品
        goodslist = Goods.objects.filter(tid=goodsid)
        # 分配数据

    context = {'goodslist': goodslist, 'ob': ob, 'ob2': typelist}

    return render(request, 'myapp/list.html', context)


# 商品详情
def app_info(request,gid):
    # 获取商品对象
    goods = Goods.objects.get(id=gid)
    # 点击量+1
    goods.clicknum += 1
    goods.save()
    # 分配数据
    context = {'goods':goods}
    return render(request, 'myapp/info.html', context)


# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
       20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
       xy = (random.randrange(0, width), random.randrange(0, height))
       fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
       draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
       rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('INFROMAN.TTF', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 短信验证码接口
def sendmsg(request):
    # 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    # 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    # 注意事项：
    # （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    # （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    # （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

    # !/usr/local/bin/python
    # -*- coding:utf-8 -*-

    # import urllib2
    import urllib
    import json
    import random
    # 用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account = "C41315756"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "7f65678fe98cce91684328c7238fb865"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000, 99999))
    # 把验证码存入session
    request.session['msgcode'] = code
    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'}
    req = urllib.request.urlopen(
        url='http://106.ihuyi.com/webservice/sms.php?method=Submit',
        data=urllib.parse.urlencode(data).encode('utf-8')
    )
    content = req.read()
    res = json.loads(content.decode('utf-8'))
    print(res)

    return HttpResponse(res)

