from django.shortcuts import render, HttpResponse, reverse
from myadmin.models import *
from myadmin.views.IndexViews import uploads
import os


# 用户信息页
def userinfo(request):
    # 获取当前用户
    user = Users.objects.get(id=request.session.get('user')['id'])
    # 分配数据
    context = {'user': user}
    return render(request, 'myapp/usercenter/userinfo.html', context)


# 用户信息修改
def userchange(request):
    # 获取用户提交的信息
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # 获取当前用户
    user = Users.objects.get(id=request.session.get('user')['id'])
    # 更新用户信息
    user.username = data['username']
    user.age = data['age']
    user.sex = data['sex']
    user.email = data['email']
    myfiles = request.FILES.get('pic')
    if myfiles:
        # 如果有文件上传,删除原头像
        if user.pic != "/static/pics/user.jpg":
            from web.settings import BASE_DIR
            os.remove(BASE_DIR + user.pic)
        user.pic = uploads(myfiles)
    user.save()
    return HttpResponse('<script>alert("保存成功!");location.href="'+reverse('userinfo')+'"</script>')


# 用户订单页
def userorder(request):
    # 获取当前用户的id
    userid = request.session.get('user')['id']
    # 获取当前用户所有订单,并按照时间排序
    userorder = UserOrder.objects.filter(uid=userid).order_by('-addtime')
    # 分配数据
    context = {'userorder': userorder}
    # 加载模板
    return render(request, 'myapp/usercenter/userorder.html', context)


# 用户订单详情
def userorderinfo(request, userorderid):
    # 获取订单
    userorder = UserOrder.objects.get(id=userorderid)
    # 获取收货地址
    address = Address.objects.get(id=userorder.addressid)
    # 分配数据
    context = {'userorder': userorder, 'address': address}
    return render(request, 'myapp/usercenter/userorderinfo.html', context)


# 用户地址管理
def useraddress(request):
    # 获取当前用户
    user = Users.objects.get(id=request.session.get('user')['id'])
    # 获取用户所有的地址
    address = Address.objects.filter(uid=user.id).exclude(status=2)
    # 分配数据
    context = {'address': address}
    # 加载模板
    return render(request, 'myapp/usercenter/useraddress.html', context)


# 修改收货地址
def addresschange(request, addressid):
    # 获取用户提交的数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    print(data)
    # 获取要修改的地址
    address = Address.objects.get(id=addressid)
    # 修改数据
    address.addresspreson = data['addresspreson']
    address.address = data['address']
    address.addressphone = data['addressphone']
    # 判断用户是否设置为默认地址
    if 'status' in data:
        # 查询出该用户所有地址
        addressall = Address.objects.filter(uid=request.session.get('user')['id'])
        address.status = data['status']
        for x in addressall:
            x.status = 0
            x.save()
    else:
        if address.status == 1:
            address.status = 0
    address.save()
    return HttpResponse('<script>alert("地址更新成功!");location.href="'+reverse('useraddress')+'"</script>')


# 新增收货地址
def useraddressadd(request):
    # 获取提交的收货地址
    addressinfo = request.POST.dict()
    addressinfo.pop('csrfmiddlewaretoken')
    # 获取当前用户
    user = Users.objects.get(id=request.session.get('user')['id'])
    addressinfo['uid'] = user
    # 判断用户是否设置默认地址
    if 'status' in addressinfo:
        # 查询出该用户所有地址
        addressall = Address.objects.filter(uid=user.id)
        for x in addressall:
            x.status = 0
            x.save()
    # 存入数据库
    Address.objects.create(**addressinfo)

    return HttpResponse('<script>alert("添加成功");location.href="'+reverse('useraddress')+'"</script>')


# 删除地址
def addressdel(request,aid):
    # 获取当前地址
    address = Address.objects.get(id=aid)
    # 执行逻辑删除
    address.status = 2
    address.save()
    # 跳转
    return HttpResponse('<script>alert("删除成功");location.href="'+reverse('useraddress')+'"</script>')

