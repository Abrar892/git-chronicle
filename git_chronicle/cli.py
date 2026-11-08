"""CLI entry point for git-chronicle."""
import argparse
import os
from git_chronicle.git_runner import GitRunner
from git_chronicle.analyzer import GitAnalyzer
from git_chronicle.metrics import MetricsEngine
from git_chronicle.reporter import generate_text_report, generate_html_report


def main():
    parser = argparse.ArgumentParser(description="Git Chronicle - Repository Analytics and Visualization")
    parser.add_argument("repo_path", nargs="?", default=".", help="Target Git repository path")
    parser.add_argument("--html", help="Generate standalone HTML report to target filepath")
    args = parser.parse_args()

    runner = GitRunner(args.repo_path)
    if not runner.is_valid_repo():
        print(f"Error: '{args.repo_path}' is not a valid git repository.")
        return

    analyzer = GitAnalyzer(runner)
    metrics = MetricsEngine(runner, analyzer)
    repo_name = os.path.basename(os.path.abspath(args.repo_path))

    if args.html:
        html = generate_html_report(analyzer, metrics, repo_name=repo_name)
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML analytics report saved to {args.html}")
    else:
        print(generate_text_report(analyzer, metrics, repo_name=repo_name))


if __name__ == "__main__":
    main()
