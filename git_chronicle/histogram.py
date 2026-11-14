"""histogram.py — Commit frequency distribution across days of the week and hours."""

from __future__ import annotations
from collections import Counter
from typing import Dict, List, Any
from git_chronicle.analyzer import CommitRecord


DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class CommitHistogram:
    """Computes time-based commit histograms (day-of-week, hour-of-day)."""

    def __init__(self, commits: List[CommitRecord]):
        self.commits = commits

    def commits_by_weekday(self) -> Dict[str, int]:
        """Return dict mapping day name (Monday..Sunday) to commit count."""
        counts = {day: 0 for day in DAYS_OF_WEEK}
        for c in self.commits:
            day_name = c.timestamp.strftime("%A")
            if day_name in counts:
                counts[day_name] += 1
        return counts

    def commits_by_hour(self) -> Dict[int, int]:
        """Return dict mapping hour (0..23) to commit count."""
        counts = {h: 0 for h in range(24)}
        for c in self.commits:
            counts[c.timestamp.hour] += 1
        return counts

    def render_ascii_weekday(self, width: int = 30) -> str:
        """Render an ASCII bar chart of commits by day of the week."""
        counts = self.commits_by_weekday()
        max_val = max(counts.values()) if counts and max(counts.values()) > 0 else 1
        lines = ["--- Commits by Weekday ---"]
        for day in DAYS_OF_WEEK:
            val = counts[day]
            bar_len = int((val / max_val) * width) if max_val > 0 else 0
            bar = "#" * bar_len
            lines.append(f"{day:<10} | {bar:<{width}} ({val})")
        return "\n".join(lines)
