"""geekshop URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from . import views
from authapp import urls as authapp_urls
from mainapp import urls as mainapp_urls
from basketapp import urls as basketapp_urls
from adminapp import urls as adminapp_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_staff/', include(adminapp_urls, namespace='admin_staff'), name='admin_staff'),
    path('auth/', include(authapp_urls, namespace='auth'), name='auth'),
    path('products/', include(mainapp_urls, namespace='products'), name='products'),
    path('order/', include('orderapp.urls', namespace='order'), name='order'),
    path('basket/', include(basketapp_urls, namespace='basket'), name='basket'),
    path('', views.index, name='index'),
    path('contact/', views.contacts, name='contacts'),
    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
