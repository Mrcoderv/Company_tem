from .models import Notice, SiteSettings, SocialLink


def site_settings(request):
    """Make SiteSettings, active social links and the popup notice global."""
    return {
        "site_settings": SiteSettings.load(),
        "social_links": SocialLink.objects.filter(is_active=True),
        "popup_notice": Notice.objects.filter(is_active=True, show_as_popup=True).first(),
    }
