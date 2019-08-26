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

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'classroom')
    list_filter = ['classroom']

admin.site.register(Student, StudentAdmin)

class CHeckoutAdmin(admin.ModelAdmin):
    list_display = ('checkout_time', 'checkout_type')
    list_filter = ['checkout_time', 'checkout_type']

admin.site.register(Checkout, CHeckoutAdmin)
