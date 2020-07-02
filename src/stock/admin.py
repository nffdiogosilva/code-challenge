from django.contrib import admin

from .models import Company, DailyPrice, Recommendation


admin.site.register(Company)
admin.site.register(DailyPrice)
admin.site.register(Recommendation)