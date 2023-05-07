from rest_framework import serializers
from .models import Product
from .models import Product,Like,Comment,Tag,Purchase
from .models import Favorite


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductListSerializer(serializers.ListSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'tag', 'user')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','title']




class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length = None, use_url=True)
    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    tags = TagSerializer(many=True)
    class Meta:
        model = Product # моедль которую нужно сериализовать 
        fields = '__all__'
        read_only_fields = ['user', 'id'] # те данные которые джанго не запрашивать 
        list_serializer_class = ProductListSerializer
    
    def get_likes_count(self, instance) -> int:
        return Like.objects.filter(product=instance).count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'text', 'created_at', 'updated_at', 'sub_comment')
        read_only_fields = ['article']



class PurchaseSerializer(serializers.ModelSerializer):
    posts = ProductListSerializer

    
    class Meta:
        model =Purchase
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    is_favorite = serializers.BooleanField(read_only=True)


    class Meta:
        model = Favorite
        fields = '__all__'

