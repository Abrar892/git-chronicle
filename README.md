# Git Chronicle

Git repository analytics, hotspot detection, and HTML report generator.

## Features
- **Git Commit Parsing:** Extracts commit timeline, authors, commit volume, and daily cadence.
- **Contributor Leaderboards:** Ranked statistics of commits per contributor.
- **Code Churn & Hotspots:** Detects volatile files with high change frequency.
- **Interactive HTML Report:** Beautiful standalone HTML visualization with dark theme and zero external JS/CSS dependencies.
- **CLI Commands:** Command-line summaries for quick terminal inspection.

## Usage
```bash
python -m git_chronicle.cli analyze .
python -m git_chronicle.cli report . --output git-report.html
```
