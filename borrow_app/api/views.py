import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Book, BorrowRecord
from .serializers import BorrowRecordSerializer
from rest_framework import viewsets
from ..models import BorrowRecord
from .serializers import BorrowRecordSerializer
from django_filters.rest_framework import DjangoFilterBackend

class BorrowBook(APIView):
    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')
        due_date = request.data.get('due_date')
        book = get_object_or_404(Book, pk=book_id)

        if not book.available:
            return Response({"error": "This book is not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        book.available = False
        book.save()

        borrow_record = BorrowRecord.objects.create(
            borrower_id=borrower_id,
            book=book,
            due_date=due_date
        )
        serializer = BorrowRecordSerializer(borrow_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReturnBook(APIView):
    def post(self, request, *args, **kwargs):
        record_id = request.data.get('record_id')
        borrow_record = get_object_or_404(BorrowRecord, pk=record_id)

        book = borrow_record.book
        book.available = True
        book.save()

        borrow_record.returned = True
        borrow_record.actual_return_date = datetime.date.today()
        borrow_record.save()

        return Response({"success": "Book returned successfully."})


class BorrowRecordDetail(APIView):
    def get(self, request, pk, format=None):
        borrow_record = BorrowRecord.objects.filter(pk=pk).first()
        if borrow_record is not None:
            serializer = BorrowRecordSerializer(borrow_record)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['borrower', 'book', 'returned','borrow_date','due_date','actual_return_date']