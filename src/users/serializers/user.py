from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from src.common.models import Attachment
from src.users.models import Profile, Address, UserAddress
from src.users.serializers import ProfileSerializer, AddressSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer with profile and address
    """
    profile = ProfileSerializer(required=False)
    address = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_active', 'profile', 'address', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        """
        Handler function that stores nested properties of the user serializer
        """
        all_address_data = validated_data.pop('address', None)
        profile_data = validated_data.pop('profile', None)
        avatar_data = profile_data.pop('avatar', None)
        user = User.objects.create_user(**validated_data)

        # Processing in case there is an avatar file
        if avatar_data:
            attachment = Attachment.objects.create(**avatar_data)
            Profile.objects.create(customer=user, **profile_data, avatar=attachment)
        else:
            Profile.objects.create(customer=user, **profile_data)
        if all_address_data:
            # Multiple addresses are create
            for address in all_address_data:
                user_address_data = address.pop('address', None)
                user_address = UserAddress.objects.create(**user_address_data)
                Address.objects.create(customer=user, **address, address=user_address)
        return user

    def update(self, instance, validated_data):
        """
        Handler function that updates nested properties of the user serializer
        """
        profile_data = validated_data.pop('profile')
        address_data = validated_data.pop('address')
        super(UserSerializer, self).update(instance, validated_data)
        profile = instance.profile
        avatar_data = profile_data.pop('avatar', None)

        # Update in case there is an avatar file
        if avatar_data:
            avatar = profile.avatar
            avatar.thumbnail = avatar_data.get('thumbnail', avatar.thumbnail)
            avatar.original = avatar_data.get('original', avatar.original)
            avatar.save()
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Register user serializer
    """
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_password(self, value):
        # user django's password validator to validate password value
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    """
    User password change serializer
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    error_message = {
        'not_match': "Old password is not match"
    }

    def validate_old_password(self, value):
        print('CONTEXT: ', self.context)
        request = self.context['request']
        user = request.user
        # check old user password
        if not user.check_password(value):
            raise serializers.ValidationError(detail=self.error_message['not_match'], code='not_match')

    def validate_new_password(self, value):
        # user django's password validator to validate new password value
        password_validation.validate_password(value)
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    """
    User password reset serialzer contain fields which in order to assign for link is sent to user
    """
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    default_error_messages = {
        'invalid': "The reset link is invalid"
    }

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        # Check token in request
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(detail=self.error_messages['invalid'], code='invalid')

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed(detail=self.error_messages['invalid'], code='invalid')
        return super(ResetPasswordSerializer, self).validators(attrs)
