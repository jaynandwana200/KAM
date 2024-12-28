from django.urls import path
from . import views

urlpatterns = [

    # End Point to Main Page
    path("",views.index,name='index'),

    #accessing kamid
    path("KAMIDforleads/",views.KAMIDforleads,name='KAMIDforleads'),
    path("addKAM/",views.addKAM,name='addKAM'),
    path("deleteKAM/",views.deleteKAM,name='deleteKAM'),
    path("showKAM/",views.showKAM,name='showKAM'),

    #performance Tracking 
    path("performanceTracking/",views.performanceTracking,name='performanceTracking'),
    

    # All endpoints related to Leads
    path("viewLeads/",views.viewLeads,name='viewLeads'),
    path("createLeads/",views.createLeads,name='createLeads'),
    path("deleteLead/",views.deleteLead,name='deleteLead'),
    path("getLeadIDForUpdateLead/",views.getLeadIDForUpdateLead,name='getLeadIDForUpdateLead'),
    path("updateLeads/",views.updateLeads,name='updateLeads'),


    # All endpoints Related to Interaction
    path("addInteraction/",views.addInteraction,name='addInteraction'),
    path("deleteInteraction/",views.deleteInteraction,name='deleteInteraction'),
    path("getLeadIDForInteraction/",views.getLeadIDForInteraction,name='getLeadIDForInteraction'),
    path("getLeadIDForUpdateInteraction/",views.getLeadIDForUpdateInteraction,name='getLeadIDForUpdateInteraction'),
    path("updateInteraction/",views.updateInteraction,name='updateInteraction'),


    # EndPoint related to Search
    path("searchResult/",views.searchResult,name='searchResult'),


    # All endpoints related to Leads
    path("createTracker/",views.createTracker,name='createTracker'),
    path("deleteTracking/",views.deleteTracking,name='deleteTracking'),
    path("getLeadIDForTracker/",views.getLeadIDForTracker,name='getLeadIDForTracker'),
    path("getLeadIDForUpdateTracking/",views.getLeadIDForUpdateTracking,name='getLeadIDForUpdateTracking'),
    path("updateTracking/",views.updateTracking,name='updateTracking'),
]