from django.urls import path
from sale_good import views

app_name = 'sale_good'
urlpatterns = [
    path('saleindex/', views.saleindex , name = 'saleindex'),
    path('salegood/',views.salegood, name = 'salegood'),
    path('showImg/' , views.showImg , name = 'showImg' ),
]

