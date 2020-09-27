from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from articles.models import Article
from comments.api.serializers import CommentDetailSerializer, CommentInlineSerializer
from comments.models import Comment


class ArticleListSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='articles-api:article-details',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'pk',
            'uri',
            'title',
            'slug',
            'author',
            'author_uri',
            'category',
            'created',
            'updated',
            'is_active',
            'views_count',
            'comments_count'
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)

    def get_comments_count(self, obj):
        comment_qs = Comment.objects.filter(article=obj)
        return comment_qs.count()


class ArticleDetailSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='articles-api:article-details',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'pk',
            'uri',
            'title',
            'author',
            'author_uri',
            'category',
            'created',
            'updated',
            'is_active',
            'views_count',
            'comments'
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)

    def get_comments(self, obj):
        request = self.context.get('request')
        comments_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentInlineSerializer(comments_qs, many=True, context={'request': request}).data
        return comments


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'author',
            'category',
            'is_active'
        ]

    def create(self, validated_data):
        article = Article.objects.create(
            **validated_data
        )
        article.save()
        return article


class ArticleDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'created'
        ]


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'created'
        ]
