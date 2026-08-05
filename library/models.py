"""Models of the library application.

These models are given to you, you do not need to write them.
You may still change them if you find it useful, as long as you generate the
matching migration and explain your choice in `description.md`.
"""

from django.db import models


class Book(models.Model):
    """A book in the library catalogue.

    There is deliberately no `available` field: whether a book is available is
    derived from its ongoing loans.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["title"]
        verbose_name = "book"
        verbose_name_plural = "books"

    def __str__(self):
        return f"{self.title} ({self.author})"


class Loan(models.Model):
    """The loan of a book to a reader.

    A loan is considered *ongoing* as long as its return date has not been set.
    """

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    borrower = models.EmailField()
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-loan_date"]
        verbose_name = "loan"
        verbose_name_plural = "loans"

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower}"
