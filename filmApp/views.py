from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status,filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import *
from  .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
class HelloAPI(APIView):
    def get(self,request):
        data={
            "massage":"Hello World"
        }
        return Response(data)

class MyCustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class AktyorlarAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="ID boyicha saralash"
            ),
            openapi.Parameter(
                name="chet_ellik",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Davlati boyicha saralash"
            ),
            openapi.Parameter(
                name="qidiruv",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="ID,ism boyicha qidirish"
            ),
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Id,ism,davlat boyicha tartiblash",
                enum=["id","ism","davlat"],
                default="id"
            )
        ]
    )
    def get(self,request):
        aktyorlar=Aktyor.objects.all()
        name=request.query_params.get("name")
        id=request.query_params.get('id')
        chet_ellik=request.query_params.get("chet_ellik")
        qidiruv=request.query_params.get("qidiruv")
        ordering=request.query_params.get('ordering',None)
        if ordering is not None:
            aktyorlar=aktyorlar.order_by(ordering)
        if id is not None:
            aktyorlar=aktyorlar.filter(id=id)
        if name is not None:
            aktyorlar=aktyorlar.filter(ism__icontains=name)
        if chet_ellik is not None:
            if  chet_ellik=="true":
                aktyorlar=aktyorlar.exclude(davlat="Ozbekiston")
            elif chet_ellik=="false":
                aktyorlar=aktyorlar.filter(davlat="Ozbekiston")
        if qidiruv is not None:
            aktyorlar=aktyorlar.filter(
            Q(ism__icontains=qidiruv)|
            Q(t_sana__icontains=qidiruv) |
            Q(davlat__icontains=qidiruv) |
            Q(jins__icontains=qidiruv)

            )
        serializer=AktyorSerializers(aktyorlar,many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=AktyorSerializer,
    )
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
    def delete(self,request,pk):
        aktyor=get_object_or_404(Aktyor,id=pk)
        aktyor.delete()
        return Response({'success': True})

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

class KinolarAPI(APIView):
    def get(self,request):
        kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar,many=True)
        return Response(serializer.data)
    def post(self, request, serializer_data=None):
        kino=request.data
        serializer=KinoSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"created_data":serializer_data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class KinoAPI(APIView):
    def get(self,request,pk):
        kino=get_object_or_404(Kino,id=pk)
        serializer= KinoSerializer(kino)
        return Response(serializer.data)
    def put(self,request,pk):
        kino=get_object_or_404(Kino,id=pk)
        serializer=KinoSerializer(kino,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"updated_data":serializer.data})
        return Response(serializer.errors)
    def delete(self,request,pk):
        kino=get_object_or_404(Kino,id=pk)
        kino.delete()
        return Response("success delete")

class KinoAktyorlarAPI(APIView):
    def get(self,request,pk):
        kino=get_object_or_404(Kino,id=pk)
        aktyorlar=Aktyor.objects.filter(
            id__in=KinoAktyor.objects.filter(kino=kino).values_list("aktyor__id",flat=True))
        serializer=AktyorSerializers(aktyorlar,many=True)
        return Response(serializer.data)





class AktyorKinolarAPI(APIView):
    def get(self,request,pk):
        aktyor=get_object_or_404(Aktyor,id=pk)
        kinolar=Kino.objects.filter(
            id__in=KinoAktyor.objects.filter(aktyor=aktyor).values_list("aktyor__id",flat=True))
        serializer=KinoSerializer(kinolar,many=True)
        return Response(serializer.data)

class IzohModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer

    def get_queryset(self):
        user=self.request.user
        izoh=Izoh.objects.filter(user=user)
        return izoh

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def delete(self, request):
        user=self.request.user
        izoh = get_object_or_404(Izoh, user=user)
        izoh.delete()
        return Response({'success': True})
class KinoModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer

    filter_backends = [filters.SearchFilter]
    search_fields=['nom','janr','yil']
    pagination_class = MyCustomPagination
    def get_queryset(self):
        kinolar=Kino.objects.all()
        nom=self.request.query_params.get("nom")
        if nom is not None:
            kinolar=kinolar.filter(nom__icontains=nom)
        return kinolar

    @action(detail=True,methods=['get'])
    def aktyorlar(self,request,pk):
        kino=self.get_object()
        aktyorlar=Aktyor.objects.filter(id__in=KinoAktyor.objects.filter(kino=kino).values_list("aktyor__id",flat=True))

        serializer=AktyorSerializers(aktyorlar,many=True)
        return Response(serializer.data)

    @action(detail=True,methods=['get'])
    def izohlar(self,request,pk):
        kino=self.get_object()
        izohlar=Izoh.objects.filter(kino=kino)

        serializer = IzohSerializer(izohlar, many=True)
        return Response(serializer.data)

class AktyorlarAPIView(APIView):
    def get(self,request,pk):
        aktyor=get_object_or_404(Aktyor,id=pk)
        serializer=AktyorSerializer(aktyor)
        return Response(serializer.data)



