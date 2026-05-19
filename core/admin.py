from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import SiteConfig, Skill, Project, Service, Testimonial, ContactMessage


# ── SiteConfig ────────────────────────────────────────────────────────
@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🪪 Identité', {
            'fields': ('nom_complet', 'titre', 'phrase_accroche', 'bio', 'photo', 'photo_preview'),
        }),
        ('📍 Localisation & Langues', {
            'fields': ('localisation', 'langues'),
        }),
        ('🔗 Liens & Contact', {
            'fields': ('email', 'github', 'linkedin', 'twitter', 'cv'),
        }),
        ('📊 Statistiques', {
            'fields': ('annees_experience', 'projets_realises', 'clients_satisfaits'),
        }),
    )
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:100px;height:100px;object-fit:cover;'
                'border-radius:50%;border:3px solid #6c63ff" />',
                obj.photo.url,
            )
        return mark_safe('<span style="color:#888">Aucune photo</span>')
    photo_preview.short_description = 'Aperçu photo'

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Skill ─────────────────────────────────────────────────────────────
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display    = ('nom', 'categorie', 'pourcentage_bar', 'icone', 'ordre')
    list_editable   = ('ordre',)
    list_filter     = ('categorie',)
    list_per_page   = 25
    ordering        = ('ordre',)
    search_fields   = ('nom',)

    def pourcentage_bar(self, obj):
        if obj.pourcentage >= 70:
            color = '#6c63ff'
        elif obj.pourcentage >= 40:
            color = '#00d4ff'
        else:
            color = '#ff6b6b'
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px">'
            '<div style="width:140px;background:#1a1a2e;border-radius:4px;overflow:hidden">'
            '<div style="width:{}%;background:{};height:8px;border-radius:4px"></div></div>'
            '<small style="color:{};font-weight:600">{}%</small></div>',
            obj.pourcentage, color, color, obj.pourcentage,
        )
    pourcentage_bar.short_description = 'Niveau'


# ── Project ───────────────────────────────────────────────────────────
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display    = ('image_thumb', 'titre', 'stack_tags', 'en_vedette', 'visible', 'ordre', 'date_creation')
    list_editable   = ('visible', 'en_vedette', 'ordre')
    list_filter     = ('visible', 'en_vedette')
    search_fields   = ('titre', 'description', 'stack')
    list_per_page   = 15
    readonly_fields = ('image_preview', 'date_creation')
    fieldsets = (
        ('📋 Infos', {
            'fields': ('titre', 'description', 'stack'),
        }),
        ('🖼️ Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('🔗 Liens', {
            'fields': ('lien_github', 'lien_demo'),
        }),
        ('⚙️ Paramètres', {
            'fields': ('ordre', 'visible', 'en_vedette', 'date_creation'),
        }),
    )

    def image_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:36px;object-fit:cover;'
                'border-radius:4px;border:1px solid #444" />',
                obj.image.url,
            )
        return mark_safe('<span style="color:#888;font-size:11px">—</span>')
    image_thumb.short_description = ''

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:400px;max-height:250px;'
                'object-fit:cover;border-radius:8px;border:2px solid #6c63ff" />',
                obj.image.url,
            )
        return mark_safe('<span style="color:#888">Aucune image</span>')
    image_preview.short_description = 'Aperçu'

    def stack_tags(self, obj):
        tags = ''.join(
            format_html(
                '<span style="background:#6c63ff22;color:#6c63ff;padding:2px 7px;'
                'border-radius:3px;margin:1px;font-size:11px;display:inline-block">{}</span>',
                s.strip(),
            )
            for s in obj.stack.split(',')[:5]
        )
        return mark_safe(tags)
    stack_tags.short_description = 'Stack'


# ── Service ───────────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ('icone', 'titre', 'visible', 'ordre')
    list_editable = ('visible', 'ordre')
    list_per_page = 20


# ── Testimonial ───────────────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('photo_thumb', 'nom_client', 'poste', 'stars_display', 'visible', 'date_ajout')
    list_editable = ('visible',)
    list_filter   = ('note', 'visible')
    list_per_page = 20

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:36px;height:36px;object-fit:cover;'
                'border-radius:50%;border:2px solid #6c63ff" />',
                obj.photo.url,
            )
        return mark_safe(
            '<div style="width:36px;height:36px;border-radius:50%;background:#1a1a2e;'
            'display:flex;align-items:center;justify-content:center;color:#6c63ff;font-size:16px">👤</div>'
        )
    photo_thumb.short_description = ''

    def stars_display(self, obj):
        filled = '★' * obj.note
        empty  = '☆' * (5 - obj.note)
        return format_html(
            '<span style="color:#f59e0b;font-size:14px">{}</span>'
            '<span style="color:#555;font-size:14px">{}</span>',
            filled, empty,
        )
    stars_display.short_description = 'Note'


# ── ContactMessage ────────────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display    = ('statut_badge', 'nom', 'email_link', 'sujet_preview', 'date')
    list_filter     = ('lu',)
    search_fields   = ('nom', 'email', 'sujet', 'message')
    readonly_fields = ('nom', 'email', 'sujet', 'message', 'date')
    list_per_page   = 20
    actions         = ['marquer_lu', 'marquer_non_lu']

    fieldsets = (
        ('👤 Expéditeur', {
            'fields': ('nom', 'email', 'date'),
        }),
        ('💬 Message', {
            'fields': ('sujet', 'message'),
        }),
    )

    def statut_badge(self, obj):
        if obj.lu:
            return format_html(
                '<span style="background:#1f2d1f;color:#4ade80;padding:3px 10px;'
                'border-radius:12px;font-size:11px;font-weight:600">✓ Lu</span>'
            )
        return format_html(
            '<span style="background:#2d1f1f;color:#f87171;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600">● Nouveau</span>'
        )
    statut_badge.short_description = 'Statut'

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = 'Email'

    def sujet_preview(self, obj):
        text = obj.sujet or obj.message
        return (text[:70] + '…') if len(text) > 70 else text
    sujet_preview.short_description = 'Sujet / Message'

    @admin.action(description='✅ Marquer comme lu')
    def marquer_lu(self, request, queryset):
        updated = queryset.update(lu=True)
        self.message_user(request, f'{updated} message(s) marqué(s) comme lu.')

    @admin.action(description='🔴 Marquer comme non lu')
    def marquer_non_lu(self, request, queryset):
        updated = queryset.update(lu=False)
        self.message_user(request, f'{updated} message(s) marqué(s) comme non lu.')

    def has_add_permission(self, request):
        return False


# ── Site branding ─────────────────────────────────────────────────────
admin.site.site_header = 'Portfolio Admin'
admin.site.site_title  = 'Portfolio'
admin.site.index_title = 'Tableau de bord'
