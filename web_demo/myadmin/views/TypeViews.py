# 分类管理视图函数
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from ..models import *


# 获取全部分类
def get_types_all():
    # 获取所有的商品分类
    # typelist = Types.objects.all()
    # select *,concat(path,id) as paths from myadmin_types order by paths;
    # 按照paths进行排序,concat是将path和id进行拼接形成新字段paths
    typelist = Types.objects.extra(select={'paths': 'concat(path,id)'}).order_by('paths')
    for x in typelist:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            ob = Types.objects.get(id=x.pid)
            x.pname = ob.name

    return typelist


@permission_required('myadmin.insert_types', raise_exception=True)
# 标签添加页面
def type_add(request):
    # 查询已有分类
    data = get_types_all()
    # 分配数据
    context = {'data': data}

    return render(request, 'myadmin/types/typeadd.html', context)


@permission_required('myadmin.insert_types', raise_exception=True)
# 执行添加标签
def type_insert(request):
    # 获取数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 判断所选分类下的分类名是否已经存在
    # 获取数据库中的所有数据
    data_all = Types.objects.filter(pid=data['pid'])
    for i in data_all:
        if i.name == data['name']:
            return HttpResponse('<script>alert("分类已存在!");location.href="'+reverse('type_add')+'"</script>')

    # 通过pid判断选中的是否为顶级分类
    if data['pid'] == '0':
        # 若是,则path为0,
        data['path'] = '0,'
        data['pname'] = '顶级分类'
    else:
        # 获取父级对象
        ob = Types.objects.get(id=data['pid'])
        # 将父级对象的path拼接上其id值存入数据中
        data['path'] = ob.path+data['pid']+','
        data['pname'] = ob.name
    # 创建对象
    Types.objects.create(**data)

    return HttpResponse('<script>alert("添加成功!");location.href="'+reverse('type_list')+'"</script>')


@permission_required('myadmin.show_types', raise_exception=True)
# 分类列表
def type_list(request):
    data = get_types_all()

    # 搜索
    # 接收用户搜索的关键词
    keywords = request.GET.get('keywords', None)
    # 搜索内容
    if keywords:
        data = data.filter(name__contains=keywords)

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(data, 10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page', 1)
    # 获取当前页的数据
    typelist = p.page(page_num)
    # 分配数据
    context = {'typelist': typelist}

    return render(request, 'myadmin/types/typelist.html', context)


@permission_required('myadmin.edit_types', raise_exception=True)
# ajax更改分类名
def type_change(request):
    # 获取分类的id值,找到分类
    ob = Types.objects.get(id=request.GET.get('id'))
    # 修改分类名
    ob.name = request.GET.get('newname')
    ob.save()

    return JsonResponse({'error': 0, 'msg': '更新成功'})


@permission_required('myadmin.del_types', raise_exception=True)
# 删除分类
def type_del(request):
    # 通过id值获取分类
    ob = Types.objects.get(id=request.GET['id'])
    # 判断该分类下是否还有子分类,若有则不能删除
    if Types.objects.filter(pid=ob.id).count():
        return JsonResponse({'error': 1, 'msg': '该分类下拥有子分类,无法删除'})

    # 判断该分类下是否有商品,若有则不能删除

    # 执行删除
    ob.delete()

    return JsonResponse({'error': 0, 'msg': '删除成功'})


