"""Serializers of the library application.

Over to you: this file is empty apart from this header.

Useful documentation:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers
from .models import Book, Loan
from datetime import date
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "publication_year", "available"]

    def get_available(self, obj):
         return not obj.loans.filter(return_date=None).exists()

    def validate(self, data):
        if Book.objects.filter(isbn=data["isbn"]).exists():
            raise serializers.ValidationError({
                "isbn": "This ISBN is already used"
            })

        if data["publication_year"] > 2026:
            raise serializers.ValidationError({
                "publication_year": "You cannot choose a year in the future"
            })

        return data

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "book", "borrower", "loan_date", "due_date", "return_date"]

class BorrowSerializer(serializers.Serializer):
    borrower = serializers.EmailField()
    due_date = serializers.DateField()

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "The due_date cannot be in the past"
            )
        return value



