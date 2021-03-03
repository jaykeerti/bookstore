from django.conf.urls import url 
from books import views 
 
urlpatterns = [ 
    url(r'^api/books$', views.books_list),
    url(r'^external-api/$', views.get_book_data_by_id),
    url(r'^api/books/(?P<pk>\w+)$', views.book_detail),
]