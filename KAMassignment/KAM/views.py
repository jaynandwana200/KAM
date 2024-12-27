from django.shortcuts import render, HttpResponse
from .models import leads, interactionLogging, tracking, KAMmail
from datetime import date
from django.core.mail import send_mail
from KAMassignment.settings import EMAIL_HOST_USER
import datetime
import logging

logger = logging.getLogger(__name__)


# send mail to new KAM on new Task allotment
def sendMail(kid,KAMmailid,resAddress,number,status,City,State,Country,name,allocationStatus,newKAMid = "NULL"):
    
    finalStatement = ""

    if(allocationStatus == 'allocate'):
        subject = "New lead allocated to Key Account Manager ID :  " + kid
        finalStatement = "Please initialize interaction with the Restaurant"

    elif(allocationStatus == 'deallocate'):
        subject = "lead deallocated to Key Account Manager ID :  " + kid
        finalStatement = "Please handover lead to Key Account Manager ID  :  " + newKAMid

    message = (
        "Details of allocated lead : \n \n"
        + "Restaurant Name  :  " + name
        + "\n"
        + "Address  :  " + resAddress + ", " + City + ", " + State + ", " + Country
        + "\n"
        + "Contact Number  :  " + number
        + "\n"
        + "Status  :  " + status
        + "\n \n" 
        +finalStatement
    )
    recipient_list = [KAMmailid]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)


#send mail new/update interaction
def sendMailInteraction(interactionStatus, leadID,type, notes, followUp, Date, time, mail,name,number):

    if(interactionStatus == "new"):
        subject = "New interaction scheduled for Lead ID  :  " + leadID
        firstStatement = "Details of Scheduled Interaction  : \n \n"
    elif(interactionStatus == "update"):
        subject = "Interaction Updated for Lead ID  :  " + leadID
        firstStatement = "Details of Updated Interaction  : \n \n"

    message = (
        firstStatement
        + "Restaurant Name  :  " + name
        + "\n"
        + "Contact Number : " + number
        + "\n"
        + "Type  :  " + type
        + "\n"
        + "Notes  :  " + notes
        + "\n"
        + "Follow Up  :  " + followUp
        + "\n"
        + "Date  :  " + Date
        + "\n"
        + "Time  :  " + time + " Hrs "
        + "\n \n"
    )
    recipient_list = [mail]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)


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


# get KAMID for createleads
def KAMIDforleads(request):

    try:
        allKAMID = KAMmail.objects.all()
    except:
        return index(request)

    params = {"KAMID": allKAMID}

    return render(request, "KAM/createLeads.html", params)


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

    # finding object related to KAMID
    try:
        kamID = KAMmail.objects.filter(KAMID=KID).get()
    except:
        return createLeads(request)

    # creating record in table
    try:
        create = leads(
            restaurantName=name,
            address=resAddress,
            contactNumber=number,
            currentStatus=status,
            KAMID=kamID,
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

    # seding mail To KAM about lead allocated to it

    sendMail(KID,kamID.KAMmailid,resAddress,number,status,City,status,Country,name,"allocate")


    return index(request)


# fetching lead id for get LeadID
def getLeadIDForUpdateLead(request):
    leadId = request.POST.get("LeadID", "")

    try:
        leadObject = leads.objects.filter(leadID=leadId).get()
        KAMID = KAMmail.objects.all()
    except:
        return index(request)

    params = {"leadObject": leadObject, "KAMID": KAMID}  # used to store parameters

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

    # finding KAMID to get old KAMID mail if modified
    try:
        oldKAMID = leads.objects.filter(leadID = leadId).get()
        oldKAMIDmail = KAMmail.objects.filter(KAMID = oldKAMID.KAMID.KAMID).get()
    except:
        oldKAMID = None
        oldKAMIDmail= None

    # getting KAMID object as it is a foreign key
    try:
        ID = KAMmail.objects.filter(KAMID=KAMId).get()
    except:
        return updateLeads(request)

    # deleting all interactions if status updated to inactive
    if status == "inactive":
        interactionLogging.objects.filter(leadID__leadID__contains=leadId).delete()

    try:
        leads.objects.filter(leadID=leadId).update(
            restaurantName=name,
            address=location,
            city=City,
            state=State,
            country=Country,
            contactNumber=number,
            currentStatus=status,
            callFrequency=callFreq,
            KAMID=ID,
        )
    except:
        return index(request)

    # seding mail to respective KAMID
    if(KAMId != oldKAMIDmail.KAMID):
        sendMail(KAMId,ID.KAMmailid,location,number,status,City,status,Country,name,"allocate")
        sendMail(oldKAMIDmail.KAMID,oldKAMIDmail.KAMmailid,location,number,status,City,status,Country,name,"deallocate",KAMId)

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

    # getting KAMID for fetch mail ID
    try:
        KAMid = leads.objects.filter(leadID = ID).get()
        mail = KAMmail.objects.filter(KAMID = KAMid.KAMID)
    except:
        return index(request)

    # Sending mail to KAMID about new interaction scheduling
    sendMailInteraction("new", ID,Type, Note, follow, Date, Time, mail)

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

    return render(request, "KAM/updateInteraction.html", params)


# chnage 12 hr to 24 hr format
def convert24(s = ""):

    hrs = int(s[0:2])
    mins = s[3:5]
    period = s[6:10]
    time = ""

    print(hrs)
    print(mins)
    print(period)

    if(period == "a.m." and hrs == 12):
        time = "00:00:00"
    elif(period == "a.m."):
            time = str(hrs) + ":"+ mins + ":00"
    else:
        hrs += 12
        time = str(hrs) + ":" + mins + ":00"

    return time


# update Interactions
def updateInteraction(request):

    interactionId = request.POST.get("interactionID", "")
    Type = request.POST.get("type", "")
    Notes = request.POST.get("notes", "")
    FollowUps = request.POST.get("followUp", "")
    Date = request.POST.get("date", "")
    Time = request.POST.get("time", "")
    Time = convert24(Time)
    

    try:
        interactionLogging.objects.filter(interactionID=interactionId).update(
            type=Type, notes=Notes, followUp=FollowUps, date=Date, time = Time
        )
    except:
        return index(request)

    # getting leadid
    try:
        leadObject = interactionLogging.objects.filter(interactionID = interactionId).get()
        ID = leadObject.leadID.leadID
    except:
        return index(request)
    
    # getting mailID of KAMID
    try:
        mail = KAMmail.objects.filter(KAMID = leadObject.leadID.KAMID.KAMID).get()
    except:
        return index(request)

    #send mail to KAM about update in interaction 
    restaurantName = leadObject.leadID.restaurantName
    restaurantNumber = leadObject.leadID.contactNumber
    sendMailInteraction("update", str(ID),Type, Notes, FollowUps, Date, Time, mail.KAMmailid,restaurantName,restaurantNumber)

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
