from django.utils.timezone import now
from rest_framework import serializers
from .models import Nsfw


class BaseNsfwSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nsfw
        fields = '__all__'


class URLNsfwSerializer(serializers.ModelSerializer):

    image = serializers.CharField()

    def create(self, validated_data):
        nsfw = Nsfw.objects.create(
            image_url=validated_data.pop('image'),
        )
        nsfw.save()
        return nsfw

    class Meta(BaseNsfwSerializer.Meta):
        model = BaseNsfwSerializer.Meta.model
        fields = BaseNsfwSerializer.Meta.fields


class Base64NsfwSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    def create(self, validated_data):
        # TODO: process base64 image to real image
        nsfw = Nsfw.objects.create(
            image=validated_data.pop('image'),  # TODO: to base64
        )
        nsfw.save()
        return nsfw

    class Meta(BaseNsfwSerializer.Meta):
        model = BaseNsfwSerializer.Meta.model
        fields = BaseNsfwSerializer.Meta.fields


class FileNsfwSerializer(serializers.ModelSerializer):

    class Meta(BaseNsfwSerializer.Meta):
        model = BaseNsfwSerializer.Meta.model
        fields = BaseNsfwSerializer.Meta.fields
