from django import forms
from django.contrib import admin
from .models import User, Tier, TierThumbnailSize, UserTier
from django.contrib.auth.admin import UserAdmin

class TierThumbAdmin(admin.TabularInline):
    model = TierThumbnailSize

class TierAdmin(admin.ModelAdmin):
    inlines = [TierThumbAdmin,]
    list_display = ('name', 'original_image_access', 'expiring_link',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Tier, TierAdmin)

class UserTierAdmin(admin.ModelAdmin):

    list_display = ['user', 'tier']

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserTierAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['tier'].label_from_instance = lambda inst: inst.name
        return form


admin.site.register(UserTier, UserTierAdmin)