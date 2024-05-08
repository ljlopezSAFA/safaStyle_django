from django.shortcuts import redirect


def check_user_logged():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('no_user_logged_error')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def check_user_role(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if request.user == "AnonymousUser" or not hasattr(request.user, 'rol') or request.user.rol != required_role:
                return redirect('permision_error')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def check_user_roles(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user == "AnonymousUser" or not hasattr(request.user, 'rol') \
                    or request.user.rol not in required_roles:
                return redirect('permision_error')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
