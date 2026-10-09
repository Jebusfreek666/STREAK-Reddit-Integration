import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from collector_preview import collect_preview, normalized_record, PermissionRequired


class FakeReddit:
    read_only = True
    def __init__(self):
        self.calls = 0
    def subreddit(self, name):
        self.calls += 1
        if name != 'wallstreetbets':
            raise ValueError(name)
        return self
    def new(self, limit):
        t = datetime(2026, 10, 9, 12, tzinfo=timezone.utc).timestamp()
        return [SimpleNamespace(id='abc', created_utc=t, title='Fictional XYZ', selftext='discussion', author='sample')]


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeReddit()
        self.now = datetime(2026, 10, 9, 13, tzinfo=timezone.utc)
    def test_no_approval_no_api_calls(self):
        with self.assertRaises(PermissionRequired):
            collect_preview(self.client, {}, author_key=b'x' * 32, now=self.now)
        self.assertEqual(self.client.calls, 0)
    def test_scope_required(self):
        with self.assertRaises(PermissionRequired):
            collect_preview(self.client, {'reddit_approval_reference':'fictional-test', 'public_posts_approved':True}, author_key=b'x'*32, now=self.now)
        self.assertEqual(self.client.calls, 0)
    def test_synthetic_metadata(self):
        evidence = {'reddit_approval_reference':'fictional-test', 'public_posts_approved':True, 'personal_financial_use_approved':True}
        records, meta = collect_preview(self.client, evidence, author_key=b'x'*32, now=self.now)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['source_id'], 't3_abc')
        self.assertNotIn('sample', str(records[0]['author_pseudonym']))
        self.assertFalse(meta['coverage_complete'])
    def test_comment_scope_requires_separate_approval(self):
        evidence = {'reddit_approval_reference':'fictional-test', 'public_posts_approved':True, 'personal_financial_use_approved':True}
        with self.assertRaises(PermissionRequired):
            collect_preview(self.client, evidence, author_key=b'x'*32, now=self.now, include_comments=True)
        self.assertEqual(self.client.calls, 0)

if __name__ == '__main__':
    unittest.main()
