from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import ContactMessage, Notice, SiteSettings, SocialLink, TeamMember


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"
        widgets = {
            "accent_color": forms.TextInput(attrs={"type": "color"}),
            "deep_color": forms.TextInput(attrs={"type": "color"}),
            "ink_color": forms.TextInput(attrs={"type": "color"}),
            "paper_color": forms.TextInput(attrs={"type": "color"}),
            "logo": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].help_text = (
            "Upload a PNG or JPG logo (transparent background recommended, "
            "around 160 px wide). It is shown in the site header and loading screen. "
            "Leave empty to display the company name as text."
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    list_display = ("company_name", "email", "phone", "updated_at")
    readonly_fields = ("logo_preview", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("company_name", "tagline")}),
        (
            "Logo",
            {
                "fields": ("logo", "logo_preview"),
                "description": "Upload your logo here. Leave it empty to show the company name as text.",
            },
        ),
        ("Brand colors", {"fields": ("accent_color", "deep_color", "ink_color", "paper_color")}),
        ("Contact & location", {"fields": ("address", "map_embed_url", "email", "phone", "hours")}),
        ("Footer", {"fields": ("footer_blurb", "copyright_name")}),
        (
            "Sections",
            {
                "fields": (
                    "show_services",
                    "show_team",
                    "show_blog",
                    "show_projects",
                    "show_notices",
                    "show_contact",
                ),
                "description": "Turn a section off to hide it from the menu (and the page becomes unavailable). "
                "Turn it back on any time.",
            },
        ),
        ("Meta", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    @admin.display(description="Current logo")
    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" alt="{}" style="max-height:70px;max-width:260px;'
                'border:1px solid #ddd;background:#fff;padding:6px;" />',
                obj.logo.url,
                obj.company_name,
            )
        return "No logo uploaded yet — the company name will be shown instead."

    def has_add_permission(self, request):
        # Keep this a single-row settings object: no duplicate rows.
        return not SiteSettings.objects.exists()


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "bio")
    fields = ("name", "role", "bio", "photo", "order", "is_active")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "platform")
    search_fields = ("label", "url")
    fields = ("platform", "label", "url", "order", "is_active")


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_pinned", "show_as_popup", "published_at", "has_attachment", "link")
    list_editable = ("is_active", "is_pinned", "show_as_popup")
    list_filter = ("is_active", "is_pinned", "show_as_popup")
    search_fields = ("title", "body")
    readonly_fields = ("published_at",)
    fields = ("title", "body", "attachment", "link", "is_active", "is_pinned", "show_as_popup", "published_at")

    @admin.display(boolean=True, description="File")
    def has_attachment(self, obj):
        return bool(obj.attachment)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Inbox: newest messages first, status editable straight from the list."""

    list_display = ("name", "email", "organization", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "organization", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "organization", "message", "created_at")
    list_per_page = 25

    def has_add_permission(self, request):
        # Messages arrive from the contact form on the site, not from here.
        return False