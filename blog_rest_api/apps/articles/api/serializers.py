from rest_framework import serializers

from articles.models import Article
from comments.api.serializers import CommentDetailSerializer, CommentInlineSerializer
from comments.models import Comment


class ArticleListSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='articles-api:article-details',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'pk',
            'uri',
            'title',
            'slug',
            'author',
            'category',
            'created',
            'updated',
            'is_active',
            'views_count',
            'comments_count'
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_comments_count(self, obj):
        comment_qs = Comment.objects.filter(article=obj)
        return comment_qs.count()


class ArticleDetailSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='articles-api:article-details',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'pk',
            'uri',
            'title',
            'author',
            'category',
            'created',
            'updated',
            'is_active',
            'views_count',
            'comments'
        ]

    def get_author(self, obj):
        return obj.author.username

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
