from chartauditor.accounts import views
from django.urls import path

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('profile/', views.CompanyInfoView.as_view(), name='profile'),
    path('update-profile/', views.UpdateCompanyInfoView.as_view(), name='update_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path("<uuid:uuid>/", views.ActivateUser.as_view(), name="confirm_user"),
]

