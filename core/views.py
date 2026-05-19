from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import requests as http_requests

from .models import SiteConfig, Skill, Project, Service, Testimonial, ContactMessage


def _send_contact_email(nom, email, sujet, message, recipient):
    api_key = getattr(settings, 'RESEND_API_KEY', '')
    if not api_key:
        return
    subject = f'[Portfolio] Nouveau message de {nom}' + (f' — {sujet}' if sujet else '')
    body = f'De : {nom} <{email}>\n\n{message}'
    http_requests.post(
        'https://api.resend.com/emails',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'from': 'Portfolio Contact <onboarding@resend.dev>',
            'to': [recipient],
            'subject': subject,
            'text': body,
        },
        timeout=10,
    )


def get_site_config():
    config, _ = SiteConfig.objects.get_or_create(pk=1)
    return config


def index(request):
    config = get_site_config()
    skills_by_cat = {}
    for skill in Skill.objects.all():
        skills_by_cat.setdefault(skill.get_categorie_display(), []).append(skill)

    context = {
        'config': config,
        'skills': Skill.objects.all(),
        'skills_by_cat': skills_by_cat,
        'projects': Project.objects.filter(visible=True),
        'services': Service.objects.filter(visible=True),
        'testimonials': Testimonial.objects.filter(visible=True),
    }
    return render(request, 'core/index.html', context)


@require_POST
def contact(request):
    try:
        data = json.loads(request.body)
        nom = data.get('nom', '').strip()
        email = data.get('email', '').strip()
        sujet = data.get('sujet', '').strip()
        message = data.get('message', '').strip()

        if not all([nom, email, message]):
            return JsonResponse({'success': False, 'error': 'Champs requis manquants.'}, status=400)

        if len(message) < 10:
            return JsonResponse({'success': False, 'error': 'Message trop court.'}, status=400)

        msg = ContactMessage.objects.create(nom=nom, email=email, sujet=sujet, message=message)

        try:
            config = get_site_config()
            _send_contact_email(nom, email, sujet, message, config.email)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error('Email send failed: %s', e)

        return JsonResponse({'success': True, 'message': 'Message envoyé avec succès !'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Données invalides.'}, status=400)


def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)
