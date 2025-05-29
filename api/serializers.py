from rest_framework import serializers
from .models import FlightLocation, FlightPoint


class FlightPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightPoint
        fields = ['position_x', 'position_y', 'position_z']


class FlightLocationSerializer(serializers.ModelSerializer):
    flight_points = FlightPointSerializer(many=True)

    class Meta:
        model = FlightLocation
        fields = [
            'name',
            'title',
            'description',
            'image',
            'flight_type',

            'speed',
            'camera_view_direction',
            'camera_pitch',

            'position_x', 'position_y', 'position_z',

            'yaw', 'pitch', 'roll',

            'flight_points'
        ]

    def to_representation(self, instance):
        data = {
            'name': instance.name,
            'title': instance.title,
            'description': instance.description,
            'flight_type': instance.flight_type,
        }

        if instance.image and hasattr(instance.image, 'url'):
            data['image'] = instance.image.url
        else:
            data['image'] = None

        if instance.flight_type == "static_frame":
            data['position_x'] = instance.position_x
            data['position_y'] = instance.position_y
            data['position_z'] = instance.position_z
            data['yaw'] = instance.yaw
            data['pitch'] = instance.pitch
            data['roll'] = instance.roll

        if instance.flight_type == "points_flight":
            data['speed'] = instance.speed
            data['camera_view_direction'] = instance.camera_view_direction
            data['camera_pitch'] = instance.camera_pitch
            data['flight_points'] = FlightPointSerializer(instance.flight_points.all(), many=True).data

        if instance.flight_type == "panorama":
            data['speed'] = instance.speed
            data['camera_pitch'] = instance.camera_pitch
            data['position_x'] = instance.position_x
            data['position_y'] = instance.position_y
            data['position_z'] = instance.position_z

        return data

class FlightLocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightLocation
        fields = ['id', 'name']
