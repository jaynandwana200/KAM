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
        return HttpResponse("No object present in Leads Table : FUNC->index")

    try:
        allInteractions = interactionLogging.objects.all()#Fetching all interaction data from database 
    except:
        return HttpResponse("No object present in Interaction Table : FUNC->index")

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
        return HttpResponse("Matching Query Dosenot exist for save : FUNC->createLeads")

    return index(request)


def getLeadIDForUpdateLead(request):
    leadId = request.POST.get('LeadID','')

    try:
        leadObject = leads.objects.filter(leadID = leadId).get()
    except:
        return HttpResponse("Matching Query Dosenot exist for leadID : FUNC->getLeadIDForuUpdateLead")
    
    params = {'leadObject' : leadObject}#used to store parameters
    
    return render(request,'KAM/updateLeads.HTML',params)

##Logic to add Tracker
# First we use getLeadIDForTracker function to get leadID from viewlead page 
# and them send leadid of lead to createLeads page to which tracker is related and then with other 
# details of tracker and leadId send it to createTracker function to add tracker  
#this is done because tracking table is referencing leads table and has foreign key ( LeadsId ) in it

#Fetching LeadId to add Tracker to leadID
#here leadIDFromCreateTracker is value of leadID if function is fired from createtacker function
def getLeadIDForTracker(request):
    leadId = request.POST.get('leadID','')
    params = {'leadId': leadId}
    return render(request,'KAM/createTracker.html',params)#sending leadID to create Tracker page


#creating tarcker 
def createTracker(request):
    leadId = request.POST.get('leadID','No')
    staffName = request.POST.get('name','No')
    staffRole = request.POST.get('role','No')
    contact = request.POST.get('contactNo','No')
    email = request.POST.get('emailID','No')
    
    #No empty data allowed
    if(leadId == 'No' or staffName == 'No' or staffRole == 'No' or contact == 'No' or email == 'No'):
        return createTracker(request)
    
    #fetching foreign key object from leads to create tracker

    try:
        foreignKey = leads.objects.filter(leadID = leadId).get()
    except:
        return HttpResponse("Matching Query Dosenot exist for leads : FUNC->createTracker")
    
    #saving data in tracker
    try:
        addTracker = tracking(name = staffName,role = staffRole,phoneNumber = contact,emailID = email,leadID = foreignKey)
        addTracker.save()
    except:
        return HttpResponse("Matching Query Dosenot exist for save : FUNC->createTracker")

    return viewLeads(request,leadId)


#viewCurrentLeads
def viewLeads(request,leadIDFromCreateTracker = -1):
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

    # if function fired from createTracking then get value of leadIDFromCreateTracker into leadId
    if(leadID == '0'):
        leadID = leadIDFromCreateTracker

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

    leadId = request.POST.get('leadId','') 
    name = request.POST.get('name','')
    location = request.POST.get('address','')
    number = request.POST.get('contactNo','')
    status = request.POST.get('currentStatus','')
    KAMId = request.POST.get('KAMID','')

    try:
        leads.objects.filter(leadID = leadId).update(restaurantName = name,address = location,contactNumber = number,currentStatus = status,KAMID = KAMId)
    except:
        return HttpResponse("Matching Query Dosenot exist for Update : FUNC->updateLeads")

    return viewLeads(request,leadId)


#getLeadIDForInteraction
#same logic as create tracker here also LeadID is Foreign Key
def getLeadIDForInteraction(request):
    leadID = request.POST.get('leadID','')

    params = {'leadID' : leadID}
    return render(request,'KAM/interactions.html',params)


#addInteraction
def addInteraction(request):
    #fetching data from intiractions web page
    ID = request.POST.get('leadID','')
    Type = request.POST.get('type','')
    Note = request.POST.get('notes','')
    follow = request.POST.get('followUp','')
    Date = request.POST.get('date','')

    #fetching foreign key to pass to intercation to create 
    try:
        foreignKey = leads.objects.filter(leadID = ID).get()
    except:
        return HttpResponse("Matching Query Dosenot exist for leads : FUNC->addInteraction")

    try:
        addinteraction = interactionLogging(type = Type,notes = Note,followUp = follow,date = Date,leadID = foreignKey)
        addinteraction.save()
    except:
        return HttpResponse("Matching Query Dosenot exist for saving : FUNC->addInteraction")

    return viewLeads(request,ID)


#deleteInteraction
def deleteInteraction(request):

    ID = request.POST.get('interactionID','1')

    #deleting interaction from database
    try:
        interactionLogging.objects.filter(interactionID = ID).delete()
    except:
        return HttpResponse("Matching Query Dosenot exist for deletion : FUNC->deleteInteraction")

    return index(request)


#delete Lead
def deleteLead(request):

    ID = request.POST.get('LID','1')#leadID
    
    #deleting interaction from database
    try:
        leads.objects.filter(leadID = ID).delete()
    except:
        return HttpResponse("Matching Query Dosenot exist for deletion : FUNC->deleteLead")

    return index(request)


#delete Tracking
def deleteTracking(request):

    #fetching Tracking id to delete
    trackingId = request.POST.get('trackingID','0')
    leadID = request.POST.get('leadID','0')

    try:
        tracking.objects.filter(trackingID = trackingId).delete()
    except:
        return HttpResponse("Matching Query Dosenot exist for deletion : FUNC->deleteTracking")

    return viewLeads(request,leadID)#sending leadID to viewLeads


##get interaction ID to update interaction as it contains lead ID as foreign key
def getLeadIDForUpdateInteraction(request):

    return HttpResponse("get leadid to update interaction")









