from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import requests as http_requests

from .models import SiteConfig, Skill, Project, Service, Testimonial, ContactMessage


def _build_email_bodies(nom, email, sujet, message):
    separator = '-' * 52
    sujet_line = f'📌 Sujet         : {sujet}' if sujet else ''

    text_parts = [
        separator,
        '📬 NOUVEAU MESSAGE - PORTFOLIO',
        separator,
        '',
        f'👤 Nom complet   : {nom}',
        f'📧 Email         : {email}',
    ]
    if sujet_line:
        text_parts.append(sujet_line)
    text_parts += [
        '',
        '💬 Message :',
        f'"{message}"',
        '',
        separator,
        f'Répondre à : {email}',
        'Envoyé depuis le formulaire de contact de votre portfolio',
        separator,
    ]
    text_body = '\n'.join(text_parts)

    sujet_html = f'<tr><td class="label">📌 Sujet</td><td>{sujet}</td></tr>' if sujet else ''
    html_body = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8"/>
<style>
  body{{font-family:Arial,sans-serif;background:#f4f4f4;margin:0;padding:20px}}
  .card{{background:#fff;border-radius:8px;max-width:600px;margin:0 auto;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1)}}
  .header{{background:#6c63ff;color:#fff;padding:24px 28px}}
  .header h2{{margin:0;font-size:1.2rem;font-weight:700}}
  .header p{{margin:4px 0 0;font-size:.85rem;opacity:.85}}
  .body{{padding:28px}}
  table{{width:100%;border-collapse:collapse;margin-bottom:20px}}
  td{{padding:8px 4px;font-size:.92rem;color:#333;vertical-align:top}}
  .label{{font-weight:600;white-space:nowrap;width:130px;color:#555}}
  .message-box{{background:#f8f7ff;border-left:4px solid #6c63ff;border-radius:4px;padding:16px;font-size:.93rem;color:#333;line-height:1.6;white-space:pre-wrap}}
  .footer{{background:#f0f0f0;padding:14px 28px;font-size:.8rem;color:#888;text-align:center}}
  .reply-btn{{display:inline-block;margin-top:16px;padding:10px 22px;background:#6c63ff;color:#fff;border-radius:6px;text-decoration:none;font-size:.9rem;font-weight:600}}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h2>📬 Nouveau message — Portfolio</h2>
    <p>Un visiteur vous a contacté via le formulaire</p>
  </div>
  <div class="body">
    <table>
      <tr><td class="label">👤 Nom complet</td><td>{nom}</td></tr>
      <tr><td class="label">📧 Email</td><td><a href="mailto:{email}">{email}</a></td></tr>
      {sujet_html}
    </table>
    <p style="font-weight:600;color:#555;margin-bottom:8px">💬 Message :</p>
    <div class="message-box">{message}</div>
    <a href="mailto:{email}?subject=Re: {sujet or 'Votre message'}" class="reply-btn">Répondre directement</a>
  </div>
  <div class="footer">Envoyé depuis le formulaire de contact de votre portfolio · Répondre à : {email}</div>
</div>
</body>
</html>"""

    return text_body, html_body


def _send_contact_email(nom, email, sujet, message, recipient):
    api_key = getattr(settings, 'RESEND_API_KEY', '')
    if not api_key:
        return
    subject = '[Portfolio] Nouveau message de ' + nom + (' — ' + sujet if sujet else '')
    text_body, html_body = _build_email_bodies(nom, email, sujet, message)
    http_requests.post(
        'https://api.resend.com/emails',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'from': 'Portfolio Contact <onboarding@resend.dev>',
            'to': [recipient],
            'reply_to': email,
            'subject': subject,
            'text': text_body,
            'html': html_body,
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
