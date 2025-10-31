from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from .models import Place, PlaceImage


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 0
    fields = ("image", "preview")
    readonly_fields = ("preview",)

    @mark_safe
    def preview(self, obj: PlaceImage) -> str:
        return f'<img src="{obj.image.url}"/>' if obj.image else "Нет изображения"

    preview.allow_tags = True
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
    fieldsets = (
        (None, {"fields": ("title",)}),
        ("Описание", {"fields": ("description_short", "description_long")}),
        ("Координаты", {"fields": (("longitude", "latitude"),)}),
    )

    inlines = (PlaceImageInline,)
