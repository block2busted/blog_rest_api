from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from comments.models import Comment

User = get_user_model()


def create_comment_serializer(model_type='articles', slug=None, parent_pk=None, user=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField()

        class Meta:
            model = Comment
            fields = [
                'pk',
                'author',
                'parent',
                'content',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_pk:
                parent_qs = Comment.objects.filter(pk=parent_pk)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError('Not valid content type!')
            some_model = model_qs.first().model_class()
            obj_qs = some_model.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError('Not a valid slug for this content type!')
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type,
                slug=slug,
                user=user,
                content=content,
                parent_obj=parent_obj
            )
            return comment

        def get_author(self, obj):
            return obj.author.username

    return CommentCreateSerializer


class CommentInlineSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'author_uri',
            'created',
            'content',
            'reply_count',
            'replies'
        ]

    def get_replies(self, obj):
        request = self.context.get('request')
        if obj.is_parent:
            return CommentChildSerializer(obj.get_children(), many=True, context={'request': request}).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.get_children().count()
        return 0

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)


class CommentChildSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'author_uri',
            'created',
            'content',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()
    article = serializers.HyperlinkedRelatedField(
        view_name='articles-api:article-details',
        lookup_field='slug',
        read_only=True
    )
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'author_uri',
            'article',
            'created',
            'content',
            'reply_count',
            'replies'
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.get_children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.get_children().count()
        return 0


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_uri = serializers.SerializerMethodField()
    article = serializers.HyperlinkedRelatedField(
        view_name='articles-api:article-details',
        lookup_field='slug',
        read_only=True
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'pk',
            'author',
            'author_uri',
            'article',
            'created',
            'content',
            'replies',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_author_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('accounts-api:profile', kwargs={'username': obj.author.username}, request=request)

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.get_children(), many=True).data
        return None