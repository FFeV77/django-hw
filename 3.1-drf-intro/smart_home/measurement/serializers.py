from rest_framework import serializers

from measurement.models import Measurement, Sensor


class MeasurementSerialazer(serializers.ModelSerializer):

    class Meta():
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorDetailSerialaizer(serializers.ModelSerializer):
    measurements = MeasurementSerialazer(read_only=True, many=True)

    class Meta():
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']


class MeasurementAddSerialazer(serializers.ModelSerializer):
    class Meta():
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image']


class SensorSerialaizer(serializers.ModelSerializer):
    class Meta():
        model = Sensor
        fields = ['id', 'name', 'description']

