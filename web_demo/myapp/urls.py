"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views, cartviews, orderviews,userviews

urlpatterns = [
    # 首页
    url(r'^$', views.app_index, name='app_index'),
    # 注册
    url(r'^register/$', views.app_register, name='app_register'),
    # 短信验证码
    url(r'^register/sendmsg/$', views.sendmsg, name='sendmsg'),
    # 登陆
    url(r'^login/$', views.app_login, name='app_login'),
    # 登陆验证码
    url(r'^verifycode/$', views.verifycode, name='verifycode'),
    # 登出
    url(r'^logout/$', views.app_logout, name='app_logout'),
    # 列表
    url(r'^list/?([0-9]+)/$', views.app_list, name='app_list'),
    # 商品详情页
    url(r'^info/?([0-9]+)/$', views.app_info, name='app_info'),

    # 购物车
    # 加入购物车
    url(r'^app/cart/add/$', cartviews.cart_add, name='cart_add'),
    # 列表
    url(r'^app/cart/list/$', cartviews.cart_list, name='cart_list'),
    # 购物车列表修改
    url(r'^app/cart/change/$', cartviews.cart_change, name='cart_change'),
    # 购物车商品删除
    url(r'^app/cart/del/$', cartviews.cart_del, name='cart_del'),

    # 订单
    # 确认提交订单页面
    url(r'^app/order/confirm/$', orderviews.orderConfirm, name='orderConfirm'),
    # 新增收货地址
    url(r'^app/address/insert/$', orderviews.addressinsert, name='addressinsert'),
    # 生成订单
    url(r'^app/order/insert/$', orderviews.orderinsert, name='orderinsert'),
    # 支付界面
    url(r'^app/order/buy/?([0-9]+)/$', orderviews.orderbuy, name='orderbuy'),
    # 支付成功界面
    url(r'^app/buy/success/$', orderviews.buysuccess, name="buysuccess"),
    # 取消订单界面
    url(r'^app/buy/cancel/?([0-9]+)/$', orderviews.buycancel, name='buycancel'),

    # 用户个人中心
    # 用户信息
    url(r'^app/user/info/$', userviews.userinfo, name='userinfo'),
    # 用户信息修改
    url(r'^app/user/change/$', userviews.userchange, name='userchange'),
    # 用户订单页
    url(r'^app/user/order/$', userviews.userorder, name="userorder"),
    # 用户订单详情
    url(r'^app/user/order/info/?([0-9]+)$', userviews.userorderinfo, name='userorderinfo'),
    # 用户地址管理
    url(r'^app/user/address/$', userviews.useraddress, name='useraddress'),
    # 修改收货地址
    url(r'^app/user/address/change/?([0-9]+)$', userviews.addresschange, name='addresschange'),
    # 新增收货地址
    url(r'^app/user/address/add/$', userviews.useraddressadd, name='useraddressadd'),
    # 删除地址
    url(r'^app/user/address/del/?([0-9]+)/$', userviews.addressdel, name='addressdel'),

]
