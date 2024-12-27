from celery import shared_task
from datetime import date
import datetime
from .models import leads, interactionLogging
import logging

logger = logging.getLogger(__name__)
date_format = "%Y/%m/%d"


@shared_task(bind=True)
def generateInteractions(self):

    # accessing all leads to Auto generate interactions according to call frequency
    try:
        allLeads = leads.objects.all()
    except:
        return None

    for item in allLeads:

        prevDate = date.today() - datetime.timedelta(days=item.callFrequency)

        # not generating interaction for inactive tasks
        if item.currentStatus != 'inactive':
            # saving new interactions generated
            if prevDate == item.lastCallMade:
                nextCallDate = date.today() + datetime.timedelta(days=item.callFrequency)
                try:
                    saveInteraction = interactionLogging(
                        type="call",
                        notes="Auto Generated",
                        followUp="No",
                        date=nextCallDate,
                        time=item.time,
                        leadID=item,
                    )
                    saveInteraction.save()
                except:
                    return None

            # updating lastCallMade
            if prevDate == date.today() - datetime.timedelta(days=item.callFrequency):
                prevDate = date.today() - datetime.timedelta(days=1)

    return None
