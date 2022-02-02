"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from coolsite import settings
from women.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Функция include передаёт путь к файлу, который будет содержать маршруты
    # нашего приложения
    path('', include('women.urls')),
    path('captcha/', include('captcha.urls')),
]


# В режиме отладки когда константа DEBUG установлена в значении True, мы вот к
# urlpatterns этим маршрутам добовляем ещё один маршрут для статических данных
# графических файлов. Указывая в начале префикс(settings.MEDIA_URL)
# а затем корневую папку(document_root = settings.MEDIA_ROOT), где будут
# находится эти файлы. ВСЁ ЭТО ДЕЛАЕТ В ОТЛАДОЧНОМ РЕЖИМЕ, НА РЕАЛЬНЫХ СЕРВЕРАХ,
# ЭТОТ ПРОЦЕСС УЖЕ НАСТРОЕН

if settings.DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
                      path('__debug__/', include('debug_toolbar.urls')),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработка исключений при запросах к серверу:
# ВСЕ ОНИ РАБОТАЮТ ТОЛЬКО ТОГДА КОГДА DEBUG = False
# handler500 - Ошибка сервера;
# handler403 - доступ запрещён;
# handler400 - невозможно обработать запрос;

# Создание 301 и 302 редиректов:
# 301 - страница перемещена на другой постоянный URL-адрес;
# 302 - страница перемещена временно на другой URL-адрес;

# Мы обработчику 404(handler404) указали использовать нашу функцию(pageNotFound),
# для отоброжения не существующих страниц
handler404 = pageNotFound

