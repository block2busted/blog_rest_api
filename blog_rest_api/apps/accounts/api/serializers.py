from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label='Password'
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    def validate_username(self, value):
        user_qs = User.objects.filter(username=value)
        if user_qs.exists():
            raise serializers.ValidationError('User with this username is already exists.')
        return value

    def validate_email(self, value):
        user_qs = User.objects.filter(email=value)
        if user_qs.exists():
            raise serializers.ValidationError('This email is already exists.')
        return value

    def validate_password(self, value):
        data = self.get_initial()
        password = value
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords must match!')
        return value

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False
        # TODO: Send activation email.
        user_obj.save()
        return user_obj


class LoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username_or_email = serializers.CharField(label='Username or email.')
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username_or_email',
            'password',
            'auth_token'
        ]

    def validate(self, data):
        username_or_email = data.get('username_or_email', None)
        password = data.get('password')
        user = User.objects.filter(username=username_or_email) or User.objects.filter(email=username_or_email)
        print(user)
        if user.exists() and user.count() == 1:
            user = user.first()
        else:
            raise serializers.ValidationError('Username or email is not valid.')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials. Please try again.')
        else:
            data['auth_token'] = 'JWT in the future.'
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]