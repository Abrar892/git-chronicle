"""File churn and hotspot metrics computation."""
from dataclasses import dataclass
from typing import List, Dict
from git_chronicle.git_runner import GitRunner
from git_chronicle.analyzer import GitAnalyzer


@dataclass
class FileMetrics:
    filepath: str
    churn_score: int
    commits_count: int


class MetricsEngine:
    def __init__(self, runner: GitRunner, analyzer: GitAnalyzer):
        self.runner = runner
        self.analyzer = analyzer

    def compute_hotspots(self, limit_commits: int = 50, top_n: int = 10) -> List[FileMetrics]:
        commits = self.analyzer.parse_commits(limit=limit_commits)
        churn_map: Dict[str, int] = {}
        commits_map: Dict[str, int] = {}

        for c in commits:
            try:
                out = self.runner.run(["show", "--numstat", "--format=", c.hash])
                for line in out.splitlines():
                    parts = line.strip().split("\t")
                    if len(parts) == 3:
                        add_str, del_str, path = parts
                        add = int(add_str) if add_str.isdigit() else 0
                        delete = int(del_str) if del_str.isdigit() else 0
                        churn_map[path] = churn_map.get(path, 0) + (add + delete)
                        commits_map[path] = commits_map.get(path, 0) + 1
            except Exception:
                continue

        sorted_files = sorted(churn_map.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [
            FileMetrics(
                filepath=path,
                churn_score=score,
                commits_count=commits_map.get(path, 1)
            )
            for path, score in sorted_files
        ]
