from .token import check_token
from django.http import JsonResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = [
    "/api/ess/auth/login/",
    "/api/ess/auth/regist/"
]


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_WHITELIST:
            if "sites" in request.path:
                pass
            else:
                # 从请求头中获取 username 和 token
                username = request.META.get("HTTP_USERNAME")
                token = request.META.get("HTTP_AUTHORIZATION")
                if username is None or token is None:
                    return JsonResponse({"code": -2, "msg": "未查询到登录信息"})
                else:
                    # 调用 check_token 函数验证
                    if check_token(username, token):
                        pass
                    else:
                        return JsonResponse({"code": -2, "msg": "登录信息错误或已过期"})
