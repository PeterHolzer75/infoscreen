# =========================================================
# Main - URL
# ========================================================
from django.contrib import admin
from django.urls import path, include
# from main import views


urlpatterns = [

    path('boendelista/', include('boendelista.urls')),
    path('kollektivtrafik/', include('kollektivtrafik.urls')),
    path('resurser/', include('resurser.urls')),

    path('infoscreen/', include('main.urls')),


    # path('busstider', include('skanetrafiken.urls')),
    path('admin/', admin.site.urls),

]
