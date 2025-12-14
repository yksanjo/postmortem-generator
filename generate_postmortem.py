#!/usr/bin/env python3
"""
Incident Post-Mortem Template Generator

Generates structured post-mortem documents from incident information.
"""

import argparse
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path


def generate_postmortem(
    incident_name: str,
    incident_date: str,
    duration: str,
    impact: str,
    root_cause: str,
    timeline: Optional[str] = None,
    resolution: Optional[str] = None,
    action_items: Optional[list] = None
) -> str:
    """
    Generate a post-mortem document from incident details.
    
    Args:
        incident_name: Name/title of the incident
        incident_date: Date of the incident (YYYY-MM-DD)
        duration: How long the incident lasted
        impact: Description of the impact
        root_cause: Root cause analysis
        timeline: Optional timeline of events
        resolution: Optional resolution steps
        action_items: Optional list of action items
    
    Returns:
        Formatted Markdown post-mortem document
    """
    
    # Parse date
    try:
        date_obj = datetime.strptime(incident_date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except:
        formatted_date = incident_date
    
    # Generate timeline if not provided
    if not timeline:
        timeline = f"""
- **{incident_date} {datetime.now().strftime('%H:%M')} UTC**: Incident detected
- **{incident_date} {datetime.now().strftime('%H:%M')} UTC**: Investigation started
- **{incident_date} {datetime.now().strftime('%H:%M')} UTC**: Root cause identified
- **{incident_date} {datetime.now().strftime('%H:%M')} UTC**: Incident resolved
"""
    
    # Generate resolution if not provided
    if not resolution:
        resolution = """
1. Immediate mitigation steps taken
2. Root cause addressed
3. System restored to normal operation
4. Monitoring verified
"""
    
    # Default action items if not provided
    if not action_items:
        action_items = [
            "Review and update monitoring alerts",
            "Document lessons learned",
            "Update runbooks if applicable",
            "Schedule follow-up review meeting"
        ]
    
    postmortem = f"""# Post-Mortem: {incident_name}

**Date:** {formatted_date}  
**Duration:** {duration}  
**Status:** Resolved  
**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}

---

## Executive Summary

**Incident:** {incident_name}  
**Date:** {formatted_date}  
**Duration:** {duration}  
**Impact:** {impact}

This document outlines the timeline, root cause analysis, and preventive measures for the incident that occurred on {formatted_date}.

---

## Timeline

{timeline.strip()}

---

## Impact Assessment

### Affected Systems
- [ ] System/service name
- [ ] User-facing impact
- [ ] Internal tooling impact

### User Impact
{impact}

### Business Impact
- [ ] Revenue impact (if applicable)
- [ ] Customer satisfaction impact
- [ ] SLA/SLO violations

### Metrics
- **Uptime Impact:** {duration}
- **Error Rate:** [To be filled]
- **Affected Users:** [To be filled]

---

## Root Cause Analysis

### Primary Root Cause
{root_cause}

### Contributing Factors
- [ ] Factor 1: [Description]
- [ ] Factor 2: [Description]
- [ ] Factor 3: [Description]

### Why It Happened
1. **Immediate Cause:** [What directly caused the incident]
2. **Underlying Cause:** [Why the immediate cause occurred]
3. **Systemic Issues:** [Broader issues that allowed this to happen]

### Detection Gap
- [ ] Why wasn't this detected earlier?
- [ ] What monitoring/alerting was missing?
- [ ] How can we detect this faster next time?

---

## Resolution

### Immediate Actions Taken
{resolution.strip()}

### Resolution Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Verification
- [ ] System functionality verified
- [ ] Monitoring confirmed normal operation
- [ ] No residual issues detected

---

## Prevention Checklist

### Short-term (Next 1-2 Weeks)
- [ ] Fix the immediate root cause
- [ ] Add/update monitoring alerts
- [ ] Update documentation
- [ ] Communicate findings to team

### Medium-term (Next 1-3 Months)
- [ ] Implement preventive measures
- [ ] Review and update runbooks
- [ ] Conduct team training if needed
- [ ] Review similar systems for same issues

### Long-term (Ongoing)
- [ ] Regular review of incident patterns
- [ ] Continuous improvement of monitoring
- [ ] Regular post-mortem reviews
- [ ] Update incident response procedures

### Technical Improvements
- [ ] Code changes to prevent recurrence
- [ ] Infrastructure improvements
- [ ] Process improvements
- [ ] Tooling improvements

---

## Action Items

| Item | Owner | Due Date | Status | Notes |
|------|-------|----------|--------|-------|
"""
    
    for i, item in enumerate(action_items, 1):
        postmortem += f"| {item} | [Owner] | [Due Date] | Open | [Notes] |\n"
    
    postmortem += f"""
---

## Lessons Learned

### What Went Well
- [ ] Positive aspect 1
- [ ] Positive aspect 2

### What Could Be Improved
- [ ] Improvement area 1
- [ ] Improvement area 2

### Key Takeaways
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]

---

## References

- [Related tickets/PRs]
- [Monitoring dashboards]
- [Documentation links]
- [Related incidents]

---

## Sign-off

**Prepared by:** [Name]  
**Reviewed by:** [Name]  
**Date:** {formatted_date}

---

*This post-mortem was generated using the Post-Mortem Template Generator. Please review and customize as needed.*
"""
    
    return postmortem


def interactive_mode():
    """Interactive CLI mode for gathering incident information."""
    print("=" * 60)
    print("Incident Post-Mortem Generator")
    print("=" * 60)
    print()
    
    incident_name = input("1. Incident Name/Title: ").strip()
    if not incident_name:
        print("Error: Incident name is required")
        return
    
    incident_date = input("2. Incident Date (YYYY-MM-DD): ").strip()
    if not incident_date:
        incident_date = datetime.now().strftime("%Y-%m-%d")
        print(f"   Using today's date: {incident_date}")
    
    duration = input("3. Duration (e.g., '2 hours', '30 minutes'): ").strip()
    if not duration:
        duration = "Unknown"
    
    print("4. Impact Description:")
    impact = input("   ").strip()
    if not impact:
        impact = "To be documented"
    
    print("5. Root Cause:")
    root_cause = input("   ").strip()
    if not root_cause:
        root_cause = "Under investigation"
    
    print("\nOptional fields (press Enter to skip):")
    print("Timeline (press Enter twice when done, or Enter to skip):")
    timeline_lines = []
    while True:
        line = input()
        if not line:
            if timeline_lines:
                break
            else:
                timeline = None
                break
        timeline_lines.append(line)
    if timeline_lines:
        timeline = "\n".join(f"- {line}" for line in timeline_lines)
    else:
        timeline = None
    
    print("\nResolution steps (press Enter twice when done, or Enter to skip):")
    resolution_lines = []
    while True:
        line = input()
        if not line:
            if resolution_lines:
                break
            else:
                resolution = None
                break
        resolution_lines.append(line)
    if resolution_lines:
        resolution = "\n".join(f"{i+1}. {line}" for i, line in enumerate(resolution_lines))
    else:
        resolution = None
    
    # Generate post-mortem
    postmortem = generate_postmortem(
        incident_name=incident_name,
        incident_date=incident_date,
        duration=duration,
        impact=impact,
        root_cause=root_cause,
        timeline=timeline,
        resolution=resolution
    )
    
    # Save to file
    output_file = f"postmortem_{incident_date}_{incident_name.lower().replace(' ', '_')}.md"
    output_path = Path(output_file)
    
    with open(output_path, "w") as f:
        f.write(postmortem)
    
    print(f"\n✓ Post-mortem generated: {output_path}")
    print(f"\nPreview (first 500 chars):")
    print("-" * 60)
    print(postmortem[:500] + "...")


def main():
    parser = argparse.ArgumentParser(description="Generate incident post-mortem documents")
    parser.add_argument("--incident", help="Incident name/title")
    parser.add_argument("--date", help="Incident date (YYYY-MM-DD)")
    parser.add_argument("--duration", help="Duration of incident")
    parser.add_argument("--impact", help="Impact description")
    parser.add_argument("--root-cause", help="Root cause analysis")
    parser.add_argument("--timeline", help="Timeline of events (file path or text)")
    parser.add_argument("--resolution", help="Resolution steps (file path or text)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive or not all([args.incident, args.date, args.duration, args.impact, args.root_cause]):
        interactive_mode()
        return
    
    # Read timeline from file if path provided
    timeline = None
    if args.timeline:
        timeline_path = Path(args.timeline)
        if timeline_path.exists():
            with open(timeline_path, "r") as f:
                timeline = f.read()
        else:
            timeline = args.timeline
    
    # Read resolution from file if path provided
    resolution = None
    if args.resolution:
        resolution_path = Path(args.resolution)
        if resolution_path.exists():
            with open(resolution_path, "r") as f:
                resolution = f.read()
        else:
            resolution = args.resolution
    
    # Generate post-mortem
    postmortem = generate_postmortem(
        incident_name=args.incident,
        incident_date=args.date,
        duration=args.duration,
        impact=args.impact,
        root_cause=args.root_cause,
        timeline=timeline,
        resolution=resolution
    )
    
    # Save or print
    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            f.write(postmortem)
        print(f"✓ Post-mortem generated: {output_path}")
    else:
        print(postmortem)


if __name__ == "__main__":
    main()
