from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="Excerpt")
    content = models.TextField(verbose_name="Content")
    image = models.ImageField(upload_to='media/blog_images/', blank=True, null=True, verbose_name="Image")
    pdf = models.FileField(upload_to='media/blog_pdfs/', blank=True, null=True, verbose_name="PDF attachment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    is_published = models.BooleanField(default=False, verbose_name="Published")
    is_pinned = models.BooleanField(
        default=False,
        verbose_name="Pin to homepage",
        help_text="Pinned published posts appear on the main page.",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']