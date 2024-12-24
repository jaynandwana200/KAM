from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("createLeads/",views.createLeads,name='createLeads'),
    path("viewLeads/",views.viewLeads,name='viewLeads'),
    path("updateLeads/",views.updateLeads,name='updateLeads'),
    path("addInteraction/",views.addInteraction,name='addInteraction'),
    path("searchResult/",views.searchResult,name='searchResult'),
    path("deleteInteraction/",views.deleteInteraction,name='deleteInteraction'),
    path("deleteLead/",views.deleteLead,name='deleteLead'),
]