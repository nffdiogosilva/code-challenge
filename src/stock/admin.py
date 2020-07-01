from django.contrib import admin

from .models import Company, DailyPrice


admin.site.register(Company)
admin.site.register(DailyPrice)