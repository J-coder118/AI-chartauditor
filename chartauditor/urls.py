from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('chartauditor.accounts.urls')),
    path('', include('chartauditor.pdf_wrapper.urls')),
    path('dashboard/', include('chartauditor.dashboard.urls')),
    path('', include('chartauditor.subscription.urls')),

    path('accounts/', include('allauth.urls')), # all OAuth operations will be performed under this route
    path('logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
