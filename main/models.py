from django.db import models


class Slider(models.Model):
    image = models.ImageField(upload_to='slider/')
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    comment_uz = models.CharField(max_length=255)
    comment_ru = models.CharField(max_length=255)


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    created = models.DateField(auto_now_add=True)


class Product(models.Model):
    image = models.ImageField(upload_to="product/")
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    bonus = models.IntegerField(default=0)


class AboutCompany(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField()
    text_ru = models.TextField()
    image = models.ImageField(upload_to='about_company/')


class About(models.Model):
    text_uz = models.TextField()
    text_ru = models.TextField()
    image = models.ImageField(upload_to='about_product/')


class Advice(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)


class AdviceItem(models.Model):
    text_uz = models.CharField(max_length=255)
    text_ru = models.CharField(max_length=255)


class Instruction(models.Model):
    image = models.ImageField(upload_to='instruction/')
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.CharField(max_length=255)
    text_ru = models.CharField(max_length=255)

class Facts(models.Model):
    title_ru = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)


class FactItem(models.Model):
    number = models.CharField(max_length=255)
    text_uz = models.TextField()
    text_ru = models.TextField()


class Info(models.Model):
    logo = models.ImageField(upload_to='logo/')
    name = models.CharField(max_length=255)
    instagram = models.URLField()
    telegram = models.URLField()
    facebook = models.URLField()
    youtube = models.URLField()
