from django.contrib import admin
from chartauditor.accounts.models import User, CompanyInformation, FacultyOption


class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'first_name', 'email',)

    ordering = ['-id']
    list_display = ['id', 'first_name', 'email',]


admin.site.register(User, UserAdmin)

admin.site.register(CompanyInformation)
admin.site.register(FacultyOption)

