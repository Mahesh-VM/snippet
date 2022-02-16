from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, ReadOnlyField
from snippetapp.models import (
    Tag,
    Snippet,
)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", 'title']


class SnippetSerializer(ModelSerializer):
    tag = TagSerializer(read_only=False, many=False)
    owner = ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = [
            "id",
            "tag",
            "content",
            "timestamp",
            "owner"
        ]

    def to_representation(self, instance):
        modified_repr = dict()
        modified_repr['id'] = instance.id
        modified_repr['tag'] = instance.tag.title
        modified_repr['content'] = instance.content
        modified_repr['timestamp'] = instance.timestamp
        modified_repr['owner'] = getattr(instance.owner, 'username')
        return modified_repr

    def create(self, validated_data):
        title = validated_data.pop('tag')
        tag_title = Tag.objects.filter(title=title['title'])
        if not tag_title.exists():
            tag_title = Tag.objects.create(**title)
        else:
            tag_title = tag_title.get(title=title['title'])
        snippet_data = Snippet.objects.create(tag=tag_title, **validated_data)
        return snippet_data

    def update(self, instance, validated_data):
        if 'tag' in validated_data:
            tag_data = validated_data.get('tag')
            tag = instance.tag
            tag_title = Tag.objects.filter(title=tag_data['title'])
            if not tag_title.exists():
                new_tag = Tag.objects.create(title=tag_data['title'])
                instance.tag = new_tag
            else:
                instance.tag = Tag.objects.get(title=tag_data['title'])
        instance.content = validated_data.get('content', instance.content)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance


class OverviewSerializer(HyperlinkedModelSerializer):
    owner = ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = [
            "url",
            "content",
            "timestamp",
            "owner",
            "tag"
        ]
