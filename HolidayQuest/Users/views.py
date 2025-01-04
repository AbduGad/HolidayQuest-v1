from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import User_serializer
from rest_framework.permissions import AllowAny


class register_view(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = User_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        