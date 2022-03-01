from .models import Category


def show_cat(req):
    return {'categories': Category.objects.filter(is_active=True).all()}
