from rest_framework import serializers

from articles.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
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

    def get_comments(self, object):
        #comments = Comment.objects.all()
        return ''


class ArticleDetailSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='articles-api:article-details',
        lookup_field='slug'
    )
    author = serializers.SerializerMethodField()

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
            'views_count'
        ]

    def get_author(self, obj):
        return obj.author.username


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
        request = self.context.get('request')
        user = request.user
        article = Article.objects.create(
            #author=user,
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
