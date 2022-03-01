from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField('Text')
    title = models.CharField('Title', max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category} :: {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1600)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    approved = models.BooleanField('Approved', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.datetime}'
