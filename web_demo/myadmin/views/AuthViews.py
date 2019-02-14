from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission, Group
from myadmin.models import Types


@permission_required('myadmin.is_superuser', raise_exception=True)
# 管理员添加
def authuseradd(request):
    if request.method == 'GET':
        # 获取所有的分组
        grouplist = Group.objects.all()
        # 分配数据
        context = {'grouplist': grouplist}
        return render(request, 'myadmin/auth/users/authuseradd.html', context)
    elif request.method == 'POST':
        # 判断是否创建超级管理员
        if request.POST['is_superuser'] == '1':
            ob = User.objects.create_superuser(request.POST['username'], request.POST['email'], request.POST['password'])
        else:
            ob = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        ob.save()
        # 判断是否需要为用户分配组
        gs = request.POST.getlist('gs', None)
        if gs:
            # 给当前用户分组
            ob.groups.set(gs)
            ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="'+reverse('authuserlist')+'"</script>')


@permission_required('myadmin.is_superuser', raise_exception=True)
# 管理员修改
def authuserchange(request, uid):
    # 获取要修改的管理员
    user = User.objects.get(id=uid)
    if request.method == 'GET':
        # 查找所有的组不包括管理员已在的
        group = Group.objects.exclude(user=user)
        # 分配数据
        context = {'user': user, 'group': group}
        # 加载模板
        return render(request, 'myadmin/auth/users/authuserchange.html', context)
    elif request.method == 'POST':
        # 获取提交的信息
        data = request.POST.dict()
        # 执行修改
        user.username = data['username']
        user.is_superuser = data['is_superuser']
        user.email = data['email']
        # 获取新分配的组
        group = request.POST.getlist('group', None)
        print(group)
        # 清除旧组
        user.groups.clear()
        if group:
            # 添加新组
            user.groups.set(group)
        user.save()
    # 跳转
    return HttpResponse('<script>alert("修改成功");location.href="'+reverse('authuserlist')+'"</script>')


@permission_required('myadmin.is_superuser', raise_exception=True)
# 管理员列表
def authuserlist(request):
    # 获取所有的管理员列表
    data = User.objects.all()

    # 获取用户要查询的类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断用户是否查询
    if types:
        data = data.filter(Q(username__contains=keywords))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(data, 10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page', 1)
    # 获取当前页的数据
    data = p.page(page_num)
    # 分配数据
    context = {'userlist': data}
    return render(request, 'myadmin/auth/users/authuserlist.html', context)


@permission_required('myadmin.is_superuser', raise_exception=True)
# 管理员删除
def authuserdel(request, uid):
    # 获取要删除的管理员
    user = User.objects.get(id=uid)
    # 执行删除
    user.delete()
    # 跳转
    return HttpResponse('<script>alert("删除成功");location.href="'+reverse('authuserlist')+'"</script>')


@permission_required('myadmin.is_superuser', raise_exception=True)
# 组添加
def authgroupadd(request):
    if request.method == 'GET':
        perms = Permission.objects.exclude(name__istartswith='Can')
        context = {'perms': perms}
        return render(request, 'myadmin/auth/group/authgroupadd.html', context)
    elif request.method == 'POST':
        # 创建组
        g = Group(name=request.POST['name'])
        g.save()
        # 获取选中的权限
        perms = request.POST.getlist('prms', None)
        # 判断是否选择权限
        if perms:
            g.permissions.set(perms)
            g.save()
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse('authgrouplist')+'"</script>')


@permission_required('myadmin.is_superuser', raise_exception=True)
# 组列表
def authgrouplist(request):
    # 获取所有的组
    data = Group.objects.all()

    # 获取用户要查询的类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断用户是否查询
    if types:
        data = data.filter(Q(name__contains=keywords))

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(data, 10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page', 1)
    # 获取当前页的数据
    data = p.page(page_num)
    # 分配数据
    context = {'glist': data}
    # 加载模板
    return render(request, 'myadmin/auth/group/authgrouplist.html', context)


@permission_required('myadmin.is_superuser', raise_exception=True)
# 组修改
def authgroupchange(request, gid):
    # 获取组
    group = Group.objects.get(id=gid)
    if request.method == 'GET':
        # 读取所有权限信息,并排除已经有的权限
        perms = Permission.objects.exclude(group=group).exclude(name__istartswith='Can')
        context = {'group': group, 'perms': perms}
        return render(request, 'myadmin/auth/group/authgroupchange.html', context)
    elif request.method == 'POST':
        # 获取组名
        group.name = request.POST['name']
        # 获取新权限
        prms = request.POST.getlist('prms', None)
        # 删除所有旧权限
        group.permissions.clear()
        # 判断是否存在权限
        if prms:
            group.permissions.set(prms)
        group.save()
    # 跳转
    return HttpResponse('<script>alert("修改成功");location.href="'+reverse('authgrouplist')+'"</script>')


@permission_required('myadmin.is_superuser', raise_exception=True)
# 组删除
def authgroupdel(request, gid):
    # 获取组
    group = Group.objects.get(id=gid)
    # 执行操作
    group.delete()
    # 跳转
    return HttpResponse('<script>alert("删除成功!");location.href="'+reverse('authgrouplist')+'"</script>')

