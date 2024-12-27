from django.shortcuts import render, HttpResponse
from .models import leads, interactionLogging, tracking
from datetime import date
from .tasks import generateInteractions
import datetime
import logging

logger = logging.getLogger(__name__)


def test_celery(request):
    generateInteractions(request).delay()
    return HttpResponse("Testing celery")


# Main Page
# similar naming convention used in all functions
def index(request):

    try:
        allLeads = leads.objects.all()  # Fetching all leads data from database
    except:
        allLeads = None

    try:
        allInteractions = (
            interactionLogging.objects.all()
        )  # Fetching all interaction data from database
    except:
        allInteractions = None

    # getting calls pending on todays dates from interactions
    todaysCalls = []

    # basic error handling as None is not iterable
    if allInteractions != None:
        for item in allInteractions:
            if item.date == date.today():
                todaysCalls.append(item)

    params = {
        "allLeads": allLeads,
        "allinteractions": allInteractions,
        "todaysCalls": todaysCalls,
    }  # Dictionary that stores parameters comming from database and pass to webpage
    return render(request, "KAM/index.html", params)


# creating lead
def createLeads(request):

    # fetching data from Data form
    name = request.POST.get("name", "Noname")
    resAddress = request.POST.get("address", "Noaddress")
    number = request.POST.get("contactNo", "NocontactNumber")
    status = request.POST.get("currentStatus", "NocurrentStatus")
    KID = request.POST.get("KAMID", "NoKAMID")
    callFreq = request.POST.get("callFrequency", "NocallFrequency")
    City = request.POST.get("city", "NoCity")
    State = request.POST.get("state", "NosCate")
    Country = request.POST.get("country", "NoCountry")
    Time = request.POST.get("time", "NotTime")

    if (
        name == "Noname"
        or resAddress == "Noaddress"
        or number == "NocontactNumber"
        or status == "NocurrentStatus"
        or callFreq == "NocallFrequency"
        or City == "NoCity"
        or State == "NosSate"
        or Country == "NoCountry"
        or Time == "NotTime"
    ):
        return render(request, "KAM/createLeads.html")

    # creating record in table
    try:
        create = leads(
            restaurantName=name,
            address=resAddress,
            contactNumber=number,
            currentStatus=status,
            KAMID=KID,
            callFrequency=callFreq,
            lastCallMade=date.today(),
            city=City,
            state=State,
            country=Country,
            time=Time,
        )
        create.save()
    except:
        return index(request)

    return index(request)


# fetching lead id for get LeadID
def getLeadIDForUpdateLead(request):
    leadId = request.POST.get("LeadID", "")

    try:
        leadObject = leads.objects.filter(leadID=leadId).get()
    except:
        return index(request)

    params = {"leadObject": leadObject}  # used to store parameters

    return render(request, "KAM/updateLeads.HTML", params)


##Logic to add Tracker
# First we use getLeadIDForTracker function to get leadID from viewlead page
# and them send leadid of lead to createLeads page to which tracker is related and then with other
# details of tracker and leadId send it to createTracker function to add tracker
# this is done because tracking table is referencing leads table and has foreign key ( LeadsId ) in it


# Fetching LeadId to add Tracker to leadID
# here leadIDFromCreateTracker is value of leadID if function is fired from createtacker function
def getLeadIDForTracker(request):
    leadId = request.POST.get("leadID", "")
    params = {"leadId": leadId}
    return render(
        request, "KAM/createTracker.html", params
    )  # sending leadID to create Tracker page


# creating tarcker
def createTracker(request):
    leadId = request.POST.get("leadID", "No")
    staffName = request.POST.get("name", "No")
    staffRole = request.POST.get("role", "No")
    contact = request.POST.get("contactNo", "No")
    email = request.POST.get("emailID", "No")

    # No empty data allowed
    if (
        leadId == "No"
        or staffName == "No"
        or staffRole == "No"
        or contact == "No"
        or email == "No"
    ):
        return createTracker(request)

    # fetching foreign key object from leads to create tracker

    try:
        foreignKey = leads.objects.filter(leadID=leadId).get()
    except:
        return index(request)

    # saving data in tracker
    try:
        addTracker = tracking(
            name=staffName,
            role=staffRole,
            phoneNumber=contact,
            emailID=email,
            leadID=foreignKey,
        )
        addTracker.save()
    except:
        return index(request)

    return viewLeads(request, leadId)


# viewCurrentLeads
def viewLeads(request, leadIDFetchFromOtherFunc="-1"):

    # accessing leadid from index page
    leadId = request.POST.get("leadid", "0")

    # if function fired from createTracking then get value of leadIDFromCreateTracker into leadId
    if leadIDFetchFromOtherFunc != "-1":
        leadId = leadIDFetchFromOtherFunc

    try:
        leadData = leads.objects.filter(
            leadID=leadId
        )  # Fetching leads data from database
    except:
        leadData = None

    try:
        interactionsData = interactionLogging.objects.filter(
            leadID__leadID__contains=leadId
        )
    except:
        interactionsData = None

    try:
        # Fetching tracking data from database
        trackingData = tracking.objects.filter(leadID__leadID__contains=leadId)
    except:
        trackingData = None

    params = {
        "leadData": leadData,
        "interactionData": interactionsData,
        "trackingData": trackingData,
    }  # Dictionary that stores parameters comming from database and pass to webpage
    return render(request, "KAM/viewLeads.html", params)


# viewSearchResult
def searchResult(request):

    # fetching data from database
    try:
        leadData = leads.objects.all()
    except:
        leadData = None

    try:
        interactionData = interactionLogging.objects.all()
    except:
        interactionData = None

    searchInput = request.POST.get(
        "searchResult", "noinput"
    )  # fetching searchdata from web page

    # if no input given
    if searchInput == "noinput":
        return index(request)

    # searchind database according to searchinput
    leadID = set()
    interactionID = []
    idForInteraction = []

    # processing data to get searchdata
    # none is not Iterable
    if leadData != None:
        for items in leadData:
            if (
                searchInput in items.restaurantName
                or searchInput == items.KAMID
                or searchInput in items.address
                or searchInput == items.city
                or searchInput == items.state
                or searchInput == items.country
            ):
                leadID.add(items)
                idForInteraction.append(items.leadID)

    if interactionData != None:
        for items in interactionData:
            if items.leadID.leadID in idForInteraction:
                interactionID.append(items)

    params = {"allLeads": leadID, "allinteractions": interactionID}

    return render(request, "KAM/searchResult.html", params)


# updateLeads
def updateLeads(request):

    leadId = request.POST.get("leadId", "")
    name = request.POST.get("name", "")
    location = request.POST.get("address", "")
    City = request.POST.get("city", "")
    State = request.POST.get("state", "")
    Country = request.POST.get("country", "")
    number = request.POST.get("contactNo", "")
    status = request.POST.get("currentStatus", "")
    callFreq = request.POST.get("callFrequency", "")
    KAMId = request.POST.get("KAMID", "")

    # deleting all interactions if status updated to inactive
    if status == "inactive":
        interactionLogging.objects.filter(leadID__leadID__contains=leadId).delete()

    # try:
    leads.objects.filter(leadID=leadId).update(
        restaurantName=name,
        address=location,
        city=City,
        state=State,
        country=Country,
        contactNumber=number,
        currentStatus=status,
        callFrequency=callFreq,
        KAMID=KAMId,
    )
    # excreturn index(request)

    return viewLeads(request, leadId)


# getLeadIDForInteraction
# same logic as create tracker here also LeadID is Foreign Key
def getLeadIDForInteraction(request):

    leadID = request.POST.get("leadID", "")

    params = {"leadID": leadID}
    return render(request, "KAM/interactions.html", params)


# addInteraction
def addInteraction(request):
    # fetching data from intiractions web page
    ID = request.POST.get("leadID", "")
    Type = request.POST.get("type", "")
    Note = request.POST.get("notes", "")
    follow = request.POST.get("followUp", "")
    Date = request.POST.get("date", "")
    Time = request.POST.get("time", datetime.time(00, 00, 00))

    # fetching foreign key to pass to intercation to create
    try:
        foreignKey = leads.objects.filter(leadID=ID).get()
    except:
        return index(request)

    try:
        addinteraction = interactionLogging(
            type=Type,
            notes=Note,
            followUp=follow,
            date=Date,
            leadID=foreignKey,
            time=Time,
        )
        addinteraction.save()
    except:
        return index(request)

    return viewLeads(request, ID)


# deleteInteraction
def deleteInteraction(request):

    ID = request.POST.get("interactionID", "1")

    # deleting interaction from database
    try:
        interactionLogging.objects.filter(interactionID=ID).delete()
    except:
        return index(request)

    return index(request)


# delete Lead
def deleteLead(request):

    ID = request.POST.get("LID", "1")  # leadID

    # deleting interaction from database
    try:
        leads.objects.filter(leadID=ID).delete()
    except:
        return index(request)

    return index(request)


# delete Tracking
def deleteTracking(request):

    # fetching Tracking id to delete
    trackingId = request.POST.get("trackingID", "0")
    leadID = request.POST.get("leadID", "0")

    try:
        tracking.objects.filter(trackingID=trackingId).delete()
    except:
        return index(request)

    return viewLeads(request, leadID)  # sending leadID to viewLeads


##get interaction ID to update interaction
def getLeadIDForUpdateInteraction(request):
    interactionId = request.POST.get("interactionID", "")
    try:
        interactionObject = interactionLogging.objects.filter(
            interactionID=interactionId
        ).get()
    except:
        return index(request)

    params = {"interactionObject": interactionObject}

    return render(request, "KAM/updateInteraction.HTML", params)


# update Interactions
def updateInteraction(request):

    interactionId = request.POST.get("interactionID", "")
    Type = request.POST.get("type", "")
    Notes = request.POST.get("notes", "")
    FollowUps = request.POST.get("followUp", "")
    Date = request.POST.get("date", "")

    try:
        interactionLogging.objects.filter(interactionID=interactionId).update(
            type=Type, notes=Notes, followUp=FollowUps, date=Date
        )
    except:
        return index(request)

    return index(request)


##get interaction ID to update interaction
def getLeadIDForUpdateTracking(request):
    trackingId = request.POST.get("trackingID", "")

    try:
        trackingObject = tracking.objects.filter(trackingID=trackingId).get()
    except:
        return index(request)

    params = {"trackingObject": trackingObject}

    return render(request, "KAM/updateTracker.html", params)


# update Tracker
def updateTracking(request):

    trackingId = request.POST.get("trackingID", "")
    Name = request.POST.get("name", "")
    Role = request.POST.get("role", "")
    ContactNo = request.POST.get("contactNo", "")
    email = request.POST.get("emailID", "")

    # fetching Lead ID to pass to viewleads
    try:
        leadId = tracking.objects.filter(trackingID=trackingId).get().leadID.leadID
    except:
        return index(request)

    try:
        tracking.objects.filter(trackingID=trackingId).update(
            name=Name, role=Role, phoneNumber=ContactNo, emailID=email
        )
    except:
        return index(request)

    return viewLeads(request, str(leadId))
