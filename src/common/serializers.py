from rest_framework import serializers

from src.common.models import Attachment, Location


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        extra_kwargs = {
            'thumbnail': {
                "required": False,
                'read_only': True
            },
            'original': {
                "required": False,
            }
        }


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
    success = serializers.BooleanField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
