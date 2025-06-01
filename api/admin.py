from django import forms
from django.contrib import admin
from .models import FlightLocation, FlightPoint, UniversityModel

admin.site.site_header = '3D Університет'
admin.site.site_title = 'Admin 3D Uni'
admin.site.index_title = 'Панель управління'


class FlightPointInline(admin.TabularInline):
    model = FlightPoint
    extra = 0
    fields = ('id', 'position_x', 'position_y', 'position_z')


@admin.register(FlightLocation)
class FlightLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'flight_type')
    list_filter = ('flight_type', 'camera_view_direction')
    search_fields = ('name', 'title', 'description')

    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'title', 'description', 'image', 'flight_type', 'speed',
                       'camera_view_direction', 'camera_pitch'),
        }),
        ('Положення камери', {
            'fields': ('position_x', 'position_y', 'position_z'),
        }),
        ('Орієнтація камери', {
            'fields': ('yaw', 'pitch'),
        }),
    )
    inlines = [FlightPointInline]

    class Media:
        js = ('display.js',)


class UniversityModelForm(forms.ModelForm):
    class Meta:
        model = UniversityModel
        fields = '__all__'

    def clean_model_file(self):
        file = self.cleaned_data.get('model_file')
        if not file.name.endswith(('.glb',)):
            raise forms.ValidationError('Підтримуються тільки .glb файли')
        return file


@admin.register(UniversityModel)
class UniversityModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'updated_at', 'is_active')
    list_display_links = ('version',)
    list_filter = ('is_active', 'updated_at')
    search_fields = ('version',)
    actions = ['make_active']

    def make_active(self, request, queryset):
        UniversityModel.objects.update(is_active=False)
        queryset.update(is_active=True)
        self.message_user(request, "Обрана модель активована")

    make_active.short_description = "Зробити обрану модель активною"
