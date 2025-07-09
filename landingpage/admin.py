from django.contrib import admin

# Register your models here.
from .models import BkashConfig, BkashConfiguration, BkashSettings, ExtraCharges, Gallery, Product, Purchase, Templates, Theme
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django import forms
from django.urls import path 
from solo.admin import SingletonModelAdmin


admin.site.register(Purchase)
admin.site.register(ExtraCharges)
admin.site.register(Product)
admin.site.register(Gallery)
admin.site.register(BkashConfiguration,SingletonModelAdmin)
admin.site.register(Templates,SingletonModelAdmin)

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_button')
    
    def preview_button(self, obj):
        return format_html(
            '<a class="button" href="/theme/{}/" target="_blank">Preview</a>',
            obj.id
        )

admin.site.register(Theme, ThemeAdmin)