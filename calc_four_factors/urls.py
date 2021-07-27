from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("calc_four_factors/result",views.result,name="result"),
    #path("plot/",views.get_svg,name="plot")
]