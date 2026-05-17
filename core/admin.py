from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfig, Skill, Project, Service, Testimonial, ContactMessage


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identité', {'fields': ('nom_complet', 'titre', 'phrase_accroche', 'bio', 'photo')}),
        ('Localisation & Langues', {'fields': ('localisation', 'langues')}),
        ('Liens', {'fields': ('email', 'github', 'linkedin', 'twitter', 'cv')}),
        ('Statistiques', {'fields': ('annees_experience', 'projets_realises', 'clients_satisfaits')}),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'pourcentage_bar', 'ordre')
    list_editable = ('ordre',)
    list_filter = ('categorie',)
    ordering = ('ordre',)

    def pourcentage_bar(self, obj):
        color = '#6c63ff' if obj.pourcentage >= 70 else '#00d4ff' if obj.pourcentage >= 40 else '#ff6b6b'
        return format_html(
            '<div style="width:200px;background:#1a1a2e;border-radius:4px;overflow:hidden">'
            '<div style="width:{}%;background:{};height:10px;border-radius:4px"></div></div>'
            ' <small>{}%</small>',
            obj.pourcentage, color, obj.pourcentage
        )
    pourcentage_bar.short_description = 'Niveau'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titre', 'stack_preview', 'en_vedette', 'visible', 'ordre', 'date_creation')
    list_editable = ('visible', 'en_vedette', 'ordre')
    list_filter = ('visible', 'en_vedette')
    search_fields = ('titre', 'description', 'stack')

    def stack_preview(self, obj):
        tags = ''.join(
            f'<span style="background:#6c63ff22;color:#6c63ff;padding:2px 6px;border-radius:3px;margin:1px;font-size:11px">{s.strip()}</span>'
            for s in obj.stack.split(',')[:4]
        )
        return format_html(tags)
    stack_preview.short_description = 'Stack'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icone', 'titre', 'visible', 'ordre')
    list_editable = ('visible', 'ordre')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('nom_client', 'poste', 'stars_display', 'visible', 'date_ajout')
    list_editable = ('visible',)
    list_filter = ('note', 'visible')

    def stars_display(self, obj):
        return '★' * obj.note + '☆' * (5 - obj.note)
    stars_display.short_description = 'Note'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet_preview', 'date', 'lu')
    list_editable = ('lu',)
    list_filter = ('lu',)
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('nom', 'email', 'sujet', 'message', 'date')

    def sujet_preview(self, obj):
        return obj.sujet or obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    sujet_preview.short_description = 'Sujet / Message'

    def has_add_permission(self, request):
        return False


admin.site.site_header = '🚀 Portfolio Admin'
admin.site.site_title = 'Portfolio'
admin.site.index_title = 'Tableau de bord'
