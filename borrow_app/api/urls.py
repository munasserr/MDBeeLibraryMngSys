from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'borrow_records', views.BorrowRecordViewSet,basename='borrow_records')

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/' ,views.BorrowBook.as_view(), name='borrow_book'),
    path('return/' ,views.ReturnBook.as_view(), name='return_book'),

    path('borrow_record/<int:pk>/', views.BorrowRecordDetail.as_view(), name='borrow-record-detail'),
    # for filtering records

]