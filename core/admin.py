from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

    readonly_fields = [
        "created_at",
        "modified_at",
    ]
