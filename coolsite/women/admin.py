from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    # теперь мы можем указать вместо photo , get_html_photo(это название метода)
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}  # Мы можем указать что заполнять
    # автоматически поле slug на основе поля name

    # Этот атрибут содержит порядок и список редактируемых полей, которые
    # следует отображать в форме редактирования
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published','time_create', 'time_update')
    # указывает что эти поля не редактированные, только для чтения и только
    # после этого мы можем их прописать в коллекции fields
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # добавляет панельку сохранить, удалить и тд в вверх(для удобства)
    save_on_top = True

    # object - будет ссылаться на текущую запись списка. То есть он будет
    # ссылаться на объект модели Women и у этого объекта мы можем взять
    # атрибут .photo и взять url этого изображения.
    # Так же mark_safe - функция которая указывает не экранировать вот эти
    # теги <img. То есть эти теги будут рабочими они будут выполняться,
    # благодаря функции mark_safe
    def get_html_photo(self, object):
        # формируем html код
        # проверяет Если путь существует
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description="Миниатюра"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # Обязательно запятую так как мы передаём кортеж
    prepopulated_fields = {"slug": ("name",)} # Мы можем указать что заполнять
    # автоматически поле slug на основе поля name


# Предназначен для связи нашего приложения с админ панелью сайта
# Благодоря функции get_absolute_url в models. У нас появляется кнопка смотреть на сайте
# Первым параметром идёт класс модели, а вторым вспомогательный класс.
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах 2'