from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def worker_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    '''
    Decorator for views that checks that the logged in user is a worker,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff==False,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def employer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/login'):
    '''
    Decorator for views that checks that the logged in user is an employer,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# def post_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
#     if request.user.is_staff:
#         is_staff = True
#     else:
#         is_staff = False

#     if request.user==post.user or not is_staff:
#         is_allowed = True

#     if is_allowed:
#         pass
#     else:
#         path = request.build_absolute_uri()
#         resolved_login_url = resolve_url(settings.LOGIN_URL)
#         return redirect_to_login(
#                 path, resolved_login_url, redirect_field_name)