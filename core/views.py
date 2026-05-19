from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from .models import SiteConfig, Skill, Project, Service, Testimonial, ContactMessage


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
            send_mail(
                subject=f'[Portfolio] Nouveau message de {nom}' + (f' — {sujet}' if sujet else ''),
                message=f'De : {nom} <{email}>\n\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[config.email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logging.getLogger(__name__).error('Email send failed: %s', e)

        return JsonResponse({'success': True, 'message': 'Message envoyé avec succès !'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Données invalides.'}, status=400)


def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)
