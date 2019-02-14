from django import template
register = template.Library()
from django.utils.html import format_html
from ..views.TypeViews import *


# 自定义过滤器,用户列表分类使用
@register.simple_tag()
def ShowPages_user(count, request):

    # 获取当前页码数
    p = int(request.GET.get('page', 1))

    # 获取用户的搜索类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 定义空字符串
    u = ''
    # 判断,当types和keywords都不为空时进行拼接,并加入下面的地址中
    if types and keywords:
        u += '&'+'types='+types+'&'+'keywords='+keywords

    # count,总页数;p:当前页码
    # 判断总页码数小于10的情况
    if count <= 10:
        start = 1
        end = count
    else:
        # 判断当前页码数小于6
        if p < 6:
            start = 1
            end = 10
        # 当前页码数大于6 小于 count-4
        elif 6 <= p <= count-4:
            start = p-5
            end = p+4
        # 当前页码数大于count-4
        elif p > count-4:
            start = count-9
            end = count
    s = ""
    # 首页
    s += '<li><a href="?page=1'+u+'">首页</a></li>'

    # 上一页
    if p == 1:
        s += '<li class="am-disabled"><a href="?page=1'+u+'">«</a></li>'
    else:
        s += '<li><a href="?page='+str(p-1)+u+'">«</a></li>'
    for x in range(start, end+1):
        if p == x:
            s += '<li class="am-active"><a href="?page='+str(x)+u+'">'+str(x)+'</a></li>'
        else:
            s += '<li><a href="?page='+str(x)+u+'">'+str(x)+'</a></li>'

    # 下一页
    if p == count:
        s += '<li class="am-disabled"><a href="?page='+str(count)+u+'">»</a></li>'
    else:
        s += '<li><a href="?page='+str(p+1)+u+'">»</a></li>'

    # 尾页
    s += '<li><a href="?page='+str(count)+u+'">尾页</a></li>'

    return format_html(s)


# 自定义过滤器,分类列表分页使用
@register.simple_tag()
def ShowPages_type(count, request):

    # 获取当前页码数
    p = int(request.GET.get('page', 1))

    # 获取用户的搜索类型和关键字
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 定义空字符串
    u = ''
    # 判断,当types和keywords都不为空时进行拼接,并加入下面的地址中
    if keywords:
        u += '&'+'keywords='+keywords

    # count,总页数;p:当前页码
    # 判断总页码数小于10的情况
    if count <= 10:
        start = 1
        end = count
    else:
        # 判断当前页码数小于6
        if p < 6:
            start = 1
            end = 10
        # 当前页码数大于6 小于 count-4
        elif 6 <= p <= count-4:
            start = p-5
            end = p+4
        # 当前页码数大于count-4
        elif p > count-4:
            start = count-9
            end = count
    s = ""
    # 首页
    s += '<li><a href="?page=1'+u+'">首页</a></li>'

    # 上一页
    if p == 1:
        s += '<li class="am-disabled"><a href="?page=1'+u+'">«</a></li>'
    else:
        s += '<li><a href="?page='+str(p-1)+u+'">«</a></li>'
    for x in range(start, end+1):
        if p == x:
            s += '<li class="am-active"><a href="?page='+str(x)+u+'">'+str(x)+'</a></li>'
        else:
            s += '<li><a href="?page='+str(x)+u+'">'+str(x)+'</a></li>'

    # 下一页
    if p == count:
        s += '<li class="am-disabled"><a href="?page='+str(count)+u+'">»</a></li>'
    else:
        s += '<li><a href="?page='+str(p+1)+u+'">»</a></li>'

    # 尾页
    s += '<li><a href="?page='+str(count)+u+'">尾页</a></li>'

    return format_html(s)


# 头部导航栏用
@register.simple_tag()
def ShowTypes():
    # 获取所有二级分类
    data = Types.objects.exclude(pid=0)
    li = ''
    for x in data:
        li += '<li class="layout-header-nav-item"><a href="'+reverse('app_list', args=(x.id,))+'" class="layout-header-nav-link">'+x.name+'</a ></li>'
    return format_html(li)


