from django.utils import unittest
from django.db import IntegrityError
from voice.models import Feature, Vote

class FeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.feature = Feature.objects.create(title='Feature',
                description='This is a feature', votes_needed=350)

    def testString(self):
        self.assertEqual('Feature', str(self.feature))

    def testDefaultState(self):
        self.assertEqual('V', self.feature.state)

    def testChangesState(self):
        for i in range(0, self.feature.votes_needed):
            voter = 'voter%d@domain.com' % i
            Vote.objects.create(feature=self.feature, voter=voter)
        self.assertEqual('W', self.feature.state)

    def testVoting(self):
        Vote.objects.create(feature=self.feature, voter='v@d.com')
        self.assertEqual(self.feature.votes.count(), 1)

class VoteTestCase(unittest.TestCase):
    def setUp(self):
        self.feature = Feature.objects.create(title='Feature',
                description='This is a feature', votes_needed=350)

    def testString(self):
        voter = 'v@d.com'
        vote = Vote.objects.create(feature=self.feature, voter=voter)
        self.assertEqual(voter, str(vote))

    def testDisallowDuplicates(self):
        voter = 'v@d.com'
        vote = Vote.objects.create(feature=self.feature, voter=voter)
        self.assertRaises(IntegrityError, Vote.objects.create,
                feature=self.feature, voter=voter)

    def testDecreasesVotesNeeded(self):
        for i in range(0, self.feature.votes_needed):
            voter = 'voter%d@domain.com' % i
            vote = Vote.objects.create(feature=self.feature, voter=voter)

        self.assertEqual(self.feature.votes_left(), 0)

        for i in range(self.feature.votes_needed + 1,
                self.feature.votes_needed * 2):
            voter = 'voter%d@domain.com' % i
            vote = Vote.objects.create(feature=self.feature, voter=voter)

        self.assertEqual(self.feature.votes_left(), 0)
