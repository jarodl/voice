from django.utils import unittest
from voice.models import Request, Vote

class RequestTestCase(unittest.TestCase):
    def setUp(self):
        self.request = Request.objects.create(title='Request',
                description='This is a request', votes_needed=350)

    def testString(self):
        self.assertEqual('Request', str(self.request))

    def testDefaultState(self):
        self.assertEqual('V', self.request.state)

    def testChangesState(self):
        for i in range(0, self.request.votes_needed):
            voter = 'voter%d@domain.com' % i
            Vote.objects.create(request=self.request, voter=voter)
        self.assertEqual('W', self.request.state)

    def testVoting(self):
        Vote.objects.create(request=self.request, voter='v@d.com')
        self.assertEqual(self.request.votes.count(), 1)

class VoteTestCase(unittest.TestCase):
    def setUp(self):
        self.request = Request.objects.create(title='Request',
                description='This is a request', votes_needed=350)

    def testString(self):
        voter = 'v@d.com'
        vote = Vote.objects.create(request=self.request, voter=voter)
        self.assertEqual(voter, str(vote))
