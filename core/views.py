from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class CreateSuperUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        User = get_user_model()  # Obtiene el modelo de usuario personalizado

        if not User.objects.filter(email='gastonfr24@test-auth.com').exists():
            # Utiliza el administrador para crear el superusuario
            user = User.objects.create_user(
                email='gastonfr24@test-auth.com',
                password=settings.USER_CREATION_PASSWORD  # Utiliza la contraseña del archivo .env
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()

            return Response({'message': 'Usuario creado, ahora puedes usar el superusuario'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Usuario creado anteriormente'}, status=status.HTTP_200_OK)
