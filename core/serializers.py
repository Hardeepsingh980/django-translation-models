from rest_framework import serializers
from .models import Blog
from django.conf import settings


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        languages = dict(settings.LANGUAGES)
        for language_code, language_name in languages.items():
            field_name = f'title_{language_code}'
            self.fields[field_name] = serializers.CharField(required=(language_code == settings.LANGUAGE_CODE))

        del self.fields['title']
            
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        title = instance.title
        for language_code, language_name in dict(settings.LANGUAGES).items():
            field_name = f'title_{language_code}'
            representation[field_name] = title.get(language_code, '')
        return representation
    
    def to_internal_value(self, data):
        title = {}
        for language_code, language_name in dict(settings.LANGUAGES).items():
            field_name = f'title_{language_code}'
            title[language_code] = data.get(field_name)
        data['title'] = title
        return super().to_internal_value(data)

    def get_validated_data(self, validated_data):
        title = {}
        for language_code, language_name in dict(settings.LANGUAGES).items():
            field_name = f'title_{language_code}'
            title[language_code] = validated_data.pop(field_name, None)
        validated_data['title'] = title
        return validated_data


    def create(self, validated_data):
        validated_data = self.get_validated_data(validated_data)
        blog = Blog.objects.create(**validated_data)
        return blog
    
    def update(self, instance, validated_data):
        validated_data = self.get_validated_data(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance