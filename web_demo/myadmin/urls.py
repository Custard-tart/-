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
from . views import IndexViews, UserViews, TypeViews, GoodViews, orderview, AuthViews

urlpatterns = [
    # 后台首页
    url(r'^$', IndexViews.index, name='index'),
    # 后台登陆页
    url(r'^login/$', IndexViews.user_login, name='user_login'),
    # 后台退出
    url(r'^logout/$', IndexViews.user_logout, name='user_logout'),

    # 用户管理模块
    # 用户添加
    url(r'^user/add/$', UserViews.user_add, name='user_add'),
    url(r'^user/insert/$', UserViews.user_insert, name='user_insert'),
    # 用户列表
    url(r'^user/lists/$', UserViews.user_lists, name='user_lists'),
    # 用户编辑
    url(r'^user/change/?([0-9]+)/$', UserViews.user_change, name='user_change'),
    url(r'^user/update/', UserViews.user_update, name='user_update'),
    # 删除用户
    url(r'^user/del/?([0-9]+)/$', UserViews.user_del, name='user_del'),


    # 分类管理模块
    # 添加分类
    url(r'^type/add/$', TypeViews.type_add, name='type_add'),
    # 执行添加
    url(r'^type/insert/$', TypeViews.type_insert, name='type_insert'),
    # 分类列表
    url(r'^type/list/$', TypeViews.type_list, name='type_list'),
    # 修改分类名
    url(r'^type/change/$', TypeViews.type_change, name='type_change'),
    # 删除分类
    url(r'^type/del/$', TypeViews.type_del, name='type_del'),

    # 商品管理模块
    # 商品添加/发布
    url(r'^goods/add/$', GoodViews.goods_add, name='goods_add'),
    # 执行添加
    url(r'^goods/insert/$', GoodViews.goods_insert, name='goods_insert'),
    # 商品列表
    url(r'^goods/list/$', GoodViews.goods_list, name='goods_list'),
    # 商品逻辑删除
    url(r'^goods/del/$', GoodViews.goods_del, name='goods_del'),
    # 商品修改页
    url(r'^goods/change/?([0-9]+)/$', GoodViews.goods_change, name='goods_change'),
    url(r'^goods/update/$', GoodViews.goods_update, name='goods_update'),

    # 订单管理
    # 订单列表
    url(r'^order/list/$', orderview.order_list, name='order_list'),
    # 订单详情
    url(r'^order/info/?([0-9]+)/$', orderview.order_info, name='order_info'),
    # 删除订单
    url(r'^order/del/?([0-9]+)/$', orderview.order_del, name='order_del'),

    # 权限管理
    # 管理员添加
    url(r'^auth/user/add/$', AuthViews.authuseradd, name='authuseradd'),
    # 管理员列表
    url(r'^auth/user/list/$', AuthViews.authuserlist, name='authuserlist'),
    # 管理员修改
    url(r'^auth/user/change/?([0-9]+)/$', AuthViews.authuserchange, name='authuserchange'),
    # 管理员删除
    url(r'^auth/user/del/?([0-9]+)/$', AuthViews.authuserdel, name='authuserdel'),

    # 组添加
    url(r'^auth/group/add/$', AuthViews.authgroupadd, name='authgroupadd'),
    # 组列表
    url(r'^auth/group/list/$', AuthViews.authgrouplist, name='authgrouplist'),
    # 组修改
    url(r'^auth/group/change/?([0-9]+)/$', AuthViews.authgroupchange, name='authgroupchange'),
    # 组删除
    url(r'^auth/group/del/?([0-9]+)/$', AuthViews.authgroupdel, name='authgroupdel'),

]
