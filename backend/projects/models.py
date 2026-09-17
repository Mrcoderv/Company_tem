from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Project name")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='media/project_images/', blank=True, null=True, verbose_name="Image")
    categories = models.ManyToManyField(Category, related_name='projects', verbose_name="Categories")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    is_published = models.BooleanField(default=False, verbose_name="Published")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']