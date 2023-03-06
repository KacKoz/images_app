from django.contrib import admin
from .models import User, Tier, TierThumbnailSize
from django.contrib.auth.admin import UserAdmin

class TierThumbAdmin(admin.TabularInline):
    model = TierThumbnailSize

class TierAdmin(admin.ModelAdmin):
    inlines = [TierThumbAdmin,]
    list_display = ('name', 'original_image_access', 'expiring_link',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Tier, TierAdmin)
