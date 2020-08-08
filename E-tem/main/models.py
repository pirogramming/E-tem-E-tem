from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Powerpoint(models.Model):
    img_src = models.URLField()
    download_link = models.TextField(blank=True, null=True)
    detail_page = models.TextField(blank=True, null=True)
    # color_tag = models.TextField(blank=True, null=True)
    # id = models.IntegerField(primary_key=True, blank=True)

    class Meta:
        db_table = 'pptbizcam_real'

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    user_num = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # ppt_cart = models.ManyToManyField(Powerpoint)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    template = models.ForeignKey(Powerpoint, on_delete=models.CASCADE, related_name='template')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("template", "cart"),)

    def __str__(self):
        return self.template

class Recent(models.Model):
    user_num = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    recent_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.recent_id

class RecentItem(models.Model):
    template_recent = models.ForeignKey(Powerpoint, on_delete=models.CASCADE, related_name='template_recent')
    recent = models.ForeignKey(Recent, on_delete=models.CASCADE)

    def __str__(self):
        return self.template_recent



class Download_List(models.Model):
    download_id = models.CharField(max_length=100, blank=True)
    user_num = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.download_id

class Download_Item(models.Model):
    templates = models.ForeignKey(Powerpoint, on_delete=models.CASCADE, related_name='templates')
    download = models.ForeignKey(Download_List, on_delete=models.CASCADE)

    def __str__(self):
        return self.templates


class Color_tag(models.Model):
    color = models.CharField(max_length=100, db_index=True)

class PPT_tag(models.Model):
    template = models.ForeignKey(Powerpoint, on_delete=models.CASCADE)
    ppt_tag = models.ForeignKey(Color_tag, on_delete=models.CASCADE)

class Myinfo(models.Model):
    pass

