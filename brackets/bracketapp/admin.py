
from django.contrib import admin
from models import Bracket,Competition

class BracketAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bracket, BracketAdmin)
admin.site.register(Competition)
