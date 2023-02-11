from django.shortcuts import render, redirect
from main.models import *
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractMonth
import calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from xlutils.copy import copy
from xlrd import open_workbook
from django.http import HttpResponse
import os
from django.views.generic.base import TemplateView
from django.db.models import Q


def signin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = authenticate(username=username, password=password)
        if usr is not None:
            login(request,usr)
            return redirect('dashboard-url')
    return render(request, 'log-in.html')


@login_required(login_url='login-url')
def password_view(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('new')
        confirm = request.POST.get('confirm')
        if password is not None:
            if password == confirm:
                user.set_password(password)
            else:
                user.save()
        user.save()
        return redirect('password-url')
    context = {
        'user': request.user
    }
    return render(request, 'change-password.html', context)


@login_required(login_url='login-url')
def logout_view(request):
    logout(request)
    return redirect('dashboard-url')

# ********** Dashboard **********
def dashboard_view(request):
    application = Client.objects.all().order_by('-id')[:7]
    count = Client.objects.all().count()
    today = datetime.today() - timedelta(days=1)
    week = datetime.today() - timedelta(days=7)
    month = datetime.today() - timedelta(days=30)
    day = Client.objects.filter(created__gte=today).count()
    weeks = Client.objects.filter(created__gte=week).count()
    months = Client.objects.filter(created__gte=month).count()
    qs = Client.objects.filter(
        created__gte=month
    ).annotate(
        day=ExtractDay("created"),
        mon=ExtractMonth('created'),
    ).values(
        'day', 'mon'
    ).annotate(
        n=Count('pk')
    ).order_by('mon')
    mon_list = []
    for i in qs:
        i['mon']=(calendar.month_abbr[i['mon']])
        if len(mon_list) >= 30:
            del mon_list[0]
            mon_list.append(i)
        else:
            mon_list.append(i)
    context = {
        "all_apps": application,
        "count": count,
        "day": day,
        "week": weeks,
        "month": months,
        "qs": mon_list,
    }
    return render(request, 'dashboard.html', context)


# ********** Client **********
def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get("page")
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def client_view(request):
    client = Client.objects.all().order_by('-id')
    context = {
        "client": PagenatorPage(client, 2, request)
    }
    return render(request, "clients.html", context)


def delete_client_view(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    return redirect("client-url")


class ExcelPageView(TemplateView):
    template_name = "client.html"


def export_write_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="clients.xls"'

    path = os.path.dirname(__file__)
    file = os.path.join(path, 'sample.xls')

    rb = open_workbook(file, formatting_info=True)

    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_num = 0  # index start from 0
    rows = Client.objects.all().values_list('name', 'phone', 'created')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]))

    # wb.save(file) # will replace original file
    # wb.save(file + '.out' + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(response)
    return response


# ********** Product **********
def product_view(request):
    product = Product.objects.all().order_by('-id')
    context = {
        "product": product
    }
    return render(request, "product.html", context)


def create_product_view(request):
    if request.method == "POST":
        img = request.FILES.get("img")
        name_uz = request.POST.get("name_uz")
        name_ru = request.POST.get("name_ru")
        price = request.POST.get("price")
        bonus = request.POST.get("bonus")
        Product.objects.create(
        img=img,
        name_uz=name_uz,
        name_ru=name_ru,
        price=price,
        bonus=bonus,
        )
        return redirect("product-url")


def delete_product_view(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("product-url")


def update_product_view(request, pk):
    if request.method == "POST":
        product = Product.objects.get(id=pk)
        img = request.FILES.get("img")
        name_uz = request.POST.get("name_uz")
        name_ru = request.POST.get("name_ru")
        price = request.POST.get("price")
        bonus = request.POST.get("bonus")
        is_sale = request.POST.get("is_sale")
        product.img = img
        product.name_uz = name_uz
        product.name_ru = name_ru
        product.price = price
        product.bonus = bonus
        product.is_sale = is_sale
        product.save()
        return redirect("product-url")

def slider_view(request):
    slider = Slider.objects.all()
    context = {
        "sliders": slider
    }
    return render(request, "slider.html", context)


def create_slider_view(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        comment_uz = request.POST.get("comment_uz")
        comment_ru = request.POST.get("comment_ru")
        Slider.objects.create(
        image=image,
        title_uz=title_uz,
        title_ru=title_ru,
        comment_uz=comment_uz,
        comment_ru=comment_ru,
        )
    return redirect("slider-url")


def delete_slider_view(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect("slider-url")


def update_slider_view(request):
    if request.method == "POST":
        edit_id = request.POST['edit_id']
        slider = Slider.objects.get(pk=edit_id)
        image = request.FILES.get("image")
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        comment_uz = request.POST.get("comment_uz")
        comment_ru = request.POST.get("comment_ru")
        slider.title_uz = title_uz
        slider.title_ru = title_ru
        slider.comment_uz = comment_uz
        slider.comment_ru = comment_ru
        if image is not None:
            slider.image = image
        slider.save()
    return redirect("slider-url")


# **************************************** About Product ****************************************
def about_view(request):
    context = {
        "about": About.objects.all()
    }
    return render(request, "about-item.html", context)


def create_about_view(request):
    if request.method == "POST":
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        image = request.FILES.get("image")
        About.objects.create(
        text_uz=text_uz,
        text_ru=text_ru,
        image=image
        )
        return redirect("about-url")
    return redirect("about-url")


def update_about_view(request):
    if request.method == "POST":
        edit_id = request.POST['edit_id']
        about = About.objects.get(pk=edit_id)
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        image = request.FILES.get("image")
        about.text_uz = text_uz
        about.text_ru = text_ru
        if image is not None:
            about.image = image
        about.save()
        return redirect("about-url")
    return redirect("about-url")


def delete_about_view(request, pk):
    about = About.objects.get(id=pk)
    about.delete()
    return redirect("about-url")


# **************************************** Instruction ****************************************
def instruction(request):
    context = {
        "instruction": Instruction.objects.last()
    }
    return render(request, "instruction.html", context)


def create_instruction(request):
    if request.method == "POST":
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        img = request.FILES.get("img")
        Instruction.objects.create(
        title_uz=title_uz,
        title_ru=title_ru,
        text_uz=text_uz,
        text_ru=text_ru,
        img=img,
        )
        return redirect("instruction-url")


def update_instruction(request, pk):
    if request.method == "POST":
        instruction = Instruction.objects.get(id=pk)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        img = request.FILES.get("img")
        instruction.title_uz = title_uz
        instruction.title_ru = title_ru
        instruction.text_uz = text_uz
        instruction.text_ru = text_ru
        instruction.img = img
        instruction.save()
        return redirect("instruction-url")


def delete_instruction(request, pk):
    instruction = Instruction.objects.get(id=pk)
    instruction.delete()
    return redirect("instruction-url")


# **************************************** About Company ****************************************
def about_company(request):
    context = {
        'company': AboutCompany.objects.all()
    }
    return render(request, "about-company.html", context)


def create_about_company(request):
    if request.method == "POST":
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        img = request.FILES.get("photo")
        AboutCompany.objects.create(
        title_uz=title_uz,
        title_ru=title_ru,
        text_uz=text_uz,
        text_ru=text_ru,
        img=img,
        )
    return redirect("about-company-url")


def update_about_company(request, pk):
    if request.method == "POST":
        about_company = AboutCompany.objects.get(id=pk)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        text_uz = request.POST.get("text_uz")
        text_ru = request.POST.get("text_ru")
        img = request.FILES.get("img")
        about_company.title_uz = title_uz
        about_company.title_ru = title_ru
        about_company.text_uz = text_uz
        about_company.text_ru = text_ru
        about_company.img = img
        about_company.save()
    return redirect("about-company-url")


def delete_about_company(request, pk):
    about_company = AboutCompany.objects.get(id=pk)
    about_company.delete()
    return redirect("about-company-url")


def info_view(request):
    info = Info.objects.last()
    context = {
        'info': info,
    }
    return render(request, 'info.html', context)



def update_info(request):
    info = Info.objects.last()
    if request.method == "POST":
        logo = request.FILES.get("logo")
        name = request.POST["name"]
        instagram = request.POST["instagram"]
        telegram = request.POST["telegram"]
        facebook = request.POST["facebook"]
        youtube = request.POST["youtube"]
        info.name = name
        info.instagram = instagram
        info.telegram = telegram
        info.facebook = facebook
        info.youtube = youtube
        if logo is not None:
            info.logo = logo
        info.save()
        return redirect("info-url")
    return redirect("info-url")



def create_info(request):
    if request.method == "POST":
        logo = request.FILES.get("logo")
        name = request.POST["name"]
        instagram = request.POST["instagram"]
        telegram = request.POST["telegram"]
        facebook = request.POST["facebook"]
        youtube = request.POST["youtube"]
        Info.objects.create(
            logo=logo,
            name=name,
            instagram=instagram,
            telegram=telegram,
            facebook=facebook,
            youtube=youtube
        )
    return redirect('info-url')


def delete_info_view(request, pk):
    info = Info.objects.get(id=pk)
    info.delete()
    return redirect("info-url")


# ********************************* advice *********************************
def advice_view(request):
    context = {
        'advice': Advice.objects.all()
    }
    return render(request, 'advice.html', context)


def create_advice_view(request):
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        Advice.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
        )
        return redirect('advice-url')
    return redirect('advice-url')


def update_advice_view(request, pk):
    if request.method == 'POST':
        advice = Advice.objects.get(id=pk)
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        advice.title_uz = title_uz
        advice.title_ru = title_ru
        advice.save()
        return redirect('advice-url')
    return redirect('advice-url')


def delete_advice_view(requset, pk):
    advice = Advice.objects.get(id=pk)
    advice.delete()
    return redirect('advice-url')


# ********************************* adviceitem *********************************
def adviceitem_view(request):
    context = {
        'adviceitem': AdviceItem.objects.all()
    }
    return render(request, 'advice.html', context)


def create_adviceitem_view(request):
    if request.method == 'POST':
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        AdviceItem.objecgts.create(
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect('')
    return redirect('')


def update_adviceitem_view(request, pk):
    if request.method == 'POST':
        adviceitem = AdviceItem.objects.get(id=pk)
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        adviceitem.text_uz = text_uz
        adviceitem.text_ru = text_ru
        adviceitem.save()
        return redirect('')
    return redirect('')


def delete_adviceitem_view(requset, pk):
    adviceitem = AdviceItem.objects.get(id=pk)
    adviceitem.delete()
    return redirect('')


# ********************************* facts *********************************
def facts_view(request):
    context = {
        'facts': Facts.objects.all().order_by('-id')
    }
    return render(request, 'fact.html', context)


def create_facts_view(request):
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        Facts.objecgts.create(
            title_uz=title_uz,
            title_ru=title_ru,
        )
        return redirect('fact-url')
    return redirect('fact-url')


def update_facts_view(request, pk):
    if request.method == 'POST':
        facts = Facts.object.get(id=pk)
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        facts.title_uz = title_uz
        facts.title_ru = title_ru
        facts.save()
        return redirect('fact-url')
    return redirect('fact-url')


def delete_facts_view(request, pk):
    facts = Facts.objects.get(id=pk)
    facts.delete()
    return redirect('fact-url')


# ********************************* factsitem *********************************
def factsitem_view(request):
    context = {
        'factsitem': FactItem.objects.all().order_by('-id')
    }
    return render(request, 'fact.html', context)

def create_factsitem_view(request):
    if request.method == 'POST':
        number = request.POST.get("number")
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        FactItem.objecgts.create(
            number=number,
            title_uz=title_uz,
            title_ru=title_ru,
        )
        return redirect('fact-url')
    return redirect('fact-url')

def update_factsitem_view(request, pk):
    if request.method == 'POST':
        facts = FactItem.object.get(id=pk)
        number = request.POST.get("number")
        title_uz = request.POST.get("title_uz")
        title_ru = request.POST.get("title_ru")
        facts.number = number
        facts.title_uz = title_uz
        facts.title_ru = title_ru
        facts.save()
        return redirect('fact-url')
    return redirect('fact-url')

def delete_factsitem_view(request, pk):
    factsitem = FactItem.objects.get(id=pk)
    factsitem.delete()
    return redirect('fact-url')

#
# def advice(request):
#     context = {
#         'advice':Advice.objects.all('-id')
#     }
#     return render(request, 'advice.html', context)
#
#
# def create_advice(request):
#
#     return redirect('advice-url')
#
#
# def update_advice(request):
#     return redirect('advice-url')
#
#
# def delete_advice(request):
#     return redirect('advice-url')
#
#