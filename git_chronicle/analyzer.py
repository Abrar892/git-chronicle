"""Commit parsing and repository analytics engine."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from git_chronicle.git_runner import GitRunner


@dataclass
class CommitRecord:
    hash: str
    author_email: str
    author_name: str
    timestamp: datetime
    subject: str


class GitAnalyzer:
    def __init__(self, runner: GitRunner):
        self.runner = runner

    def parse_commits(self, limit: Optional[int] = None) -> List[CommitRecord]:
        raw_lines = self.runner.get_log(limit=limit)
        commits = []
        for line in raw_lines:
            parts = line.split("|", 4)
            if len(parts) >= 5:
                chash, email, name, date_str, subject = parts
                try:
                    dt = datetime.fromisoformat(date_str.strip())
                except Exception:
                    dt = datetime.now()
                commits.append(
                    CommitRecord(
                        hash=chash.strip(),
                        author_email=email.strip(),
                        author_name=name.strip(),
                        timestamp=dt,
                        subject=subject.strip()
                    )
                )
        return commits

    def total_commits(self) -> int:
        return len(self.parse_commits())

    def commits_by_author(self) -> Dict[str, List[CommitRecord]]:
        commits = self.parse_commits()
        res = {}
        for c in commits:
            res.setdefault(c.author_email, []).append(c)
        return res

    def commits_by_day(self) -> Dict[str, int]:
        commits = self.parse_commits()
        res = {}
        for c in commits:
            day_str = c.timestamp.strftime("%Y-%m-%d")
            res[day_str] = res.get(day_str, 0) + 1
        return res

    def most_active_contributors(self, n: int = 10) -> List[tuple]:
        author_map = self.commits_by_author()
        sorted_authors = sorted(author_map.items(), key=lambda x: len(x[1]), reverse=True)
        out = []
        for email, commits in sorted_authors[:n]:
            name = commits[0].author_name if commits else email
            out.append((name, email, len(commits)))
        return out
