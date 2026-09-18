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
    list_display_links = ("company_name",)
    readonly_fields = ("logo_preview", "updated_at")
    save_on_top = True
    fieldsets = (
        (
            "Brand identity",
            {
                "fields": ("company_name", "tagline"),
                "description": "The foundation of your public site. These details appear in the header, loading screen, page titles, and footer.",
            },
        ),
        (
            "Logo",
            {
                "fields": ("logo", "logo_preview"),
                "description": "Upload a transparent PNG or JPG. Leave it empty to show the company name as text.",
            },
        ),
        (
            "Brand colors",
            {
                "fields": (("accent_color", "deep_color"), ("ink_color", "paper_color")),
                "description": "Use six-digit hex colors. Changes are applied across the public site automatically.",
            },
        ),
        (
            "Contact & location",
            {
                "fields": (("email", "phone"), "address", "hours", "map_embed_url"),
                "description": "This information powers the contact page and footer.",
            },
        ),
        ("Footer", {"fields": ("footer_blurb", "copyright_name")}),
        (
            "Published sections",
            {
                "fields": (("show_services", "show_team", "show_blog"), ("show_projects", "show_notices", "show_contact")),
                "description": "Toggle sections on or off without deleting their content. Disabled sections are removed from public navigation.",
            },
        ),
        ("Last updated", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    def has_change_permission(self, request, obj=None):
        return True

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
    list_display_links = ("name",)
    list_filter = ("is_active",)
    search_fields = ("name", "role", "bio")
    ordering = ("order", "name")
    save_on_top = True
    fieldsets = (
        ("Profile", {"fields": ("name", "role", "bio", "photo")}),
        ("Publishing", {"fields": (("order", "is_active"),), "description": "Lower order numbers appear first. Turn Active off to hide this person without deleting them."}),
    )
    fieldsets = (
        ("Profile", {"fields": ("name", "role", "bio", "photo")}),
        ("Publishing", {"fields": ("order", "is_active"), "description": "Use order to control the display sequence on the public team page."}),
    )


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
