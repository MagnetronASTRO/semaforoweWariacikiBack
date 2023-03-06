from rest_framework import serializers
from .models import Event, Category, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        image = Image.objects.create(**image_data)
        return Event.objects.create(image=image, **validated_data)
