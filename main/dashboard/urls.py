from django.urls import path
from .views import *

urlpatterns = [
    # ****************************************** Dilmurod ********************************************
    # ********************** Dashboard **********************

    path("", dashboard_view, name='dashboard-url'),
    path("sign-in/", signin_view, name="login-url"),
    path("log-out/", logout_view, name="logout-url"),
    path("password/", password_view, name="password-url"),

    # ********************** Client **********************

    path('client/', client_view, name='client-url'),
    path('delete-client/<int:pk>/', delete_client_view, name='delete-client-url'),
    path('export-write-xls', export_write_xls, name='export-write-xls-url'),

    # ********************** Product **********************

    path('product/', product_view, name='product-url'),
    path('create-product/', create_product_view, name='create-product-url'),
    path('update-product/<int:pk>/', update_product_view, name='update-product-url'),
    path('delete-product/<int:pk>/', delete_product_view, name='delete-product-url'),

    # ****************************************** Odiljon ********************************************
    # ********************** Slider **********************

    path('slider/', slider_view, name='slider-url'),
    path('create-slider/', create_slider_view, name='create-slider-url'),
    path('update-slider/', update_slider_view, name='update-slider-url'),
    path('delete-slider/<int:pk>/', delete_slider_view, name='delete-slider-url'),

    # ********************** About product **********************

    path('about/', about_view, name='about-url'),
    path('create-about/', create_about_view, name='create-about-url'),
    path('update-about/', update_about_view, name='update-about-url'),
    path('delete-about/<int:pk>/', delete_about_view, name='delete-about-url'),

    # ********************** About company **********************

    path('about-company/', about_company, name='about-company-url'),
    path('create-about-company/', create_about_company, name='create-about-company-url'),
    path('update-about-company/<int:pk>/', update_about_company, name='update-about-company-url'),
    path('delete-about-company/<int:pk>/', delete_about_company, name='delete-about-company-url'),
    # ********************** Instruction **********************

    path('instruction/', instruction, name='instruction-url'),
    path('create-instruction/', create_instruction, name='create-instruction-url'),
    path('update-instruction/<int:pk>/', update_instruction, name='update-instruction-url'),
    path('delete-instruction/<int:pk>/', delete_instruction, name='delete-instruction-url'),

    # ****************************************** Sarvinoz ********************************************
    # ********************** Advice **********************
    path('advice/', advice_view, name='advice-url'),
    path('create-advice/', create_advice_view, name='create-advice-url'),
    path('update-advice/<int:pk>/', update_advice_view, name='update-advice-url'),
    path('delete-advice/<int:pk>/', delete_advice_view, name='delete-advice-url'),

    # ********************** AdviceItem **********************

    # ********************** Facts **********************
    path("fact/", facts_view, name="fact-url"),
    path("create-fact/", create_facts_view, name="create-fact-url"),
    path('update-fact/', update_facts_view, name='update-fact-url'),
    path('delete-fact/<int:pk>/', delete_facts_view, name='delete-fact-url'),
    # ********************** FactItem **********************
    path("factitem/", factsitem_view, name="factitem-url"),
    path("create-factitem/", create_factsitem_view, name="create-factitem-url"),
    path('update-factitem/', update_factsitem_view, name='update-factitem-url'),
    path('delete-factitem/<int:pk>/', delete_factsitem_view, name='delete-factitem-url'),
    # ********************** Info **********************

    path('info/', info_view, name='info-url'),
    path('update-info/<int:pk>/', update_info, name='update-info-url'),
    path('delete-info/<int:pk>/', delete_info_view, name='delete-info-url'),
    path('create-info/', create_info, name='create-info-url'),

    # ********************** Account **********************



]