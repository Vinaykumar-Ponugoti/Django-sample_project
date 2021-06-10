from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("checkslot", views.checkslot, name="checkslot"),
    path("cancelslot", views.cancelslot, name="cancelslot"),
    path("administrator", views.administrator, name="administrator"),
    path("blockslots", views.blockslots, name="blockslots"),
    path("checkout", views.checkout, name="checkout"),
    path("newslots", views.newslots, name="newslots"),
    path("operator", views.operator, name="operator"),
    path("<str:carid>", views.paid, name="paid")
]