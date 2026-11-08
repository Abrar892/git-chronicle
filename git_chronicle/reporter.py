"""HTML and text reports generator for git-chronicle."""
from git_chronicle.analyzer import GitAnalyzer
from git_chronicle.metrics import MetricsEngine


def generate_text_report(analyzer: GitAnalyzer, metrics: MetricsEngine, repo_name: str = "Repository") -> str:
    total = analyzer.total_commits()
    contributors = analyzer.most_active_contributors(5)
    hotspots = metrics.compute_hotspots(top_n=5)

    lines = [
        "=" * 60,
        f"  GIT CHRONICLE REPORT — {repo_name}",
        "=" * 60,
        f"Total Commits: {total}",
        "-" * 60,
        "Top Contributors:",
    ]
    for name, email, count in contributors:
        lines.append(f"  - {name} <{email}>: {count} commits")

    lines.append("-" * 60)
    lines.append("Top Hotspot Files (by churn score):")
    for h in hotspots:
        lines.append(f"  - {h.filepath} (churn: {h.churn_score}, commits: {h.commits_count})")

    lines.append("=" * 60)
    return "\n".join(lines)


def generate_html_report(analyzer: GitAnalyzer, metrics: MetricsEngine, repo_name: str = "Repository") -> str:
    total = analyzer.total_commits()
    contributors = analyzer.most_active_contributors(10)
    hotspots = metrics.compute_hotspots(top_n=10)
    commits = analyzer.parse_commits(limit=20)

    contrib_rows = "".join(
        f"<tr><td>{name}</td><td>{email}</td><td>{count}</td></tr>"
        for name, email, count in contributors
    )
    hotspot_rows = "".join(
        f"<tr><td><code>{h.filepath}</code></td><td>{h.churn_score}</td><td>{h.commits_count}</td></tr>"
        for h in hotspots
    )
    commit_rows = "".join(
        f"<tr><td><code>{c.hash[:7]}</code></td><td>{c.timestamp.strftime('%Y-%m-%d')}</td>"
        f"<td>{c.author_name}</td><td>{c.subject}</td></tr>"
        for c in commits
    )

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Git Chronicle - {repo_name}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #090d16; color: #f1f5f9; padding: 24px; }}
        h1 {{ color: #38bdf8; }}
        .metric-badge {{ background: #1e293b; padding: 12px 20px; border-radius: 8px; display: inline-block; margin-bottom: 20px; }}
        .card {{ background: #111827; border: 1px solid #1f2937; padding: 20px; border-radius: 8px; margin-bottom: 24px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #1f2937; text-align: left; font-size: 14px; }}
        th {{ background: #030712; color: #9ca3af; }}
        code {{ color: #a78bfa; }}
    </style>
</head>
<body>
    <h1>Git Chronicle — {repo_name}</h1>
    <div class="metric-badge">
        <strong>Total Commits:</strong> {total}
    </div>

    <div class="card">
        <h2>Top Contributors</h2>
        <table>
            <thead><tr><th>Name</th><th>Email</th><th>Commits</th></tr></thead>
            <tbody>{contrib_rows}</tbody>
        </table>
    </div>

    <div class="card">
        <h2>Code Hotspots & Churn</h2>
        <table>
            <thead><tr><th>File Path</th><th>Churn Score</th><th>Commits</th></tr></thead>
            <tbody>{hotspot_rows}</tbody>
        </table>
    </div>

    <div class="card">
        <h2>Recent Commit Log (Last 20)</h2>
        <table>
            <thead><tr><th>Hash</th><th>Date</th><th>Author</th><th>Subject</th></tr></thead>
            <tbody>{commit_rows}</tbody>
        </table>
    </div>
</body>
</html>"""
