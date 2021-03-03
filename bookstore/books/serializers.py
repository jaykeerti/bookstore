from rest_framework import serializers 
from books.models import BookInventory
 
 
class BooksSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = BookInventory
        fields = ('bookid',
                  'quantity')