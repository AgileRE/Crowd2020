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

class RequirementView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)

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
    ('', '--- Choose Requirement Category ---'),
    ('Functional System', 'Functional System'),
    ('Non-functional System', 'Non-functional System'),
    ('User Requirement', 'User Requirement'),
    )

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
    reqlikes = models.ManyToManyField(User, related_name='reqlikes', blank=True)
    reqdislikes = models.ManyToManyField(User, related_name='reqdislikes', blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    category = models.CharField(max_length=30, 
        choices=RequirementCategory.RCategories,
        default='',
        null=False, 
        blank=False,)
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

    
    def get_absolute_url(self):
        return reverse('requirement-detail', kwargs={
            'pk': self.pk
        })
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(requirement=self).count()

    @property
    def reqlike_count(self):
        return self.reqlikes.all().count()

    @property
    def reqdislike_count(self):
        return self.reqdislikes.all().count()


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    requirement = models.ForeignKey('Requirement', related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies' )

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "{}-{}".format(self.requirement.project, str(self.user.username))

    def children (self): #replies
        return Comment.objects.filter(parent=self)
    
    @property
    def isParent (self):
        if self.parent is not None:
            return False
        return True

         
class Project(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = HTMLField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
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
    def dislike_count(self):
        return self.dislikes.all().count()

    @property
    def view_count(self):
        return ProjectView.objects.filter(project=self).count()

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Project)