from rest_framework import serializers

from src.common.models import Attachment
from src.common.serializers import AttachmentSerializer
from src.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AttachmentSerializer(required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'contact', 'customer')

    def create(self, validated_data):
        avatar = validated_data.pop('avatar', None)
        if avatar is not None:
            print('CREATE CALLED: ', avatar)
            attachment = Attachment(**avatar)
            profile = Profile.objects.create(avatar=attachment, **validated_data)
        else:
            profile = Profile.objects.create(**validated_data)
        return profile
