from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement
from rest_framework.validators import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )
    in_favorite = UserSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'in_favorite')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        open_limit = 10
        if data.get('status') == 'OPEN':
            open_counter = Advertisement.objects.filter(
                status='OPEN',
                creator=self.context['request'].user
                ).count()
            if open_counter >= open_limit:
                raise ValidationError('У Вас достигнут лимит открытых объявлений')

        return data
