from django.db import models


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255, null=False)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f'{self.title}'


class Snippet(models.Model):
    tag = models.ForeignKey(Tag, related_name="tag", on_delete=models.DO_NOTHING)
    content = models.TextField(max_length=1000, null=False)
    timestamp = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('authapp.User', db_column='owner', on_delete=models.CASCADE)

    class Meta:
        ordering = ("-id",)
