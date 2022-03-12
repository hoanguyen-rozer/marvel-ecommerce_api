from rest_framework import serializers

from src.payments.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('number', 'expiry_month', 'expiry_year', 'cvv', 'email')
