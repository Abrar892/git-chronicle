"""Full test suite for git-chronicle."""
import unittest
import tempfile
import subprocess
import os
from git_chronicle.git_runner import GitRunner
from git_chronicle.analyzer import GitAnalyzer
from git_chronicle.metrics import MetricsEngine
from git_chronicle.reporter import generate_text_report, generate_html_report


class TestGitChronicle(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        subprocess.run(["git", "init", self.test_dir], check=True, capture_output=True)
        subprocess.run(["git", "-C", self.test_dir, "config", "user.name", "TestUser"], check=True)
        subprocess.run(["git", "-C", self.test_dir, "config", "user.email", "test@example.com"], check=True)

        # Create sample commit
        file1 = os.path.join(self.test_dir, "file1.txt")
        with open(file1, "w") as f:
            f.write("Line 1\nLine 2\n")
        subprocess.run(["git", "-C", self.test_dir, "add", "."], check=True)
        subprocess.run(["git", "-C", self.test_dir, "commit", "-m", "initial commit"], check=True, capture_output=True)

        self.runner = GitRunner(self.test_dir)
        self.analyzer = GitAnalyzer(self.runner)
        self.metrics = MetricsEngine(self.runner, self.analyzer)

    def test_repo_validation(self):
        self.assertTrue(self.runner.is_valid_repo())
        invalid_runner = GitRunner(os.path.join(self.test_dir, "nonexistent"))
        self.assertFalse(invalid_runner.is_valid_repo())

    def test_commits_parsing(self):
        commits = self.analyzer.parse_commits()
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].subject, "initial commit")
        self.assertEqual(commits[0].author_name, "TestUser")

    def test_hotspots(self):
        hotspots = self.metrics.compute_hotspots()
        self.assertGreaterEqual(len(hotspots), 1)
        self.assertEqual(hotspots[0].filepath, "file1.txt")

    def test_reports(self):
        text = generate_text_report(self.analyzer, self.metrics, "TestRepo")
        self.assertIn("GIT CHRONICLE", text)
        self.assertIn("TestUser", text)

        html = generate_html_report(self.analyzer, self.metrics, "TestRepo")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("TestRepo", html)


if __name__ == "__main__":
    unittest.main()
