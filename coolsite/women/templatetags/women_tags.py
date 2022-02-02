from django import template
# УЖЕ НЕ ИСПОЛЬЗУЕТСЯ ТАК КАК МИКСИНЫ(ОНИ используются в классах, в то время как тэги используются в функциях) КРУЧЕ
import women.views
from women.models import *

# Через него и происходит регистрация собственных шаблонных тэгов
register = template.Library()

# простой тэг - возвращаем коллекцию данных, которые используем в шаблоне
# функцию называем как удобно. name='getcats' - задаём название всей функции. Теперь
# что бы обратиться к этой функции нужно писать getcats вместо get_categories
@register.simple_tag(name='getcats')# связывает эту функцию с тегом(то есть превращает функцию в
# тег). Декоратор simple_tag экземпляр класса Library. register - мы указали выше
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        # Если фильтр присутсвует, то выбираем главные ключи(pk), которые соотв. фильтру
        return Category.objects.filter(pk=filter)

# включающий тэг - формирует фрагмент html страницы.


# "cats" - этот параметр, который возвращается нашей функцией, будет автоматически
# передаваться этому шаблону list_categories.html
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats":cats, "cat_selected":cat_selected}


@register.inclusion_tag('women/list_header.html')
def show_header(cat_selected=0):
    head = women.views.menu
    return {"head":head,"cat_selected":cat_selected}