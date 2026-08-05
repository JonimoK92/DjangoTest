"""Views of the library API.

Over to you: this file is empty apart from this header.

Nothing forces you to write everything here. If you would rather keep the
business logic somewhere else (in the models, the serializers, a dedicated
module), do so and explain why in `description.md`.

Useful documentation:
https://www.django-rest-framework.org/api-guide/views/
https://www.django-rest-framework.org/api-guide/viewsets/
"""


from .serializers import *
from rest_framework import viewsets
from .models import *
from django.db.models import Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ["title", "author"]

    def get_queryset(self):
        book_is_on_loan = Loan.objects.filter(book=OuterRef("pk"),
            return_date__isnull=True
        )

        queryset = Book.objects.annotate(loan_exist=Exists(book_is_on_loan))

        available = self.request.query_params.get("available")

        if available == "true":
            queryset = queryset.filter(
                loan_exist=False
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "borrow":
            return BorrowSerializer
        return BookSerializer

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()

        if book.loans.filter(return_date__isnull=True).exists():
            return Response(
            {"error": "You can't this book is already on loan"},
            status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        loan = Loan.objects.create(
            book=book,
            borrower=serializer.validated_data["borrower"],
            due_date=serializer.validated_data["due_date"]
        )

        serializer = LoanSerializer(loan)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


    @action(detail=True, methods=["post"])
    def returnbook(self, request, pk=None):
        loan = self.get_object()

        if loan.return_date is not None:
            return Response(
                {"error": f"There is already a return_date, {loan.return_date}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.return_date = timezone.now().date()
        loan.save()

        serializer = LoanSerializer(loan)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )