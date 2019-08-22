from rest_framework import serializers

from charge.models import Facility, Battery


class FacilitySerializer(serializers.ModelSerializer):
    slots1 = serializers.CharField(source='get_slots1_display')
    slots2 = serializers.CharField(source='get_slots2_display')
    slots3 = serializers.CharField(source='get_slots3_display')
    slots4 = serializers.CharField(source='get_slots4_display')
    slots5 = serializers.CharField(source='get_slots5_display')
    slots6 = serializers.CharField(source='get_slots6_display')


    class Meta:
        model = Facility
        fields = '__all__'


    def to_representation(self, instance):
        ret=super().to_representation(instance)
        ret.pop('addr')
        return ret



class BatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Battery
        fields = '__all__'
