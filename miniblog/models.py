import datetime

from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import inflect


# Надо бы переместить модель в accounts
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    country = CountryField(blank=True)
    phone_number = PhoneNumberField(blank=True)
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
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    mod_date = models.DateTimeField(default=datetime.datetime.now())
    description = models.TextField(max_length=1000)
    # autodescription = models.CharField(max_length=100, null=True, blank=True)

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
    
    def comments_num(self):
        return self.comment_set.count()

    def get_absolute_url(self):
        return reverse('blog-detail', args=[self.id])
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.mod_date = datetime.datetime.now()
        
        return super(Blog, self).save(*args, **kwargs)  
    
    def autodescription(self):
        if self.author and self.pub_date:
            blogs_dates = sorted([blog.pub_date for blog in self.author.blog_set.all()])
            blog_position = blogs_dates.index(self.pub_date) + 1
            return self.author.username + "'s " + inflect.engine().ordinal(blog_position) + " blog"     


class Comment(models.Model):
    commented_blog = models.ForeignKey('Blog', null=False, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    mod_date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        d = self.description
        return '{} ({})'.format(d[:15] + ("..." if len(d) > 15 else ""), self.author)

    def get_absolute_url(self):
        return reverse('comment-detail', args=[self.id])

    def display_description(self):
        return str(self.description)[:15] + ("..." if len(self.description) > 15 else "")

    display_description.short_description = "Text"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.mod_date = datetime.datetime.now()
                             
        return super(Comment, self).save(*args, **kwargs)


"""
To be implemented on Helper
"""

SOME_FIELDS = ['field_1', 'field_2']


EVALUATION_RANGES_V1 = ['Low', 'Medium', 'High']

def evaluate_v1(num, values, max):
    return None if not num else values[int(num//(max/len(values)))]


EVALUATION_RANGES_V2 = {
    "Bad": range(1, 41),
    "Medium": range(41, 61),
    "Good": range(61, 81),
    "Great": range(81, 101)  
}

def evaluate_v2(num, values):
    if not num:
        return None
    for v in values:
        if num in values[v]:
            return v
        

class SomeModel(models.Model):
    name = models.CharField(max_length=128)
    field_1_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=None, null=True, blank=True)
    field_2_value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=None, null=True, blank=True)
    field_1_text = models.CharField(max_length=32, default=None, null=True, blank=True)
    field_2_text = models.CharField(max_length=32, default=None, null=True, blank=True)
    

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        this_model = self.__class__.objects.get(id=self.id)
                   
        for field in SOME_FIELDS:
            field_value = getattr(self, f'{field}_value')
            field_text = getattr(self, f'{field}_text')
            if field_value != getattr(this_model, f'{field}_value') and field_text in EVALUATION_RANGES_V1 \
                or field_value and not field_text:
                    setattr(self, f'{field}_text', evaluate_v1(field_value, EVALUATION_RANGES_V1, 100))
                                   
                             
        return super(SomeModel, self).save(*args, **kwargs)