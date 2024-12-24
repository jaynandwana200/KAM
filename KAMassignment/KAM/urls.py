from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("viewLeads/",views.viewLeads,name='viewLeads'),
    path("createLeads/",views.createLeads,name='createLeads'),
    path("updateLeads/",views.updateLeads,name='updateLeads'),
    path("getLeadIDForUpdateLead/",views.getLeadIDForUpdateLead,name='getLeadIDForUpdateLead'),
    path("deleteLead/",views.deleteLead,name='deleteLead'),
    path("addInteraction/",views.addInteraction,name='addInteraction'),
    path("deleteInteraction/",views.deleteInteraction,name='deleteInteraction'),
    path("getLeadIDForInteraction/",views.getLeadIDForInteraction,name='getLeadIDForInteraction'),
    path("getLeadIDForUpdateInteraction/",views.getLeadIDForUpdateInteraction,name='getLeadIDForUpdateInteraction'),
    path("searchResult/",views.searchResult,name='searchResult'),
    path("createTracker/",views.createTracker,name='createTracker'),
    path("getLeadIDForTracker/",views.getLeadIDForTracker,name='getLeadIDForTracker'),
    path("deleteTracking/",views.deleteTracking,name='deleteTracking'),
]