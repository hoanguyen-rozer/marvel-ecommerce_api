from rest_framework import serializers

from src.common.models import Attachment, Location


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Attachment model serializer
    """

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
    """
        Location model serializer
    """

    class Meta:
        model = Location
        fields = '__all__'


class TokenObtainPairResponseSerializer(serializers.Serializer):
    """
    Format template for token pair class in Swagger UI
    """
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class NotificationSerializer(serializers.Serializer):
    """
    Format template for notification is returned in Swagger UI
    """
    message = serializers.CharField()
    success = serializers.BooleanField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
