"""Git subprocess runner for executing git queries."""
import subprocess
import os
from typing import List, Tuple, Optional


class GitError(Exception):
    pass


class GitRunner:
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)

    def run(self, cmd: List[str], timeout: int = 30) -> str:
        try:
            res = subprocess.run(
                ["git", "-C", self.repo_path] + cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            if res.returncode != 0:
                raise GitError(res.stderr.strip() or f"Git command failed with code {res.returncode}")
            return res.stdout
        except Exception as e:
            raise GitError(str(e))

    def is_valid_repo(self) -> bool:
        try:
            out = self.run(["rev-parse", "--is-inside-work-tree"])
            return out.strip() == "true"
        except GitError:
            return False

    def get_log(self, limit: Optional[int] = None) -> List[str]:
        cmd = ["log", "--format=%H|%ae|%an|%ai|%s"]
        if limit:
            cmd.extend(["-n", str(limit)])
        output = self.run(cmd)
        return [line for line in output.splitlines() if line.strip()]

    def get_branches(self) -> List[str]:
        output = self.run(["branch", "--list"])
        return [b.replace("*", "").strip() for b in output.splitlines() if b.strip()]

    def get_contributors(self) -> List[Tuple[str, str, int]]:
        output = self.run(["shortlog", "-sne", "--all"])
        res = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                count = int(parts[0].strip())
                author_info = parts[1].strip()
                if "<" in author_info and ">" in author_info:
                    name, email = author_info.split("<", 1)
                    res.append((name.strip(), email.replace(">", "").strip(), count))
                else:
                    res.append((author_info, "", count))
        return res
