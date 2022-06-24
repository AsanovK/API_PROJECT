from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

class RegistrationView(APIView):
    def post(self, request):
        print(request)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Thanks for registration! Please activate your account', status=201)
        return Response(serializer.errors, status=400)

class ActivationView(APIView):
    def get(self, request, code):
        user = User.objects.filter(activation_code=code).first()
        if user:
            user.is_active = True
            user.save()
            return Response(
                'Your account is activated',
                status=200
            )
        return Response('Invalid activation code', status=400)