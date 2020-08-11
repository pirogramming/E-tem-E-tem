from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

from .models import *

class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(ColorTag, BoardAdmin)
admin.site.register(PPT_tag, BoardAdmin)
