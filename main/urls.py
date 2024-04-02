from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("prediction", views.prediction, name="prediction"),
    path("result", views.result, name="result"),
    path("suggestions", views.suggestions, name="suggestions"),
    # path('logins',views.logins,name="logins"),
    # path('log',views.log,name="log"),
    # path('handlogin',views.handlogin,name="handlogin"),
    # path('handlogout',views.handlogout,name="handlogout")
]
