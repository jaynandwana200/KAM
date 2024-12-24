from django.shortcuts import render
from django.http import HttpResponse
from .models import leads,interactionLogging,tracking
from datetime import date

# Main Page 
#similar naming convention used in all functions
def index(request):

    try:
        allLeads = leads.objects.all() #Fetching all leads data from database
    except:
        return HttpResponse("No object present in Leads Table")

    try:
        allInteractions = interactionLogging.objects.all()#Fetching all interaction data from database 
    except:
        return HttpResponse("No object present in Interaction Table")

    #getting calls pending on todays dates from interactions
    todaysCalls = []
    for item in allInteractions:
        if(item.date == date.today()):
            todaysCalls.append(item)
    

    params = {'allLeads' : allLeads,'allinteractions':allInteractions,'todaysCalls' : todaysCalls}    #Dictionary that stores parameters comming from database and pass to webpage
    return render(request,'KAM/index.html',params)


#creating lead
def createLeads(request):
    
    #fetching data from Data form
    name = request.POST.get('name','Noname')
    resAddress = request.POST.get('address','Noaddress')
    number = request.POST.get('contactNo','NocontactNumber')
    status = request.POST.get('currentStatus','NocurrentStatus')
    KID = request.POST.get('KAMID','NoKAMID')

    #check if all fields in form if filled or not
    if(name == 'Noname' or resAddress == 'Noaddress' or number == 'NocontactNumber' or status == 'NocurrentStatus' or KID == 'NoKAMID'):
        return render(request,'KAM/createLeads.html')

    # creating record in table
    try:
        create = leads(restaurantName = name, address = resAddress,contactNumber = number,currentStatus =  status,KAMID = KID)
        create.save()
    except:
        return HttpResponse("Save does not Exist for givem query")
    

    return index(request)


#create tracker
def createTracker(request):

    return HttpResponse('createTracker')


#viewCurrentLeads
def viewLeads(request):
    try:
        allLeads = leads.objects.all() #Fetching all leads data from database
    except:
        return HttpResponse("No object present in Leads Table")

    try:
        allInteractions = interactionLogging.objects.all()#Fetching all interaction data from database 
    except:
        return HttpResponse("No object present in Interaction Table")

    try:   
        allTrackingData = tracking.objects.all()#Fetching all tracking data from database 
    except:
        return HttpResponse("No object presnet in Tracking Table")

    #accessing leadid from index page 
    leadID = request.POST.get('leadid','0')
    
    leadData = 0#will contain lead data
    interactionsData = []
    trackingData = []
    #processing allLeads to get data related to leadId
    for lead in allLeads:
        if str(lead.leadID) == leadID:
            leadData = lead
            break
    
    #processing allLeads to get data related to interactions related to lead
    for interaction in allInteractions:
        if(str(interaction.leadID.leadID) == leadID):
            interactionsData.append(interaction)

    # processing alltrackingdata to get tracking details related tot lead
    for track in allTrackingData:
        if(str(track.leadID.leadID) == leadID):
            trackingData.append(track)

    params = {'leadData' : leadData,'interactionData':interactionsData,'trackingData':trackingData}#Dictionary that stores parameters comming from database and pass to webpage
    return render(request,'KAM/viewLeads.html',params)


#viewSearchResult
def searchResult(request):   

    #fetching data from database
    leadData = leads.objects.all()
    interactionData = interactionLogging.objects.all()

    searchInput = request.POST.get('searchResult','noinput')#fetching searchdata from web page

    #if no input given
    if searchInput == 'noinput':
        return index(request)

    #searchind database according to searchinput
    leadID = set()
    interactionID = []
    idForInteraction = []

    #processing data to get searchdata
    for items in leadData:
        if(searchInput in items.restaurantName or searchInput == items.KAMID or searchInput in items.address or searchInput == items.currentStatus):
            leadID.add(items)
            idForInteraction.append(items.leadID)

    for items in interactionData:
        if(items.leadID.leadID in idForInteraction):
            interactionID.append(items)

    params = {'allLeads' : leadID, 'allinteractions' : interactionID}

    return render(request,'KAM/searchResult.html',params)


#updateLeads
def updateLeads(request):
    return HttpResponse('Hello')


#addInteraction
def addInteraction(request):
    return render(request,'KAM/interactions.html')


#deleteInteraction
def deleteInteraction(request):

    ID = request.POST.get('interactionID','1')

    #deleting interaction from database
    interactionLogging.objects.filter(interactionID = ID).delete()

    return index(request)


#delete Lead
def deleteLead(request):

    ID = request.POST.get('LID','1')#leadID
    
    #deleting interaction from database
    leads.objects.filter(leadID = ID).delete()

    return index(request)
