import pytest
from unittest.mock import patch
from django.urls import reverse
from KAM.models import KAMmail, leads


@pytest.mark.django_db
@patch("django.core.mail.send_mail")
def test_change_kam(mock_send_mail, client):
    """
    Test the process of changing a KAM for a lead:
    1. Create an old and new KAM.
    2. Assign a lead to the old KAM.
    3. Update the lead's KAM to the new one.
    4. Verify emails are sent to both old and new KAMs.
    5. Validate the database changes.
    """

    # Step 1: Create old and new KAMs
    old_kam = KAMmail.objects.create(KAMmailid="old.kam@example.com")
    new_kam = KAMmail.objects.create(KAMmailid="new.kam@example.com")

    # Step 2: Assign a lead to the old KAM
    lead = leads.objects.create(
        restaurantName="Test Restaurant",
        address="123 Main St",
        city="Test City",
        state="Test State",
        country="Test Country",
        contactNumber="9876543210",
        currentStatus="active",
        KAMID=old_kam,
        callFrequency=7,
    )

    assert lead.KAMID == old_kam

    # Step 3: Update the lead's KAM to the new KAM via the view
    data = {
        "leadId": lead.leadID,
        "name": lead.restaurantName,
        "address": lead.address,
        "city": lead.city,
        "state": lead.state,
        "country": lead.country,
        "contactNo": lead.contactNumber,
        "currentStatus": lead.currentStatus,
        "callFrequency": lead.callFrequency,
        "KAMID": new_kam.KAMID,  # Assign to the new KAM
    }
    response = client.post(reverse("updateLeads"), data)

    # Step 4: Validate the response and database changes
    assert response.status_code == 200
    lead.refresh_from_db()
    assert lead.KAMID == new_kam

    # Step 5: Verify emails sent to old and new KAMs
    assert mock_send_mail.call_count == 2  # One email for old KAM, one for new KAM

    # Check email to old KAM
    old_kam_email_call = mock_send_mail.call_args_list[0]
    assert old_kam_email_call[0][0] == f"lead deallocated to Key Account Manager ID :  {old_kam.KAMID}"
    assert old_kam_email_call[0][1].find("Please handover lead to Key Account Manager ID") != -1

    # Check email to new KAM
    new_kam_email_call = mock_send_mail.call_args_list[1]
    assert new_kam_email_call[0][0] == f"New lead allocated to Key Account Manager ID :  {new_kam.KAMID}"
    assert new_kam_email_call[0][1].find("Please initialize interaction with the Restaurant") != -1