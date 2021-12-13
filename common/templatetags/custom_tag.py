from django import template
from django.contrib.auth.models import User
from clientportal.models import UserDepositApproval
import hashlib
from random import randint

register = template.Library()

@register.filter
def get_user_deposit_auto(user_instance_id):
    a = UserDepositApproval.objects.filter(user_id = user_instance_id)
    if a.exists() and a.first().approve:
        d = 1
        return d
    d = 2
    return d

@register.filter
def make_hash_item(user_instance_id, user_instance_name):
    a = hashlib.md5()
    str_obj = "{0}{1}{2}".format(user_instance_name, randint(10023, 438843), user_instance_id)
    a.update(str_obj.encode())
    return a.hexdigest()

@register.filter
def round_amount_value(amount_value):
    a = round(amount_value, 3)
    return a
