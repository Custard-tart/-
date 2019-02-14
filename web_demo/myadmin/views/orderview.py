from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, reverse, HttpResponse
from ..models import *

from django.db.models import Q


@permission_required('myadmin.show_orders', raise_exception=True)
# 订单列表
def order_list(request):
    # 查询所有的订单
    orderlist = UserOrder.objects.all().order_by('-addtime')

    # 查询
    # 获取用户要查询的类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断用户是否查询
    if types:
        # 判断用户的查询类型
        if types == 'username':
            # 模糊查询所有的符合关键字的用户
            users = Users.objects.filter(Q(username__contains=keywords))
            orderlist = []
            for u in users:
                for j in u.userorder_set.all():
                    orderlist.append(j)
        elif types == 'orderid':
            orderlist = UserOrder.objects.filter(id=keywords)

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页对象:参数1,数据列表;参数2,每页显示的条数
    p = Paginator(orderlist, 10)
    # 获取当前的页码数,如果没有默认为1
    page_num = request.GET.get('page', 1)
    # 获取当前页的数据
    orderlist = p.page(page_num)

    context = {'orderlist': orderlist}
    return render(request, 'myadmin/orders/orderlist.html', context)


# 订单详情
def order_info(request, orderid):
    # 获取订单详情
    order = UserOrder.objects.get(id=orderid)
    # 获取收货地址
    address = Address.objects.get(id=order.addressid)
    # 分配数据
    context = {'order': order, 'address': address}
    # 加载模板
    return render(request, 'myadmin/orders/orderinfo.html', context)


@permission_required('myadmin.del_orders', raise_exception=True)
# 删除订单
def order_del(request, orderid):
    # 获取订单
    userorder = UserOrder.objects.get(id=orderid)
    # 执行删除
    userorder.delete()
    # 跳转列表页
    return HttpResponse('<script>alert("删除成功");location.href="'+reverse('order_list')+'"</script>')

