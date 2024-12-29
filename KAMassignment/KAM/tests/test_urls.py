from django.test import SimpleTestCase
from django.urls import reverse, resolve
from KAM import views 


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_KAMIDforleads_url_resolves(self):
        url = reverse('KAMIDforleads')
        self.assertEqual(resolve(url).func, views.KAMIDforleads)

    def test_addKAM_url_resolves(self):
        url = reverse('addKAM')
        self.assertEqual(resolve(url).func, views.addKAM)

    def test_deleteKAM_url_resolves(self):
        url = reverse('deleteKAM')
        self.assertEqual(resolve(url).func, views.deleteKAM)

    def test_showKAM_url_resolves(self):
        url = reverse('showKAM')
        self.assertEqual(resolve(url).func, views.showKAM)

    def test_performanceTracking_url_resolves(self):
        url = reverse('performanceTracking')
        self.assertEqual(resolve(url).func, views.performanceTracking)

    def test_viewLeads_url_resolves(self):
        url = reverse('viewLeads')
        self.assertEqual(resolve(url).func, views.viewLeads)

    def test_createLeads_url_resolves(self):
        url = reverse('createLeads')
        self.assertEqual(resolve(url).func, views.createLeads)

    def test_deleteLead_url_resolves(self):
        url = reverse('deleteLead')
        self.assertEqual(resolve(url).func, views.deleteLead)

    def test_getLeadIDForUpdateLead_url_resolves(self):
        url = reverse('getLeadIDForUpdateLead')
        self.assertEqual(resolve(url).func, views.getLeadIDForUpdateLead)

    def test_updateLeads_url_resolves(self):
        url = reverse('updateLeads')
        self.assertEqual(resolve(url).func, views.updateLeads)

    def test_addInteraction_url_resolves(self):
        url = reverse('addInteraction')
        self.assertEqual(resolve(url).func, views.addInteraction)

    def test_deleteInteraction_url_resolves(self):
        url = reverse('deleteInteraction')
        self.assertEqual(resolve(url).func, views.deleteInteraction)

    def test_getLeadIDForInteraction_url_resolves(self):
        url = reverse('getLeadIDForInteraction')
        self.assertEqual(resolve(url).func, views.getLeadIDForInteraction)

    def test_getLeadIDForUpdateInteraction_url_resolves(self):
        url = reverse('getLeadIDForUpdateInteraction')
        self.assertEqual(resolve(url).func, views.getLeadIDForUpdateInteraction)

    def test_updateInteraction_url_resolves(self):
        url = reverse('updateInteraction')
        self.assertEqual(resolve(url).func, views.updateInteraction)

    def test_searchResult_url_resolves(self):
        url = reverse('searchResult')
        self.assertEqual(resolve(url).func, views.searchResult)

    def test_createTracker_url_resolves(self):
        url = reverse('createTracker')
        self.assertEqual(resolve(url).func, views.createTracker)

    def test_deleteTracking_url_resolves(self):
        url = reverse('deleteTracking')
        self.assertEqual(resolve(url).func, views.deleteTracking)

    def test_getLeadIDForTracker_url_resolves(self):
        url = reverse('getLeadIDForTracker')
        self.assertEqual(resolve(url).func, views.getLeadIDForTracker)

    def test_getLeadIDForUpdateTracking_url_resolves(self):
        url = reverse('getLeadIDForUpdateTracking')
        self.assertEqual(resolve(url).func, views.getLeadIDForUpdateTracking)

    def test_updateTracking_url_resolves(self):
        url = reverse('updateTracking')
        self.assertEqual(resolve(url).func, views.updateTracking)
