import datetime

from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models import TextField, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Надо бы переместить модель в accounts
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def blogs_num(self):
        return self.user.blog_set.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Blog(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a blog title")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    description = TextField(max_length=1000)

    class Meta:
        ordering = ['-pub_date']
        # default_related_name = 'blogs'

    def __str__(self):
        return '{} ({})'.format(self.name, self.author)

    def last_comment_date(self):
        last_comment = self.comment_set.last()
        return last_comment.pub_date if last_comment else None

    def last_update(self):
        last_comment = self.comment_set.last()
        # updates_list = [last_comment.pub_date if last_comment else None, self.pub_date]
        # return next(date for date in updates_list if date)
        return last_comment.pub_date if last_comment else self.pub_date

    def get_absolute_url(self):
        return reverse('blog-detail', args=[self.id])


class Comment(models.Model):
    commented_blog = models.ForeignKey('Blog', null=False, on_delete=models.CASCADE)
    description = TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())

    def __str__(self):
        d = self.description
        return '{} ({})'.format(d[:15] + ("..." if len(d) > 15 else ""), self.author)

    def get_absolute_url(self):
        return reverse('comment-detail', args=[self.id])

    def display_description(self):
        return str(self.description)[:15] + ("..." if len(self.description) > 15 else "")

    display_description.short_description = "Text"



