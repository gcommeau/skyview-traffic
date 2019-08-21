from django.contrib import admin
from .models import *

admin.site.register(Classroom)

class StudentInline(admin.StackedInline):
    model = Student
    extra = 1


class FamilyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['family_number']
        }),
    ]
    inlines = [StudentInline]

admin.site.register(Family, FamilyAdmin)

admin.site.register(Student)

admin.site.register(Checkout)
