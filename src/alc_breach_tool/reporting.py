from collections import Counter


def build_summary(results: list[dict]) -> str:
    total_emails = len(results)
    breached_emails = sum(1 for result in results if result.get("breached") is True)
    non_breached_emails = sum(1 for result in results if result.get("breached") is False)

    breach_counter = Counter()

    for result in results:
        for breach in result.get("breaches", []):
            breach_counter[breach] += 1

    top_sources = breach_counter.most_common(10)

    lines = [
        "# Analyst Summary",
        "",
        "## Overview",
        f"- Emails analysed: {total_emails}",
        f"- Breached emails: {breached_emails}",
        f"- Non-breached emails: {non_breached_emails}",
        "",
        "## Top Breach Sources",
    ]

    if top_sources:
        for source, count in top_sources:
            lines.append(f"- {source}: {count}")
    else:
        lines.append("- No breach sources identified")

    lines.extend([
        "",
        "## Notes",
        "- Invalid email addresses were skipped before API submission.",
        "- Duplicate email addresses were removed during input processing.",
        "- Results depend on the coverage and limitations of the selected breach-intelligence API.",
    ])

    return "\n".join(lines)