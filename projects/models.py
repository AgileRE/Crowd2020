from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model

from django.db.models.signals import pre_save
from django.urls import reverse
from django.dispatch import receiver

from PIL import Image

from .utils import unique_slug_generator


User = get_user_model()


class ProjectView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Asset(models.Model):
    image = models.ImageField(upload_to='assets')

    def save(self, *args, **kwargs):
        super(Asset, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 800:
            output_size = (600, 800)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class RequirementCategory(models.Model):
    RCategories = (
    ('Functional', 'Functional'),
    ('NonFunctional', 'Non functional'),
    ('Others', 'Others'),)
    Categories2 = (
    ('UserRequirement', 'User Requirement'),
    ('SystemRequirement', 'System Requirement'),)

    def __str__(self):
        return self.r_cat

class Requirement(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('D', 'Declined')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    category  = models.CharField(max_length=14, choices=RequirementCategory.RCategories ,null=False, blank=True)
    choose = models.CharField(max_length=18, choices=RequirementCategory.Categories2 ,null=False, blank=True)
    content = models.TextField()
    project = models.ForeignKey(
        'Project', related_name='requirements', on_delete=models.CASCADE)
    status = models.CharField(max_length=2,
                              choices=STATUS,
                              default='P', 
                              blank=True,
                              null=True,)

    def __str__(self):
        return self.content


class Project(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = HTMLField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='assets', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    status_open = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

        if self.thumbnail:
            img = Image.open(self.thumbnail.path)

            if img.height > 600 or img.width > 800:
                output_size = (600, 800)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('project-update', kwargs={
            'pk': self.pk
        })

    def get_close_url(self):
        return reverse('project-close', kwargs={
            'pk': self.pk
        })

    @property
    def get_requirements(self):
        return self.requirements.all().order_by('-timestamp')

    @property
    def requirement_count(self):
        return Requirement.objects.filter(project=self).count()

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def view_count(self):
        return ProjectView.objects.filter(project=self).count()

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Project)