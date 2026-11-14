"""comparator.py — Multi-repository comparison and comparative metrics engine."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any
from git_chronicle.git_runner import GitRunner
from git_chronicle.analyzer import GitAnalyzer


@dataclass
class RepoSummary:
    repo_path: str
    total_commits: int
    total_authors: int
    top_author: str


class MultiRepoComparator:
    """Compare multiple git repositories side-by-side."""

    def __init__(self, repo_paths: List[str]):
        self.repo_paths = repo_paths

    def summarize_all(self) -> List[RepoSummary]:
        summaries = []
        for path in self.repo_paths:
            runner = GitRunner(path)
            analyzer = GitAnalyzer(runner)
            commits = analyzer.parse_commits()
            by_author = analyzer.commits_by_author()
            top_author = "None"
            if by_author:
                top_author = max(by_author.items(), key=lambda kv: len(kv[1]))[0]

            summaries.append(
                RepoSummary(
                    repo_path=path,
                    total_commits=len(commits),
                    total_authors=len(by_author),
                    top_author=top_author,
                )
            )
        return summaries

    def render_comparison_text(self) -> str:
        summaries = self.summarize_all()
        lines = [
            "=" * 70,
            " MULTI-REPOSITORY COMPARISON MATRIX",
            "=" * 70,
            f"{'Repository Path':<35} | {'Commits':<8} | {'Authors':<8} | {'Top Contributor':<15}",
            "-" * 70,
        ]
        for s in summaries:
            short_path = s.repo_path[-33:] if len(s.repo_path) > 33 else s.repo_path
            lines.append(f"{short_path:<35} | {s.total_commits:<8} | {s.total_authors:<8} | {s.top_author:<15}")
        lines.append("=" * 70)
        return "\n".join(lines)
