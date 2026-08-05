"""URL configuration of the library application.

These routes are included under the `/api/` prefix (see `config/urls.py`).
The list is empty, filling it in is up to you.

Useful documentation:
https://www.django-rest-framework.org/api-guide/routers/
"""

from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LoanViewSet

router = DefaultRouter()
router.register("books",BookViewSet,basename="books")
router.register("loans",LoanViewSet,basename="loans")
urlpatterns = router.urls

