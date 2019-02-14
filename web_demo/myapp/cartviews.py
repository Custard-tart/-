from django.shortcuts import render, HttpResponse, reverse
from django.http import JsonResponse
from myadmin.models import *


# 加入购物车
def cart_add(request):
    # 获取用户
    userid = request.session.get('user')['id']
    user = Users.objects.get(id=userid)
    # 获取商品id
    goodsid = request.GET['goodsid']
    # 获取商品
    goods = Goods.objects.get(id=goodsid)
    # 获取数量
    num = request.GET['num']
    try:
        # 判断商品是否存在于该用户购物车
        cartgoods = CartGoods.objects.filter(uid=userid).get(goodsid=goodsid)
        cartgoods.num += int(num)
        cartgoods.price = int(cartgoods.num) * float(goods.price)
        cartgoods.save()
        return JsonResponse({'error': 0, 'msg': '加入购物车成功'})
    except:
        # 计算小计
        price = int(num) * float(goods.price)
        # 准备数据
        data = {'uid': user, 'num': num, 'goodsid': goodsid, 'price': price}
        # 存入数据库
        CartGoods.objects.create(**data)

        return JsonResponse({'error': 0, 'msg': '加入购物车成功'})


# 购物车列表
def cart_list(request):
    try:
        # 获取用户的id
        userid = request.session.get('user')['id']
        # 获取的购物车信息
        goodslist = CartGoods.objects.filter(uid=userid)
        # 获取商品
        for i in goodslist:
            i.items = Goods.objects.get(id=i.goodsid)
        # 分配数据
        context = {'goodslist': goodslist}
        # 加载模板
        return render(request, 'myapp/cart.html', context)
    except:
        return HttpResponse('<script>alert("请您先登陆!");location.href="'+reverse('app_login')+'"</script>')


# 购物车列表修改
def cart_change(request):
    # 商品数量
    num = request.GET['num']
    # 商品id
    goodsid = request.GET['goodsid']
    # 获取商品
    goods = Goods.objects.get(id=goodsid)
    # 获取用户id
    userid = request.session.get('user')['id']
    # 获取购物车列表
    goodslist = CartGoods.objects.filter(uid=userid).get(goodsid=goodsid)
    # 修改数量和小计
    goodslist.num = int(num)
    goodslist.price = goods.price*int(num)
    goodslist.save()
    context = {'num': num, 'price': goodslist.price}

    return JsonResponse(context)


# 购物车删除商品
def cart_del(request):
    try:
        # 获取商品id
        goodsid = request.GET['goodsid']
        # 获取购物车记录
        cartgoods = CartGoods.objects.get(goodsid=goodsid)
        cartgoods.delete()
        # 返回数据
        return JsonResponse({'erorr': 0, 'msg': '删除成功'})
    except:
        return JsonResponse({'erorr': 1, 'msg': '删除失败'})




