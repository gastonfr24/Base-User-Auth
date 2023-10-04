from django.conf import settings
# Create 1 superuser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateSuperUserView(APIView):
    def get(self, request, *args, **kwargs):

        if not User.objects.filter(username='nombre_de_superusuario').exists():
            # Utiliza config para obtener la contraseña del archivo .env
            User.objects.create_superuser('gastonfr24', 'gastonfr24@test-auth.com', settings.USER_CREATION_PASSWORD)

            Response({'message': 'usuario creado, ahora puedes usar el superuser'},status=status.HTTP_201_CREATED)
        else:
            Response({'message': 'usuario creado anteriormente'},status=status.HTTP_200_OK)
