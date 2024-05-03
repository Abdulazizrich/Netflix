from django.contrib import admin
from django.urls import path,include
from filmApp.views import *
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
   openapi.Info(
      title="Netflix API",
      default_version='v1',
      description="Abdulaziz 2005.admin panel /admin/ routeda joylashgan",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="abdulazizxolmurodov2023@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,

)
router = DefaultRouter()
router.register('izohlar',IzohModelViewSet)
router.register('kinolar1',KinoModelViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),

    #swagger docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),


    path('',include(router.urls)),
    path('hello/', HelloAPI.as_view()),
    path('aktyorlar/', AktyorlarAPI.as_view()),
    path('aktyorlar1/<int:pk>/', AktyorlarAPIView.as_view()),
    path('aktyor/<int:pk>/', AktyorAPI.as_view()),
    path('tariflar/', TariflarAPI.as_view()),
    path('tarif/<int:pk>/', TarifAPI.as_view()),
    path('kinolar/', KinolarAPI.as_view()),
    path('kino/<int:pk>/', KinoAPI.as_view()),
    path('kino/<int:pk>/aktyorlar/', KinoAktyorlarAPI.as_view()),
    path('aktyor/<int:pk>/kinolar/', AktyorKinolarAPI.as_view()),
    path('auth-token/',obtain_auth_token),

]
