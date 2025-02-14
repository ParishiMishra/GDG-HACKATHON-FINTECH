from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', include('portfolio.urls')),  # Include your app's URLs
    path('', RedirectView.as_view(url='/portfolio/dashboard/')),  # Correct the redirect URL
]
