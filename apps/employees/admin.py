from django.contrib import admin
from .models import Employeer,Task,TaskUpload

# Register your models here.
class EmploAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)#para ver o id no painel
admin.site.register(Employeer,EmploAdmin)
admin.site.register(Task)
admin.site.register(TaskUpload)