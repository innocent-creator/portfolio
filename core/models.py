from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SiteConfig(models.Model):
    nom_complet = models.CharField(max_length=100, default='Innocent ATCHA')
    titre = models.CharField(max_length=150, default='Développeur Web Fullstack')
    phrase_accroche = models.TextField(default="Je construis des applications web performantes et élégantes.")
    bio = models.TextField(default='Passionné par le développement web, je crée des solutions digitales sur mesure depuis le Bénin.')
    localisation = models.CharField(max_length=100, default='Cotonou, Bénin 🇧🇯')
    langues = models.CharField(max_length=200, default='Français, Anglais')
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(default='innocentatcha32@gmail.com')
    github = models.URLField(blank=True, default='https://github.com')
    linkedin = models.URLField(blank=True, default='https://linkedin.com')
    twitter = models.URLField(blank=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    annees_experience = models.PositiveIntegerField(default=3)
    projets_realises = models.PositiveIntegerField(default=20)
    clients_satisfaits = models.PositiveIntegerField(default=15)

    class Meta:
        verbose_name = 'Configuration du site'
        verbose_name_plural = 'Configuration du site'

    def __str__(self):
        return self.nom_complet

    def save(self, *args, **kwargs):
        if not self.pk and SiteConfig.objects.exists():
            return
        super().save(*args, **kwargs)


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Base de données'),
        ('devops', 'DevOps & Outils'),
    ]
    nom = models.CharField(max_length=50)
    pourcentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    categorie = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='backend')
    icone = models.CharField(max_length=100, blank=True, help_text='Classe CSS ou emoji')
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'Compétence'
        verbose_name_plural = 'Compétences'

    def __str__(self):
        return f'{self.nom} ({self.pourcentage}%)'


class Project(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    stack = models.CharField(max_length=300, help_text='Ex: Django, React, PostgreSQL')
    lien_github = models.URLField(blank=True)
    lien_demo = models.URLField(blank=True)
    ordre = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)
    date_creation = models.DateField(auto_now_add=True)
    en_vedette = models.BooleanField(default=False)

    class Meta:
        ordering = ['ordre', '-date_creation']
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'

    def __str__(self):
        return self.titre

    def get_stack_list(self):
        return [s.strip() for s in self.stack.split(',')]


class Service(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.CharField(max_length=10, default='⚡', help_text='Emoji ou icone')
    ordre = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.titre


class Testimonial(models.Model):
    nom_client = models.CharField(max_length=100)
    poste = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    texte = models.TextField()
    note = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    visible = models.BooleanField(default=True)
    date_ajout = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'

    def __str__(self):
        return f'{self.nom_client} — {self.note}★'

    def get_stars(self):
        return range(self.note)

    def get_empty_stars(self):
        return range(5 - self.note)


class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f'{self.nom} <{self.email}> — {self.date.strftime("%d/%m/%Y")}'
