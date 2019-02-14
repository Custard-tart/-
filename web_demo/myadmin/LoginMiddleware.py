from django.http import HttpResponse
import re
from django.core.urlresolvers import reverse


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # 检测当前的请求是否已经登录,如果已经登录,.则放行,如果未登录,则跳转到登录页
        # 获取当前用户的请求路径  /admin/开头  但不是 /admin/login/  /admin/dologin/   /admin/verifycode
        urllist = [reverse('user_login')]
        # 判断是否进入了后台,并且不是进入登录页面
        if re.match('/myadmin/', request.path) and request.path not in urllist:
            # 检测session中是否存在 adminlogin的数据记录
            if not request.session.get('_auth_user_id', None):
                # 如果在session没有记录,则证明没有登录,跳转到登录页面
                return HttpResponse('<script>alert("请先登录");location.href="'+reverse('user_login')+'";</script>')

        # 验证前台登录
        # 有哪些需要登录的地址
        if re.match('/app/', request.path):
            # 验证是否已经登录
            if not request.session.get('user'):
                return HttpResponse('<script>alert("请先登录");location.href="'+reverse('app_login')+'";</script>')

        response = self.get_response(request)
        return response