from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from ..models import *
from .TypeViews import get_types_all
from .IndexViews import uploads
import os
from django.db.models import Q


@permission_required('myadmin.insert_goods', raise_exception=True)
# 商品添加页面
def goods_add(request):
    # 查询现有的分类
    data = get_types_all()
    # 分配数据
    context = {'data': data}
    return render(request, 'myadmin/goods/goodadd.html', context)


@permission_required('myadmin.insert_goods', raise_exception=True)
# 执行添加
def goods_insert(request):
    # 接收数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # 处理图片
    myfiles = request.FILES.get('pic', None)
    if not myfiles:
        return HttpResponse('<script>alert("请上传商品缩略图");location.href="'+reverse('goods_add')+'"</script>')
    data['pic'] = uploads(myfiles)

    # 处理商品和分类间的关系
    data['tid'] = Types.objects.get(id=data['tid'])

    # 创建数据
    Goods.objects.create(**data)

    return HttpResponse('<script>alert("添加成功");location.href="'+reverse('goods_list')+'"</script>')


@permission_required('myadmin.show_goods', raise_exception=True)
# 商品列表
def goods_list(request):
    # 获取数据
    data = Goods.objects.exclude(status=3)

    # 获取用户要查询的类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断用户是否查询
    if types == 'tid':
        ob = Types.objects.exclude(pid=0)
        num = 0
        for o in ob:
            if keywords == o.name:
                data = data.filter(tid=o.id)
                num = 1
                break
        if num == 0:
            data = []
    elif types == 'status':
        if keywords == '新发布':
            data = data.filter(status=0)
        elif keywords == '热销':
            data = data.filter(status=1)
        elif keywords == '下架':
            data = data.filter(status=2)
        else:
            data = []
    elif types:
        types_data = {types + '__contains': keywords}
        data = data.filter(**types_data)

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(data, 10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page', 1)
    # 获取当前页的数据
    goodlist = p.page(page_num)

    # 分配数据
    context = {'data': goodlist}

    # 加载模板
    return render(request, 'myadmin/goods/goodlist.html', context)


@permission_required('myadmin.del_goods', raise_exception=True)
# 商品逻辑删除
def goods_del(request):
    # 通过商品id获取商品
    ob = Goods.objects.get(id=int(request.GET.get('id')))
    # 修改状态(逻辑删除)
    ob.status = 3
    ob.save()
    return JsonResponse({'error': 0, 'msg': '删除成功'})


@permission_required('myadmin.edit_goods', raise_exception=True)
# 商品修改页
def goods_change(request, id):
    # 获取商品信息
    ob = Goods.objects.get(id=id)
    # 获取分类信息
    data = get_types_all()
    # 分配数据
    context = {'goodsinfo': ob, 'data': data}
    # 加载模板
    return render(request, 'myadmin/goods/goodupdate.html', context)


@permission_required('myadmin.edit_goods', raise_exception=True)
# 执行修改
def goods_update(request):
    # 获取数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 获取对象
    ob = Goods.objects.get(id=data['id'])

    '''{'id': '1', 'tid': '3', 
    'title': '魅族16th', 'price': '2398', 
    'num': '1000', 'status': '0', 'pic': '', 
    'info': '<p>&lt;p&gt;魅族16th魅族16th魅族16th魅族16th魅族16th魅族16th&lt;/p&gt;</p>'}'''
    # 修改数据
    ob.title = data['title']
    ob.price = data['price']
    ob.num = data['num']
    ob.status = data['status']
    ob.info = data['info']
    # 处理图片
    myfiles = request.FILES.get('pic', None)
    if myfiles:
        # 如果有文件上传,删除原头像
        from web.settings import BASE_DIR
        os.remove(BASE_DIR + ob.pic)
        ob.pic = uploads(myfiles)
    # 处理分类
    ob.tid = Types.objects.get(id=data['tid'])
    ob.save()

    return HttpResponse('<script>alert("更新成功");location.href="'+reverse('goods_list')+'"</script>')





