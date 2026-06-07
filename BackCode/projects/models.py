from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.ImageField(upload_to='project_skill_icons/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    PROJECT_TYPE_CHOICES = [
        ('UI/UX', 'UI/UX Design'),
        ("Frontend", "Frontend Development"),
        ("Backend", "Backend Development"),
        ("Mobile", "Mobile Development"),
        ("AI_Data", 'AI & Data Development'),
        ("DevOps_Cloud", "DevOps & Cloud"),
        ("Game", "Game Development"),
        ("Cyber_Sec", "Cyber Security"),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)

    title = models.CharField(max_length=200)

    description = models.TextField()

    likes_count = models.PositiveIntegerField(default=0, editable=False)

    download_count = models.PositiveIntegerField(default=0, editable=False)

    view_count = models.PositiveIntegerField(default=0, editable=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    last_download = models.DateTimeField(
        null=True, blank=True, editable=False
    )

    image = models.ImageField(upload_to='projects_images/', blank=True, null=True)

    file = models.FileField(upload_to='projects_files/', blank=True, null=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    skills = models.ManyToManyField(Skill, related_name="projects", blank=True)

    def __str__(self):
        return self.title

    def get_user_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    def get_user_profile_photo(self):
        if self.user.avatar:
            return self.user.avatar.url
        return '/static/img/avatar.png'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True) or 'project'
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.project.title}"

class Comment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
