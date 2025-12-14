from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ core 앱의 urls.py를 포함
    path("", include("core.urls")),
]
