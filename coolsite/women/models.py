from django.urls import reverse

from django.db import models
# Для хранения ORM модели. Для представления базы из базы данных
# Create your models here.


# models.Model - этот базовый класс содержит все необходимые механизмы
# для того что бы мы могли создавать свои собственные классы моделей
class Women(models.Model):
    # verbose_name - Значение этого параметра используется админ панелью для отображения соответст. поля
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    # unique - говорим что оно будет уникальным!. db_index - Это поле будет индексируемым
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # blank=True - означает что данное поле content может быть пустым
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    # upload_to="photos/%Y/%m/%d/" - в какой каталог и подкаталоги мы
    # будем загружать наши изоброжения. Так же эти подкаталоги мы можем обределять в виде шаблона
    # Сначала будет идти подкаталог photos/. Затем %Y - текущий год.
    # %m- Текущий месяц. %d - Текущий день
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",verbose_name="Фото")
    # auto_now_add=True - это значит что поле time_create будет принимать
    # текущее время в момент добавление новой записи и дальше меняться уже не будет
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    # auto_now=True - будет меняться каждый раз когда мы что-либо меняем в этой текущей записи
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    # default=True - по умолчанию True
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    # Внешний ключ. Класс ForeignKey - для связи многие к одному.
    # 'Category' - первичная модель
    # on_delete=models.PROTECT - запрещает удалять категории на которые
    # есть ссылки из модели Women. related_name - задаёт имя с помощью которого
    # можно обращаться в терминале и получать все связанные данные
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    # reverse - будет формиравать маршрут с именем 'post' вот по этому
    # правилу =  'post/<int:post_id>/'. Для этого мы как раз таки дополнительно
    # передаём параметр post_id с идентификатором текущей функции self.pk
    # post - это как я понял имя шаблона в urls.py. А в 'post_id' мы
    # передаём номер в зависимоти от поста(которые перебираются через for в html документах)
    def get_absolute_url(self):
        # ЭТОТ ПАРАМЕТР post_slug Будет передоваться в urls!!!!!
        # ТУТ ВОЗВРАЩАЕТСЯ АДРЕС ДЛЯ ДОБАВЛЕННОГО ПОСТА
        return reverse('post', kwargs={'post_slug': self.slug})


    # Это специальный класс который используется админ панелью, для настройки
    # модели Women в каком-то ином виде.
    class Meta:
        # verbose_name - название таблицы Women в админке(в ед. числе вроде)
        verbose_name = 'Известные женщины'
        # verbose_name_plural - как будет во множественном числе
        verbose_name_plural = 'Известные женщины'
        # ordering - сортировка. time_create - по времени создания.
        # Тут происходит 2 сортировка. Сначала сортируется по time_create, затем
        # если значения равны, тогда сортируется по title. ЗНАК - ЭТО ОБРАТНАЯ СОРТИРОВКА
        # На сайте будт отоброжаться данные в такой же сортировке!!!
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # reverse()
        # Если вам нужно вернуть абсолютную ссылку, соответствующую
        # указанному представлению, как это делает url, Django
        # предоставляет следующую функцию. Если URL принимает аргументы,
        # вы можете их передать аргументом kwargs
        # ЭТОТ ПАРАМЕТР cat_slug Будет передоваться в urls!!!!!
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# Каждый класс модели содержит специальный статический объект objects
# он берётся из базового класса Model и представляет собой ссылку на спец. класс manager
# w4 = Women.objects.create(title='Ума Турман', content='Биография Ума Турман') - ПРИ
# ТАКОЙ ЗАПИСИ ДАННЫЕ ПОПАДАЮТ СРАЗУ В БАЗУ ДАННЫХ


# ОБНОВЛЕНИЕ ЗАПИСЕЙ В БД(ЧЕРЕЗ КОНСОЛЬ) ПРИМЕР=
# wu = Women.objects.get(pk=2)
# >>> wu.title = 'Марго Робби'
# >>> wu.content = 'Биография Марго Робби'
# >>> wu.save()
# УДАЛЕНИЕ ЗАПИСЕЙ В БД(ЧЕРЕЗ КОНСОЛЬ) ПРИМЕР=
# wd = Women.objects.filter(pk__gte=4)
# wd.delete()
# Результат = (2, {'women.Women': 2}). Первая цифра 2 означает что мы удалили 2 записи
# ДОБАВЛЕНИЕ ЗАПИСЕЙ В БД(ЧЕРЕЗ КОНСОЛЬ) ПРИМЕР=
# w2 = Women(title = 'Энн Хэтэуэй', content = "Биография Энн Хэтэуэй')
# ЧТЕНИЕ ЗАПИСЕЙ В БД(ЧЕРЕЗ КОНСОЛЬ) ПРИМЕР =
# Women.objects.filter(title='Энн Хэтэуэй')


# ЕСЛИ МЫ ХОТИМ ВЫБРАТЬ ВСЕ ЗАПИСИ В БД WOMEN КОТОРЫЕ СВЯЗАНЫ С Актрисами в базе данных
# категории используем следующий синтаксис:
# c = Category.objects.get(pk=1)
# c.women_set.all() - место women пишется та таблица в которой нужно что либо искать
# так же они должны быть связаны

#СПРАВОЧНИК ПО API QuerySet https://django.fun/docs/django/ru/3.2/ref/models/querysets/