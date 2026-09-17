from django.db import models
from django.utils.safestring import mark_safe


class SiteSettings(models.Model):
    """Single-row model so the whole site can be edited from /admin."""

    company_name = models.CharField(max_length=200, default="Pivot Risk Pvt. Ltd.")
    tagline = models.CharField(
        max_length=200, default="RISK MANAGEMENT & ADVISORY"
    )
    logo = models.ImageField(upload_to="media/site/", blank=True, null=True)

    accent_color = models.CharField(
        max_length=7, default="#c72f2b", help_text="Primary accent color (hex, e.g. #c72f2b)"
    )
    deep_color = models.CharField(
        max_length=7, default="#163d7f", help_text="Deep blue for headings & logo (hex, e.g. #163d7f)"
    )
    ink_color = models.CharField(
        max_length=7, default="#0d2349", help_text="Dark ink used for text & footer (hex, e.g. #0d2349)"
    )
    paper_color = models.CharField(
        max_length=7, default="#f4f7fb", help_text="Page background (hex, e.g. #f4f7fb)"
    )

    address = models.CharField(max_length=255, default="Kupandole, Lalitpur, Nepal")
    map_embed_url = models.URLField(
        blank=True,
        default="https://www.google.com/maps?q=Kupandole,+Lalitpur,+Nepal&output=embed",
        help_text="Google Maps embed URL for the contact page. In Google Maps: Share the place → Embed a map → copy the src URL.",
    )
    email = models.EmailField(default="hello@pivotrisk.com.np")
    phone = models.CharField(max_length=50, default="+977 1-000-0000")
    hours = models.CharField(max_length=120, default="Sunday – Friday, 10:00 – 17:00")
    footer_blurb = models.TextField(
        default="Risk management and advisory, based in Kupandole, Lalitpur. "
        "Working with organizations across Nepal.",
        help_text="Short description shown in the site footer.",
    )
    copyright_name = models.CharField(
        max_length=200, default="Pivot Risk Pvt. Ltd.", help_text="Name shown in the footer copyright line."
    )

    show_services = models.BooleanField(default=True, verbose_name="Show Services section")
    show_team = models.BooleanField(default=True, verbose_name="Show Team section")
    show_blog = models.BooleanField(default=True, verbose_name="Show Blog section")
    show_projects = models.BooleanField(default=True, verbose_name="Show Projects section")
    show_contact = models.BooleanField(default=True, verbose_name="Show Contact section")
    show_notices = models.BooleanField(default=True, verbose_name="Show Notices section")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    body = models.TextField(blank=True, verbose_name="Details")
    attachment = models.FileField(
        upload_to="media/notices/",
        blank=True,
        null=True,
        verbose_name="Attachment (PDF or image)",
        help_text="Optional. Upload a PDF or an image.",
    )
    link = models.URLField(
        blank=True, verbose_name="External link", help_text="Optional. Opens in a new tab."
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_pinned = models.BooleanField(default=False, verbose_name="Pin to top")
    show_as_popup = models.BooleanField(
        default=True,
        verbose_name="Show as popup on site load",
        help_text="If on, this notice pops up once per visit (with a preview of the attachment).",
    )
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted at")

    class Meta:
        verbose_name = "Notice"
        verbose_name_plural = "Notices"
        ordering = ["-is_pinned", "-published_at"]

    def __str__(self):
        return self.title

    @property
    def is_image(self):
        if not self.attachment:
            return False
        return self.attachment.name.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg")
        )

    @property
    def is_pdf(self):
        return bool(self.attachment) and self.attachment.name.lower().endswith(".pdf")

    @property
    def filename(self):
        if not self.attachment:
            return ""
        return self.attachment.name.rsplit("/", 1)[-1]


class SocialLink(models.Model):
    """Editable social media / external links shown on the contact page & footer."""

    PLATFORM_FACEBOOK = "facebook"
    PLATFORM_INSTAGRAM = "instagram"
    PLATFORM_LINKEDIN = "linkedin"
    PLATFORM_X = "x"
    PLATFORM_YOUTUBE = "youtube"
    PLATFORM_TIKTOK = "tiktok"
    PLATFORM_WHATSAPP = "whatsapp"
    PLATFORM_VIBER = "viber"
    PLATFORM_OTHER = "other"

    PLATFORM_CHOICES = [
        (PLATFORM_FACEBOOK, "Facebook"),
        (PLATFORM_INSTAGRAM, "Instagram"),
        (PLATFORM_LINKEDIN, "LinkedIn"),
        (PLATFORM_X, "X (Twitter)"),
        (PLATFORM_YOUTUBE, "YouTube"),
        (PLATFORM_TIKTOK, "TikTok"),
        (PLATFORM_WHATSAPP, "WhatsApp"),
        (PLATFORM_VIBER, "Viber"),
        (PLATFORM_OTHER, "Other / Website"),
    ]

    _ICONS = {
        PLATFORM_FACEBOOK: '<path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.9h2.54V9.85c0-2.51 1.49-3.9 3.77-3.9 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.44 2.9h-2.34V22c4.78-.79 8.44-4.94 8.44-9.94Z"/>',
        PLATFORM_INSTAGRAM: '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.31-1.46.72-2.12 1.38C1.35 2.67.94 3.34.63 4.13.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.79.72 1.46 1.38 2.12.66.66 1.33 1.07 2.12 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56.79-.31 1.46-.72 2.12-1.38.66-.66 1.07-1.33 1.38-2.12.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91-.31-.79-.72-1.46-1.38-2.12C21.33 1.35 20.66.94 19.87.63 19.1.33 18.22.13 16.95.07 15.67.01 15.26 0 12 0Zm0 5.84A6.16 6.16 0 1 0 12 18.16 6.16 6.16 0 0 0 12 5.84Zm0 10.16A4 4 0 1 1 12 8a4 4 0 0 1 0 8Zm6.41-10.4a1.44 1.44 0 1 1 0-2.88 1.44 1.44 0 0 1 0 2.88Z"/>',
        PLATFORM_LINKEDIN: '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0Z"/>',
        PLATFORM_X: '<path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.41l-5.8-7.58-6.64 7.58H.46l8.6-9.83L0 1.15h7.59l5.24 6.93 6.07-6.93Zm-1.29 19.5h2.04L6.49 3.24H4.3l13.31 17.41Z"/>',
        PLATFORM_YOUTUBE: '<path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19C0 8.08 0 12 0 12s0 3.92.5 5.81a3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14C24 15.92 24 12 24 12s0-3.92-.5-5.81ZM9.55 15.57V8.43L15.82 12l-6.27 3.57Z"/>',
        PLATFORM_TIKTOK: '<path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07Z"/>',
        PLATFORM_WHATSAPP: '<path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51-.17-.01-.37-.01-.57-.01-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.06 2.88 1.21 3.08.15.2 2.09 3.19 5.06 4.47.71.31 1.26.49 1.69.62.71.23 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35ZM12.04 21.5h-.01a9.42 9.42 0 0 1-4.8-1.32l-.34-.2-3.57.94.95-3.48-.22-.36a9.4 9.4 0 0 1-1.44-5.02c0-5.2 4.23-9.42 9.43-9.42 2.52 0 4.88.98 6.66 2.76a9.36 9.36 0 0 1 2.76 6.67c0 5.2-4.23 9.43-9.42 9.43Zm8.02-17.44A11.32 11.32 0 0 0 12.04.74C5.79.74.71 5.82.71 12.06c0 1.99.52 3.94 1.51 5.66L.6 23.5l5.92-1.55a11.31 11.31 0 0 0 5.52 1.41h.01c6.24 0 11.32-5.08 11.32-11.32 0-3.02-1.18-5.87-3.32-8.01Z"/>',
        PLATFORM_VIBER: '<path d="M12 2C6.48 2 2 6.04 2 11c0 2.4 1.02 4.58 2.68 6.18L4 22l4.9-1.55c.98.26 2.02.4 3.1.4 5.52 0 10-4.04 10-9S17.52 2 12 2Z"/>',
        PLATFORM_OTHER: '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm7.93 9h-3.02a15.6 15.6 0 0 0-1.1-4.9A8.03 8.03 0 0 1 19.93 11ZM12 4.04c.83 1.2 1.48 2.53 1.9 3.96h-3.8c.42-1.43 1.07-2.76 1.9-3.96ZM4.07 13h3.02c.16 1.72.55 3.37 1.1 4.9A8.03 8.03 0 0 1 4.07 13Zm3.02-2H4.07a8.03 8.03 0 0 1 4.12-4.9A15.6 15.6 0 0 0 7.09 11ZM12 19.96a13.6 13.6 0 0 1-1.9-3.96h3.8a13.6 13.6 0 0 1-1.9 3.96Zm2.35-5.96h-4.7a13.7 13.7 0 0 1 0-4h4.7a13.7 13.7 0 0 1 0 4Zm.46 4.9c.55-1.53.94-3.18 1.1-4.9h3.02a8.03 8.03 0 0 1-4.12 4.9Z"/>',
    }

    platform = models.CharField(
        max_length=20, choices=PLATFORM_CHOICES, default=PLATFORM_FACEBOOK, verbose_name="Platform"
    )
    label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Custom label",
        help_text="Optional. Overrides the platform name (useful for 'Other / Website').",
    )
    url = models.CharField(
        max_length=500,
        verbose_name="Link",
        help_text="Full link, e.g. https://facebook.com/yourpage or https://wa.me/9779800000000",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Social link"
        verbose_name_plural = "Social links"
        ordering = ["order", "id"]

    def __str__(self):
        return self.aria_label

    @property
    def aria_label(self):
        return self.label or self.get_platform_display()

    @property
    def svg(self):
        """Inner SVG markup for the chosen platform (safe, not user-supplied)."""
        return mark_safe(self._ICONS.get(self.platform, self._ICONS[self.PLATFORM_OTHER]))


class TeamMember(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    role = models.CharField(max_length=200, blank=True, verbose_name="Role")
    bio = models.TextField(blank=True, verbose_name="Short bio")
    photo = models.ImageField(upload_to="media/team_photos/", blank=True, null=True, verbose_name="Photo")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Team member"
        verbose_name_plural = "Team members"
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    STATUS_PENDING = "pending"
    STATUS_TAKEN = "taken"
    STATUS_NOT_TAKEN = "not_taken"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_TAKEN, "Action taken"),
        (STATUS_NOT_TAKEN, "Not taken"),
    ]

    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Organization")
    message = models.TextField(verbose_name="Message")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Received at")

    class Meta:
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"