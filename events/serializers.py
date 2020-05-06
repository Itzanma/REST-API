from rest_framework import serializers

from events.models import Event, Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    """
        Serialiazador de speakers de eventos
    """

    class Meta:
        model = Speaker
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    """
        Serializador para los eventos
    """
    speakers = serializers.ListSerializer(
        child=serializers.CharField(source='speakers.name', read_only=True)
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'speakers', 'image', 'slug', 'day')


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'description', 'speakers', 'image', 'day')
