import math

from rest_framework import serializers
from .models import FlightLocation, FlightPoint


class FlightPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightPoint
        fields = ['position_x', 'position_y', 'position_z']

    def to_representation(self, instance):
        data = {'x': instance.position_x,
                'y': instance.position_z,
                'z': -instance.position_y
                }
        return data


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

            'yaw', 'pitch',

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
            data['x'] = instance.position_x
            data['y'] = instance.position_z
            data['z'] = -instance.position_y
            data['yaw'] = math.radians(instance.yaw)
            data['pitch'] = math.radians(instance.pitch)
            data['roll'] = instance.roll

        if instance.flight_type == "points_flight":
            data['speed'] = instance.speed
            data['camera_view_direction'] = instance.camera_view_direction
            data['camera_pitch'] = math.radians(instance.camera_pitch)
            data['flight_points'] = FlightPointSerializer(instance.flight_points.all(), many=True).data

        if instance.flight_type == "panorama":
            data['speed'] = instance.speed
            data['camera_pitch'] = math.radians(instance.camera_pitch)
            data['x'] = instance.position_x
            data['y'] = instance.position_z
            data['z'] = -instance.position_y

        return data


class FlightLocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightLocation
        fields = ['id', 'title']
