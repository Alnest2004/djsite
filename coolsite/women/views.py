from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# Для хранения представлений
# Create your views here.

# Обязательный параметр request - фактически это есть ссылка на
# класс HttpRequest(Который содержит инф. о запросе о сесии и тд).
# Получается что через переменную request нам доступна вся возможная
# информация в рамках текущего запроса.
# На выходе эта функция должна формировать Экземпляр класса HttpResponse.
# Содержимое главной страницы будет Страница приложения women.

class WomenHome(DataMixin, ListView):
    # Так как в ListView уже импортирован Paginator, мы можем его не импортировать
    # paginate_by это специальная переменная которой передаётся количество страниц,
    # которые мы хотим передавать на 1 страничку
    # paginate_by = 3
    # model - будет ссылаться на модель Women связанный с этим списком
    # Выбирает все записи из таблицы и пытается их отобразить в виде списка
    model = Women
    # template_name - указывает путь к нужному шаблону
    template_name = 'women/index.html'
    # указываем название переменной(posts) через каторое мы можем обращаться в
    # шаблоне
    context_object_name = 'posts'

    # спец атрибут которому мы передаём словарь. Тут мы можем передавать только
    # НЕИЗМЕНЯЕМЫЕ ЗНАЧЕНИЯ!
    # extra_context = {'title': 'Главная страница'}

    # Формирует и динамический(изменяемый) и статический(неизменяемый) контекст
    # который передаётся затем в шаблон index.html.
    def get_context_data(self, *, object_list=None, **kwargs):
        # мы обращаемся к базовому классу ListView и берём у него существующий
        # контекст. .get_context_data(**kwargs) - берёт существующий контекст и
        # передаём ей все именнованные параметры
        # Получаем контекст который уже сформирован для шаблона index.html. Например коллекция
        # context_object_name = 'posts' уже существует и мы её затереть не должны!
        context = super().get_context_data(**kwargs)  # формируется на основе ListView
        # Мы вызываем метод через self, мы можем так делать потому что класс WomenHome
        # наследует 2 базовых класса и мы к ним можем обращаться через self. И далее
        # передаём один именованный параметр title, и это будет передаваться в виде словаря
        # в kwargs(с ключом titile:"Главная страница")
        c_def = self.get_user_context(title="Главная страница")  # формируется на основе DataMixin
        # словарь c_def и context формирует нужный нам общий контекст. Тут мы их
        # объединяем для этого. Создаём список из первого и второго словаря и потом на
        # основе этого списка создаём общий словарь
        context = dict(list(context.items()) + list(c_def.items()))

        # Тут получается указывается каким параметрам какие значения присвоить
        # context['menu'] = menu  # это можно  не писать так как я это уже связал
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        return context

    # Возвращает только те записи в который is_published=True. Получается что теперь
    # model = Women будет читать не все записи,а только те которые подходят
    def get_queryset(self):
        # .select_related('cat') - ещё загружает записи из таблицы категории(
        # загружает их вместе с данными Women.objects.filter(is_published=True))
        # 'cat' - потому что в модели Women именно такой атрибут cat является внешним ключом
        # .select_related('cat') - будет реализован жадный запрос, который возьмёт
        # все связанные данные и из модели категории и тогда при выводе рубрик в
        # index.html, не будет выполняться дополнительный sql-запрос
        return Women.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)

# запрещает доступ не зарегестрированным пользователям у функций
# @login_required
def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


# LoginRequiredMixin запрещает доступ не зарегестрированным пользователям у класса
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # AddPostForm - класс формы который будет подключаться к этому классу вида(form_class)
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # ЕМУ ПРИСВАИВАЕМ АДРЕС МАРШРУТА, НА КОТОРЫЙ мы хотим переправиться в случаи
    # успешного заполнения статьи. reverse_lazy - выполняет построение маршрута,
    # только в момент когда он понадобиться, в отличии от просто reverse, который
    # пытается построить маршрут сразу же
    success_url = reverse_lazy('home')
    # Указывает адрес перенаправления для незарегистрированного пользователя
    login_url = reverse_lazy('home')

    # Генерирует страницу 403 (доступ запрещён)
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        return context


# def addpage(request):
#     # это равно true если мы грубо говоря нажали кнопку вход
#     if request.method == 'POST':
#         # тут мы передаём все данные которые были записаны.
#         # request.FILES - СПИСОК ФАЙЛОВ КОТОРЫЕ БЫЛИ ПЕРЕДАНЫ НА СЕРВЕР ИЗ ФОРМЫ
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # это просто в консоль выводит сведения
#             # print(form.cleaned_data)
#             # try:
#             # Делаем добавление новой записи в базу данных в таблицу Women и
#             # если добавление прошло успешно то перенаправляемся на главную стр
#             # Использование ** для распаковки словарей в другие словари.
#             # Women.objects.create(**form.cleaned_data)
#
#             # Когда форма связана с моделью можно поступить проще
#             # В результате все данные которые нам будут переданы от формы
#             # form.save() с помощью этого будут автоматически занесены в базу
#             # данных Women. Именно в Women потому что эта форма связана именно
#             # с моделью Women, в forms.py мы указали это!!
#             form.save()
#             return redirect('home')
#             # except:
#             # Добавляем общую ошибку для отображения на странице формы. И
#             # что бы она отображалась в addpage.html нужно кое что добавить
#             # form.add_error(None, 'Ошибка добавления поста')
#
#     # а это будет при первом входе на форму(она будет пустая и не заполненая)
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse("Обратная связь")

# FormView - это стандартный базовый класс для форм, которые не привязаны к модели
# то есть эта форма не будет работать с бд
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # указываем название через которое хотим обращаться в urls.py
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg - это уже для айдишников
    # указываем в какую переменную будут помещаться данные взятые из модели Women
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # тут заголовок поста формируется на основе context
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = context['post']
        # context['menu'] = menu
        return context


# post_id вроде берём из urls.py!
# def show_post(request, post_slug):
#     # Берём запись из модели Women у которого первичный ключ(pk) совпадает
#     # post_id который мы пердаём. get_object_or_404 - Функция Django, она выбирает
#     # из таблицы Women пост с таким первичным ключом pk(если он находится), если
#     # не находится то генерирует исключение 404
#     post = get_object_or_404(Women, slug=post_slug)
#
#     # формируем параметры котоыре будем передавать шаблону post.html
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         # cat_id - содержит id текущей рубрики к которой относится эта статья.
#         # post - эта сыллка на класс Women и когда создаётся экземпляр этого класса
#         # то появляется автоматически свойство cat_id.
#         # Из-за этой строчки то что выбрано перестаёт быть ссылкой и наоборот.
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


# Наследуется от ListView потому что это будет список
class WomenCategory(DataMixin, ListView):
    # paginate_by = 3 # оно работает сразу и всё отображает правильно, но это дублирование кода
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # если он установлен False, То будет возникать исключение 404 если такая стр не найдена
    allow_empty = False

    def get_queryset(self):
        # Выбираем записи из таблицы те которым соответствуют категории по указанному
        # слагу. .kwargs['cat_slug'] - получаем все параметры нашего маршрута. В частности
        # переменную cat_slug которую мы прописали в urls.py. cat__slug - слаг категории
        # cat__slug - означает что мы обращаемся к полю slug вот этого поля cat,
        # связанной с этой текущей записью
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # берём по слагу категорию для которой и выводим вот этот список c
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        # str(context['posts'][0].cat - Это берётся из базового класса
        # 'posts'[0].cat - коллекция прочитанных записей и в этой коллекции мы берём
        # первую запись и обращаемся к параметру cat(Который представляет собой
        # объект который возвращает название категории, но с помощью str, мы преобра-
        # зовываем его в строку)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # И тут происходит почти тоже самое, только тут мы берём идентификатор
        # выбранной рубрики ['posts'][0].cat_id
        # context['cat_selected'] = context['posts'][0].cat_id
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# Как я понял сами значения cat_id и тд, берутся из urls.py
# def show_category(request, cat_slug):
#     # выбираем посты которые соответсвуют текущей рубрике. Те у которых
#     # внешний ключ cat_id совпадает с ключом который мы передали в функцию
#     posts = Women.objects.filter(cat_id=cat_slug)
#
#     if len(posts) == 0:
#         allow_empty = False
#
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'women/index.html', context=context)


# передаём дополнительный параметр. Который и будет являться числом который мы напишем
# мы его тут как бы получаем
# УЖЕ НЕ ИСПОЛЬЗУЕМ
def categories(request, catid):
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


# УЖЕ НЕ ИСПОЛЬЗУЕМ
def archive(request, year):
    if int(year) > 2021:
        # redirect('/') - указывает куда мы будем перенаправлены если год будет больше чем 2021
        # permanent - указывает что сайт переместился на постоянной основе(301)
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


# exception - если произолши какие-то исключения, для этого и используется
# этот параметр.
# БУДЕТ ВЫЗЫВАТЬСЯ ВСЯКИЙ РАЗ ПРИ ВОЗНИКНОВЕНИИ ИСКЛЮЧЕНИЯ 404
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# Так как он будет работать с формой, то есть заносить данные в бд, то используем
# CreateView
class RegisterUser(DataMixin, CreateView):
    # Будет ссылаться на форму UserCreationForm(это стандартная джанговская
    # форма, которая служит для регистрации пользователей)
    # RegisterUserForm - наша собственная форма в forms.py
    form_class = RegisterUserForm
    # ссылка на шаблон который мы будем тут использоваться
    template_name = 'women/register.html'
    # перенаправление при успешной регистрации
    success_url = reverse_lazy('login')

    # контекст для шаблона register.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # Вызывается при успешной проверке формы регистрации(при успешной регистрации)
    def form_valid(self, form):
        # сохроняем форму в базу данных
        user = form.save()
        # login - функция джанго которая авторизовывает пользователя
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    # метод для формирования контекста для login.html шаблона
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    # logout - стандартная функция Django что бы пользователь вышел
    logout(request)
    return redirect('login')
