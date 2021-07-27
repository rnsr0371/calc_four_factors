from django.contrib import admin
from .models import Team,BasicStat,Four_Factor

# Register your models here.
admin.site.register(Team)
admin.site.register(BasicStat)
admin.site.register(Four_Factor)