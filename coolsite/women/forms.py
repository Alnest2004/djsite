from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
    # Когда созадётся экземпляр формы AddPostForm(как раз таки когда форма ото
    # бражается этот экземпляр и создаётся), то вызывается конструктор __init__
    # который обязательно должен вызвать конструктор базового класса ModelForm
    # что бы были выполнены все автоматические действия,а далее мы для поля
    # 'cat' меняем свойство empty_label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        # делает связь с этой формой AddPostForm с моделью Women
        model = Women
        # Тут говорится какие поля нужно отобразить в форме. В данном случаи все,
        # КРОМЕ тех которые заполняются автоматически
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # указаываем для какого поля какие стили нужно применить
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО ВАЛИДАТОРА!!
    def clean_title(self):
        # получаем данные по заголовку. Как я понял данные уже проверенные
        # встроенным валидатором или скорее всего тем которым мы написали в models.py это
        # например unique=True
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        # модель User это модель которая работает с таблицей auth_user в бд
        model = User
        # поля которые будут отображаться в нашей форме
        fields = ('username', 'email', 'password1', 'password2')
        # оформление для каждого из этих полей
        # widgets = {
        #     # Название этих полей можно узнать из админки(просмотреть код
        #     # конкретного элемента и там например для пароля имя будет
        #     # password1, для подтверждения пароля будет password2 и тд)
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class':'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        # }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))

# forms.Form - Общий класс для формы
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}))
    captcha = CaptchaField()



    # widget - через него можно передавать стили к отдельным полям. К которому
    # присваивается класс(TextInput) с соответствующими атрибутами
    # title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label="URL")
    # Формирует текстовое поле на основе Textarea из html. Так же Textarea передаём
    # свои атрибуты через словарь.
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
    # формирует чек бокс. required=False - делает поле не обязательным. initial=True
    # - делает по умолчанию чек бокс отмеченным
    # is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
    # Будет показывать выпадающий список где мы сможем выбирать соответствующуюю
    # категорию. Список будет формироваться на основе queryset.
    # empty_label - будет показываться вместо этих чёрточек -------. То есть по умолчанию
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")
