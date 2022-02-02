from django.urls import path, re_path
from .views import *
# cache_page на его основе как раз таки и кэшируется отдельные либо функции либо
# классы представления
from django.views.decorators.cache import cache_page

# Список типов которые мы можем указывать:
# str - любая не пустая строка, исключая символ '/';
# int - любое положительное целое число, включая 0;
# slug - слаг, то есть, латиница ASCII таблицы, символы дефиса и подчёркивания;
# uuid - цифры, малые латинские символы ASCII, дефис;
# path - любая не пустая строка, включая символ '/'.

# re_path - ссылка которая может описываться с использование регулряных выражений
urlpatterns = [
    # .as_view - функция. Она действительно связывает класс с тем или иным маршрутом
    # cache_page(60) - вызываем декоратор. 60 - время хранения кэша(60 сек). И далее
    # в круглых скобках мы заключаем тот класс представления который будем кэшировать
    path('', WomenHome.as_view(), name='home'),  # http://127.0.0.1:8000/
    # <int:catid> - int = указываем тип элемента. catid = название(любое). Так
    # же это называется шаблоном
    #path('cats/<int:catid>/', categories),  # http://127.0.0.1:8000/cats/5/
    # ^ - обозначает начало последовательности
    # (?P<year>) - указываем имя year
    # (?P<year>[0-9]{4}) - это именнованый параметр year Для фрагмента этого шаблона
    #re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
