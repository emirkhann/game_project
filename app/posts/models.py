from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import ValidationError
import random

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True, unique=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    tag = models.ManyToManyField("Tag", related_name='product')
  
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user','product')

    def __str__(self) -> str:
        return f'liked by {self.user.username}'
    

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    #u1 = User.objects.get(id=1)
    #u1.comments.all()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # не существующий коментарий
    updated_at = models.DateTimeField(auto_now=True) # существующий коментарий 
    sub_comment = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null = True)# не обязательно к заполнению blank true
    article = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
    def __str__(self) -> str:
        return f'Комментарий от {self.user.username}'

class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
    
class Purchase(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posts = models.ForeignKey(Product, blank=True, on_delete=models.CASCADE)

    def clean(self):
        if self.posts.count() > settings.MAX_FAVORITES_POSTS:
            raise ValidationError('Favorites limit exceeded.')
        
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


    
