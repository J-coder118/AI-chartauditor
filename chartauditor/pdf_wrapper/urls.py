from django.urls import path
from chartauditor.pdf_wrapper import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout'),
    path('chart-audit/', views.ChartCheckerView.as_view(), name='chart_audit'),
    path('chart/user/input/', views.ChartUserInputView.as_view(), name='chart_user_input'),
    path('user/cancel/chart/<int:pk>/', views.UserCancelChart.as_view(), name='user_cancel_chart'),
    path('user-report/', views.ChartListView.as_view(), name='report'),
    path('download/report/', views.DownloadsView.as_view(), name='download_report'),
]