from django.urls import path
from .views import *


urlpatterns = [
    path("slider/", slider),#
    path("client/", client),#
    path("product/", product),
    path("about-product/", about_product),
    path("advice/", advice),
    path("advice-item/", advice_item),
    path("instruction/", instruction),
    path("facts/", facts),
    path("factitem/", factitem),
    path("info/", info),#
]