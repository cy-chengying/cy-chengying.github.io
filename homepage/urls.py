from django.urls import path
from homepage import views
app_name = 'homepage'
urlpatterns = [
     path('home/',views.home , name = 'home'),
    path('message_board/' , views.message_board , name = 'message_board'),
    path('create/' ,views.create , name = 'create'),
    path('save/' , views.save , name = 'save'),
    path('search/', views.search ,name='search' ),
    path('showImg/',views.showImg , name = 'showImg'),
]