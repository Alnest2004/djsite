from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3
    # Будет создавать контекст для шаблона(+убирает дублирование кода)
    def get_user_context(self, **kwargs):
        # Сформируем начальный словарь из тех именнованых параметров
        # которые были передано вот этой функцией get_user_context
        context = kwargs
        # Читаем коллекцию cats с помощью функции get и ключ будет называться cats
        # А ТУТ МЫ ЕГО ПОЛУЧАЕМ
        cats = cache.get('cats')
        # далее проверяем если cats принимает значение None(то есть данные не были прочитаны)
        #
        if not cats:
            # Формируем список категорий.(читает данные из таблицы)
            cats = Category.objects.annotate(Count('women'))
            # Заносим эти данные в кэш. По ключу cats, мы будем заносить коллекцию
            # cats и далее укажем на какое время мы будем использовать этот кэш
            # ПОЛУЧАЕТСЯ ТУТ МЫ УСТАНАВЛИВАЕМ КЭШ
            cache.set('cats', cats, 60)


        # Сначала делаем копию всей коллекции. Затем проверяем если поль-
        # зователь не авторизован
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            # удаляем 2 пункт.({'title': "Добавить статью", 'url_name': 'add_page'},)
            user_menu.pop(1)

        # Затем в context передаём ссылку на это меню
        context['menu'] = user_menu

        context['cats'] = cats
        # ЕСЛИ **kwargs ТУТ В ПАРАМЕТРАХ МЫ ЭТОТ КЛЮЧ ПЕРЕДАЁМ ТО В context
        # , КОГДА МЫ ЕГО ПО УМОЛЧАНИЮ СОЗДАЁМ ЭТОТ КЛЮЧ БУДЕТ ПРИСУТСТВОВАТЬ
        # И В ЭТОМ СЛУЧАИ МЫ ПЕРЕОПРЕДЕЛЯТЬ ЕГО УЖЕ НЕ БУДЕМ. Но если в kwargs
        # КЛЮЧ cat_selected НЕ ПРИСУТСТВУЕТ, ТОГДА МЫ ПО УМОЛЧАНИЮ СДЕЛАЕМ ЕГО РАВНЫМ НУЛЮ
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
