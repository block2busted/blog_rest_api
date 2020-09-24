from rest_framework import serializers

from categories.models import Category
from articles.models import Article


class CategoryListSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='categories-api:category-details',
        lookup_field='slug'
    )
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'pk',
            'uri',
            'article_count',
            'title',
            'description',
            'image'
        ]

    def get_image(self, obj):
        try:
            return obj.image
        except:
            return None


    def get_article_count(self, obj):
        return ''


class CategoryDetailSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='categories-api:category-details',
        lookup_field='slug'
    )
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'pk',
            'uri',
            'article_count',
            'title',
            'description',
            'image'
        ]

    def get_article_count(self):
        return