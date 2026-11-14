"""Tests for git_chronicle histogram and comparator modules."""

import unittest
from datetime import datetime
from git_chronicle.analyzer import CommitRecord
from git_chronicle.histogram import CommitHistogram
from git_chronicle.comparator import MultiRepoComparator, RepoSummary


class TestHistogramAndComparator(unittest.TestCase):
    def setUp(self):
        self.commits = [
            CommitRecord(hash="c1", author_email="a@test.com", author_name="A", timestamp=datetime(2026, 11, 9, 10, 0, 0), subject="Mon commit"), # Nov 9, 2026 is Monday
            CommitRecord(hash="c2", author_email="b@test.com", author_name="B", timestamp=datetime(2026, 11, 10, 14, 0, 0), subject="Tue commit"), # Nov 10, 2026 is Tuesday
            CommitRecord(hash="c3", author_email="a@test.com", author_name="A", timestamp=datetime(2026, 11, 10, 15, 0, 0), subject="Tue commit 2"),
        ]

    def test_weekday_histogram(self):
        hist = CommitHistogram(self.commits)
        by_day = hist.commits_by_weekday()
        self.assertEqual(by_day["Monday"], 1)
        self.assertEqual(by_day["Tuesday"], 2)
        self.assertEqual(by_day["Wednesday"], 0)
        
        rendered = hist.render_ascii_weekday()
        self.assertIn("Tuesday", rendered)
        self.assertIn("##", rendered)

    def test_hour_histogram(self):
        hist = CommitHistogram(self.commits)
        by_hour = hist.commits_by_hour()
        self.assertEqual(by_hour[10], 1)
        self.assertEqual(by_hour[14], 1)
        self.assertEqual(by_hour[15], 1)
        self.assertEqual(by_hour[0], 0)

    def test_comparator_render(self):
        comp = MultiRepoComparator([])
        rendered = comp.render_comparison_text()
        self.assertIn("MULTI-REPOSITORY COMPARISON MATRIX", rendered)


if __name__ == "__main__":
    unittest.main()
