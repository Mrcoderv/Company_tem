from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import ContactMessage, Notice, TeamMember
from .sections import require_section

from blog.models import Post


def home(request):
    notices = Notice.objects.filter(is_active=True)[:3]
    pinned_posts = Post.objects.filter(is_published=True, is_pinned=True)[:3]
    return render(
        request,
        'pages/index.html',
        {'notices': notices, 'pinned_posts': pinned_posts},
    )


def about(request):
    return render(request, 'pages/about.html')


@require_section('show_services')
def services(request):
    return render(request, 'pages/services.html')


@require_section('show_team')
def team(request):
    members = TeamMember.objects.filter(is_active=True)
    return render(request, 'pages/team.html', {'team_members': members})


@require_section('show_notices')
def notices(request):
    notice_list = Notice.objects.filter(is_active=True)
    return render(request, 'pages/notices.html', {'notices': notice_list})


@require_section('show_contact')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        organization = request.POST.get('org', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email, organization=organization, message=message
            )
            messages.success(
                request,
                "Thank you — your message has been received. We'll get back to you soon.",
            )
        else:
            messages.error(
                request,
                "Please fill in your name, email and a message before sending.",
            )
        return redirect(f"{reverse('home:contact')}#contact-form")
    return render(request, 'pages/contact.html')
