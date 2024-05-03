from rest_framework import serializers
from .models import *

class AktyorSerializers(serializers.Serializer):
    ism=serializers.CharField()
    t_sana=serializers.DateField()
    davlat=serializers.CharField()
    jins=serializers.CharField()



class TarifSerializers(serializers.Serializer):
    nom=serializers.CharField()
    davomiylik=serializers.CharField()
    narx=serializers.IntegerField()

class KinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = '__all__'

    def to_representation(self, instance):
        kino=super(KinoSerializer,self).to_representation(instance)
        soni=Izoh.objects.filter(kino__id=kino["id"]).count()
        kino.update({"izohlar_soni":soni})
        return kino

class KinoAktyorSerializer(serializers.ModelSerializer):
    class Meta:
        model=KinoAktyor
        fields='__all__'



class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model=Izoh
        fields='__all__'

class AktyorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Aktyor
        fields='__all__'

    def to_representation(self, instance):
        aktyor=super(AktyorSerializer,self).to_representation(instance)
        soni=KinoAktyor.objects.filter(aktyor__id=aktyor["id"]).count()
        aktyor.update({"Kinolar_soni":soni})
        return aktyor






