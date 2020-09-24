from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse


from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'article',
            'created',
            'parent',
            'content',
        ]


class CommentChildSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'created',
            'content',
        ]

    def get_author(self, obj):
        return obj.author.username


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    article = serializers.HyperlinkedRelatedField(
        view_name='articles-api:article-details',
        lookup_field='slug',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'article',
            'created',
            'content',
            'replies'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.get_children(), many=True).data
        return None

    def get_author(self, obj):
        return obj.author.username
