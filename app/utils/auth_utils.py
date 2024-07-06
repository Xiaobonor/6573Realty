# app/utils/auth_utils.py
import os

from flask import session, redirect, request, flash, url_for
from functools import wraps


def login_required(f):
    """
    Decorator to check if the user is logged in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        def redirect_to_login():
            sso_login_url = os.getenv('HOST_DOMAIN') + '/auth/login'
            next_url = request.url
            return redirect(f"{sso_login_url}?next={next_url}")

        if 'user_info' not in session:
            return redirect_to_login()

        # Reset the session expiry time on each activity
        session.permanent = True

        return f(*args, **kwargs)

    return decorated_function


def seller_required(f):
    """
    Decorator to check if the user is logged in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        def redirect_to_login():
            sso_login_url = os.getenv('HOST_DOMAIN') + '/auth/login'
            next_url = request.url
            return redirect(f"{sso_login_url}?next={next_url}")

        def redirect_to_register():
            # noinspection PyTypeChecker
            flash({"title": "授權失敗", "content": "未能成功授權，請先註冊成為房地產經紀人。"}, "popup_error")
            return redirect(url_for('seller_register.register'))

        if 'user_info' not in session:
            return redirect_to_login()

        if not session['user_info']['sell_rent_property']:
            print(session['user_info']['sell_rent_property'])
            return redirect_to_register()

        session.permanent = True

        return f(*args, **kwargs)

    return decorated_function

