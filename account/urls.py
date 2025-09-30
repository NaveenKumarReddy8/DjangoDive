from account.views import login
from django.urls import path

app_name = "account"

urlpatterns = [path("/login", login, name="login")]
