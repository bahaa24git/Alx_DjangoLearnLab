from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly  
 
from .models import Book
from .serializers import BookSerializer

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly] 