from django.contrib import admin

from detection.models import Detection

class TomatoDetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_image', 'result_image', 'created_at')

admin.site.register(Detection, TomatoDetectionAdmin)