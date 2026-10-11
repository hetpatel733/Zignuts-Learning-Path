from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('tasks.urls')),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('register/', TemplateView.as_view(template_name='registration.html'), name='register_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
]
