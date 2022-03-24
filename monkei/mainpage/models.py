from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class hashtag(models.Model):

    nome = models.CharField(max_length=10,default=None,primary_key=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    file = models.FileField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE )
    def __str__(self):
        return f'{self.title} -- {self.id}'



class bananas(models.Model):
    id_post = models.OneToOneField(Post,blank=True,null=True,on_delete=models.CASCADE)
    banana1 = models.IntegerField(default=0)
    banana2 = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id_post}'


    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = CountryField()
    user_avatar = models.ImageField(upload_to="You/media/uploads", blank=True,null=True)
    datecreate = models.DateTimeField(default=timezone.now)
    gmail = models.CharField(max_length=100)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'state'
        verbose_name = 'User'



