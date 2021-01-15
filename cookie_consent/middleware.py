from django.utils.encoding import smart_str

from cookie_consent.cache import all_cookie_groups
from cookie_consent.models import UserCookieConsent
from cookie_consent.util import (
    get_cookie_dict_from_request,
    is_cookie_consent_enabled,
    set_cookie_dict_to_response,
)
from cookie_consent.conf import settings


class CheckUserCookieContentMiddleware:
    """
    Set existing cookie consent to the response when user is authenticated
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user_cookie_consents = UserCookieConsent.objects.filter(user=request.user)
            cookie_dic = {}
            for user_cookie_consent in user_cookie_consents:
                cookie_group = user_cookie_consent.cookiegroup
                if user_cookie_consent.action == 1:
                    cookie_dic[cookie_group.varname] = cookie_group.get_version()
                else:
                    cookie_dic[cookie_group.varname] = settings.COOKIE_CONSENT_DECLINE

            if user_cookie_consents.exists():
                consent_expiration_date = min(
                    [user_cookie_consent.modified for user_cookie_consent in user_cookie_consents])
            else:
                consent_expiration_date = None
            set_cookie_dict_to_response(response, cookie_dic, consent_expiration_date)

        return response


class CleanCookiesMiddleware:
    """
    Clean declined cookies
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not is_cookie_consent_enabled(request):
            return response
        cookie_dic = get_cookie_dict_from_request(request)
        for cookie_group in all_cookie_groups().values():
            if not cookie_group.is_deletable:
                continue
            group_version = cookie_dic.get(cookie_group.varname, None)
            for cookie in cookie_group.cookie_set.all():
                if cookie.name not in request.COOKIES:
                    continue
                if group_version == settings.COOKIE_CONSENT_DECLINE:
                    response.delete_cookie(smart_str(cookie.name),
                                           cookie.path, cookie.domain)
                if group_version < cookie.get_version():
                    response.delete_cookie(
                        smart_str(cookie.name),
                        cookie.path, cookie.domain
                    )

        return response
