from django.shortcuts import render

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
