from rest_framework.response import Response
from rest_framework.views import APIView
from  .models import *
from .serializers import *
class HelloAPI(APIView):
    def get(self,request):
        data={
            "massage":"Hello World"
        }
        return Response(data)


class AktyorlarAPI(APIView):
    def get(self,request):
        aktyorlar=Aktyor.objects.all()
        serializer=AktyorSerializers(aktyorlar,many=True)
        return Response(serializer.data)

    def post(self,request):
        aktyor=request.data
        serializer=AktyorSerializers(data=aktyor)
        if serializer.is_valid():
            data=serializer.validated_data
            Aktyor.objects.create(
                ism=data.get("ism"),
                jins = data.get("jins"),
                davlat=data.get("davlat"),
                t_sana=data.get("t_sana"),
            )
            return  Response({"success":True,"created_data":serializer.data})
        return Response({"success":False,"errros":serializer.errors})



class AktyorAPI(APIView):
    def get(self,request,pk):
        aktyor=Aktyor.objects.get(id=pk)
        serializer=AktyorSerializers(aktyor)
        return Response(serializer.data)
    def put(self,request,pk):
        aktyor=Aktyor.objects.filter(id=pk)
        serializer=AktyorSerializers(aktyor.first(),data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            aktyor.update(
                ism=data.get("ism"),
                jins=data.get("jins"),
                davlat=data.get("davlat"),
                t_sana=data.get("t_sana"),
            )
            serializer=AktyorSerializers(aktyor.first())
            return Response({"success": True, "update_data": serializer.data})
        return Response({"success": False, "errros": serializer.errors})

class TariflarAPI(APIView):
    def get(self,request):
        tariflar=Tarif.objects.all()
        serializer=TarifSerializers(tariflar,many=True)
        return Response(serializer.data)
    def post(self,request):
        tarif=request.data
        serializer=TarifSerializers(data=tarif)
        if serializer.is_valid():
            data=serializer.validated_data
            Tarif.objects.create(
                nom=data.get("nom"),
                davomiylik = data.get("davomiylik"),
                narx=data.get("narx"),
            )
            return  Response({"success":True,"created_data":serializer.data})
        return Response({"success":False,"errros":serializer.errors})

class TarifAPI(APIView):
    def get(self,request,pk):
        tarif=Tarif.objects.get(id=pk)
        serializer=TarifSerializers(tarif)
        return Response(serializer.data)
    def put(self,request,pk):
        tarif=Tarif.objects.filter(id=pk)
        serializer=TarifSerializers(tarif.first(),data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            tarif.update(
                nom=data.get("nom"),
                davomiylik=data.get("davomiylik"),
                narx=data.get("narx"),
            )
            serializer=TarifSerializers(tarif.first())
            return Response({"success": True, "update_data": serializer.data})
        return Response({"success": False, "errros": serializer.errors})
    def delete(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        tarif.delete()
        return Response({'success': True})

