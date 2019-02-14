from django.shortcuts import render, HttpResponse, reverse
from myadmin.models import *


# 确认订单
def orderConfirm(request):
    # 获取用户的id
    userid = request.session.get('user')['id']
    # 获取用户
    user = Users.objects.get(id=userid)
    # 获取用户地址
    address = user.address_set.all()
    # 获取选中的商品id
    goodsids = request.GET['goodsids']
    # 将商品id传入session中
    request.session['goodsids'] = goodsids
    # 切分
    goodsids = goodsids.split(',')
    # 获取商品
    goodslist = []
    for i in goodsids:
        cartgoods = CartGoods.objects.get(goodsid=i)
        cartgoods.items = Goods.objects.get(id=i)
        goodslist.append(cartgoods)
    # 分配数据
    context = {'goodslist': goodslist, 'address': address}
    # 加载模板
    return render(request, 'myapp/order.html', context)


# 新增收货地址
def addressinsert(request):
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
    # 获取当前用户购买商品的id号
    goodsids = request.session.get('goodsids')

    return HttpResponse('<script>alert("添加成功");location.href="'+reverse('orderConfirm')+'?goodsids='+goodsids+'"</script>')


# 生成订单
def orderinsert(request):
    # 获取用户id,及用户
    userid = request.session.get('user')['id']
    user = Users.objects.get(id=userid)
    # 获取收货地址id
    addressid = request.POST['addressid']
    # 获取购买商品id
    goodsids = request.session.get('goodsids')
    goodsids = goodsids.split(',')
    # 删除session中的商品id
    del request.session['goodsids']
    # 初始化总价
    totalprice = 0
    # 准备数据
    data = {'totalprice': totalprice, 'addressid': addressid, 'uid': user}
    # 生成订单
    userorder = UserOrder.objects.create(**data)

    # 生成订单详情并计算总价
    for i in goodsids:
        # 获取购物车中购买的商品数据
        cartgoods = CartGoods.objects.get(goodsid=i)
        # 生成订单详情
        orderinfo = OrderInfo()
        # 设置商品id
        orderinfo.goodsid = Goods.objects.get(id=cartgoods.goodsid)
        # 设置购买数量
        orderinfo.num = cartgoods.num
        # 设置商品单价
        orderinfo.price = Goods.objects.get(id=i).price
        # 设置外键
        orderinfo.orderid = userorder
        orderinfo.save()
        # 计算总价
        totalprice += cartgoods.price
        # 删除购物车已购买的商品
        cartgoods.delete()

    # 修改总价
    userorder.totalprice = totalprice
    userorder.save()
    # 跳转
    return HttpResponse('<script>location.href="'+reverse('orderbuy', args=[str(userorder.id)])+'"</script>')


# 支付界面
def orderbuy(request, orderid):
    # 获取用户订单
    userorder = UserOrder.objects.get(id=orderid)
    # 获取用户地址
    address = Address.objects.get(id=userorder.addressid)
    # 获取总价
    totalprice = userorder.totalprice
    # 分配数据
    context = {'orderid': orderid, 'address': address, 'totalprice': totalprice}

    return render(request, 'myapp/orderbuy.html', context)


# 支付成功界面
def buysuccess(request):
    # 获取订单id
    orderid = request.GET['orderid']
    # 修改订单状态
    userorder = UserOrder.objects.get(id=orderid)
    userorder.status = 1
    userorder.save()

    return render(request, 'myapp/buysuccess.html')


# 订单取消界面
def buycancel(request, oid):
    # 获取订单
    order = UserOrder.objects.get(id=oid)
    # 将状态更改为取消
    order.status = 3
    order.save()
    # 跳转
    return HttpResponse('<script>alert("订单取消成功");location.href="'+reverse('userorder')+'"</script>')









