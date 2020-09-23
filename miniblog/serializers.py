from action_serializer import ModelActionSerializer
from django.contrib.auth.models import User
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import Blog, Comment


# 1
# class BlogSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     pub_date = serializers.DateTimeField()
#     name = serializers.CharField(max_length=120)
#     author_id = serializers.IntegerField()
#     author = serializers.CharField()
#     description = serializers.CharField()
#
#     def create(self, validated_data):
#         return Blog.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         # instance.pub_date = validated_data.get('pub_date', instance.pub_date)
#         # instance.author = validated_data.get('author', instance.author)
#         instance.author_id = validated_data.get('author_id', instance.author_id)
#         instance.description = validated_data.get('description', instance.description)
#         # instance.author_id = validated_data.get('author_id', instance.author_id)
#         instance.save()
#         return instance


# 2, 3+
class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'last_update', 'pub_date', 'name', 'autodescription', )

    def to_representation(self, instance):
        representation = super(BlogSerializer, self).to_representation(instance)
        representation['author'] = instance.author.username
        return representation


class BlogDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'pub_date', 'name', 'author_id', 'author', 'description', 'last_comment_date', )

    def to_representation(self, instance):
        representation = super(BlogDetailSerializer, self).to_representation(instance)
        representation['author'] = instance.author.username
        return representation


class BloggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', )

    def to_representation(self, instance):
        representation = super(BloggerSerializer, self).to_representation(instance)
        representation['birth_date'] = instance.profile.birth_date
        representation['blogs_num'] = instance.profile.blogs_num()
        return representation


class BloggerDetailSerializer(serializers.ModelSerializer):
    country = CountryField(source='profile.country', required=False)
    blogs_num = serializers.IntegerField(source='profile.blogs_num', required=False)
    birth_date = serializers.DateField(source='profile.birth_date', required=False)
    phone_number = PhoneNumberField(source='profile.phone_number', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'blogs_num', 'birth_date', 'phone_number', 'country', 'bio', )

    # def to_representation(self, instance):
    #     representation = super(BloggerDetailSerializer, self).to_representation(instance)
    #     representation['blogs_num'] = instance.profile.blogs_num()
    #     representation['birth_date'] = instance.profile.birth_date
    #     representation['country'] = str(instance.profile.country)
    #     representation['phone_number'] = instance.profile.phone_number
    #     representation['bio'] = instance.profile.bio
    #     return representation


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'pub_date', )

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        representation['author'] = instance.author.username
        representation['commented_blog'] = instance.commented_blog.name
        return representation


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'pub_date', )

    def to_representation(self, instance):
        representation = super(CommentDetailSerializer, self).to_representation(instance)
        representation['author'] = instance.author.username
        representation['commented_blog'] = instance.commented_blog.name
        representation['description'] = instance.description
        return representation


class BloggerActionSerializer(ModelActionSerializer):
    country = CountryField(source='profile.country', required=False)
    blogs_num = serializers.IntegerField(source='profile.blogs_num', required=False)
    birth_date = serializers.DateField(source='profile.birth_date', required=False)
    phone_number = PhoneNumberField(source='profile.phone_number', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'blogs_num', 'birth_date', 'phone_number', 'country', 'bio', )
        action_fields = {
            "list": {"fields": ('id', 'username', 'blogs_num', )},
            # "retrieve": {"fields": ('id', 'username', 'blogs_num',)},
        }