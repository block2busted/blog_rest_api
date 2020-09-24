from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from articles.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

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

    def get_uri(self, object):
        request = self.context.get('request')
        return api_reverse('articles-api:article-detail', kwargs={'pk': object.pk}, request=request)


class ArticleDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

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

    def get_uri(self, object):
        request = self.context.get('request')
        return api_reverse('articles-api:article-detail', kwargs={'pk': object.pk}, request=request)


class ArticleCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'pk',
            'title',
            'author',
            'category',
            'created',
            'updated',
            'is_active',
            'views_count'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        article = Article.objects.create(
            author=user,
            **validated_data
        )
        article.save()
        return article
