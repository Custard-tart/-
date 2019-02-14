from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from ..models import *
from .IndexViews import uploads
import os
from django.db.models import Q
from django.contrib.auth.decorators import permission_required


# Create your views here.


# 显示用户添加页面
@permission_required('myadmin.insert_users',raise_exception = True)
def user_add(request):
    return render(request, 'myadmin/users/useradd.html')


# 执行用户
@permission_required('myadmin.insert_users',raise_exception = True)
def user_insert(request):
    try:
        # 获取表单内容
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 密码加密
        data['password'] = make_password(data['password'])

        # 判断是否上传了头像
        myfiles = request.FILES.get('pic')
        # 判断是否有文件上传
        if myfiles:
            # 有文件上传
            data['pic'] = uploads(myfiles)
        else:
            # 没有文件上传使用默认头像
            data['pic'] = '/static/pics/user.jpg'

        # 创建用户
        Users.objects.create(**data)

        return HttpResponse("<script>alert('添加成功!');location.href='" + reverse('user_lists') + "'</script>")
    except:
        return HttpResponse("<script>alert('添加失败!');location.href='" + reverse('user_add') + "'</script>")


@permission_required('myadmin.show_users',raise_exception = True)
def user_lists(request):
    # 获取用户数据,排除已经逻辑删除的数据
    users = Users.objects.exclude(status=2)

    # 查询
    # 获取用户要查询的类型和关键字
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 判断用户是否查询
    if types:
        # 判断用户的查询类型
        if types == 'all':
            # 使用Q对象在已获取的用户数据中进行模糊查询
            users = users.filter(Q(username__contains=keywords) | Q(age__contains=keywords) | Q(phone__contains=keywords) | Q(email__contains=keywords))
        else:
            types_data = {types+'__contains':keywords}
            users = users.filter(**types_data)

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(users,10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page',1)
    # 获取当前页的数据
    userlist = p.page(page_num)

    # 分配数据
    data = {'users':userlist}

    # 解析模板
    return render(request, 'myadmin/users/userlist.html', data)


@permission_required('myadmin.edit_users',raise_exception = True)
def user_change(request,uid):
    # 根据用户id获取用户信息
    userinfo = Users.objects.get(id=uid)
    # 分配数据
    data = {'userinfo':userinfo}
    return render(request, 'myadmin/users/userupdate.html', data)

def user_update(request):
    try:
        # 接收修改的信息
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 根据id获取用户信息
        userinfo = Users.objects.get(id=data['id'])
        # 修改用户信息
        userinfo.username = data['username']
        userinfo.age = data['age']
        userinfo.sex = data['sex']
        userinfo.email = data['email']
        userinfo.phone = data['phone']
        userinfo.status = data['status']

        # 获取用户修改的头像
        myfiles = request.FILES.get('pic')
        # 先判断用户是否上传文件
        if myfiles:
            # 如果有文件上传,删除原头像
            if userinfo.pic != "/static/pics/user.jpg":
                from web.settings import BASE_DIR
                os.remove(BASE_DIR + userinfo.pic)

            data['pic'] = uploads(myfiles)
            userinfo.pic = data['pic']

        userinfo.save()

        return HttpResponse('<script>alert("更新成功!");location.href="'+reverse('user_lists')+'"</script>')
    except:
        return HttpResponse('<script>alert("更新失败!");location.href="'+reverse('user_lists')+'"</script>')


@permission_required('myadmin.del_users',raise_exception = True)
def user_del(request,uid):
    try:
        # 根据用户id查找用户信息
        user = Users.objects.get(id=uid)
        # 执行逻辑删除
        user.status = 2
        user.save()
        # 重新定向
        return HttpResponse('<script>alert("删除成功!");location.href="'+reverse('user_lists')+'"</script>')
    except:
        return HttpResponse('<script>alert("删除失败!");location.href="'+reverse('user_lists')+'"</script>')

