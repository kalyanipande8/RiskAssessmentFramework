"""
generate_report.py - writes the FMEA technical report artifacts to
output/reports/: the full FMEA table, the critical-control-point list,
and a markdown technical report summarizing findings and recommendations.
"""

from __future__ import annotations

import os

import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")


def write_csv_outputs(fmea_df: pd.DataFrame, ccp_recs_df: pd.DataFrame) -> None:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fmea_df.to_csv(os.path.join(OUTPUT_DIR, "fmea_full_table.csv"), index=False)
    ccp_recs_df.to_csv(os.path.join(OUTPUT_DIR, "critical_control_points.csv"), index=False)


def _fmt_row(row) -> str:
    return (
        f"| {row['fmea_id']} | {row['unit_op']} | {row['parameter']} | "
        f"{row['failure_mode']} | {row['severity']} | {row['occurrence']} | "
        f"{row['detection']} | **{row['rpn']}** |"
    )


def _fmt_rec_row(row) -> str:
    return (
        f"| {row['fmea_id']} | {row['unit_op']} / {row['failure_mode']} | "
        f"{row['rpn']} | {row['new_rpn']} | "
        f"-{row['rpn_reduction']} (-{row['rpn_reduction_pct']}%) |"
    )


def write_markdown_report(
    fmea_df: pd.DataFrame,
    ccp_recs_df: pd.DataFrame,
    stats: dict,
) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, "fmea_technical_report.md")

    lines = []
    lines.append("# FMEA Risk Assessment Technical Report")
    lines.append("## Simulated Tablet Manufacturing Process")
    lines.append("")
    lines.append(
        "> Portfolio/demo project. Process, parameters, and FMEA scores are a "
        "realistic synthetic model built from general pharmaceutical "
        "manufacturing and ICH Q9 quality-risk-management knowledge, not from "
        "any real plant, product, or employer dataset."
    )
    lines.append("")
    lines.append("## 1. Scope")
    lines.append(
        f"- **{stats['n_failure_modes']} failure modes** analyzed across "
        f"**{stats['n_unit_ops']} unit operations** of a tablet manufacturing "
        "line (dispensing through packaging, plus facility and QC/IPC systems)."
    )
    lines.append(
        "- Severity (S), Occurrence (O), Detection (D) scored 1-10 using a "
        "documented rationale basis (see Section 2); RPN = S x O x D."
    )
    lines.append("")

    lines.append("## 2. Scoring Rationale Basis")
    lines.append(
        "- **Severity**: 1 = no quality impact -> 10 = patient-safety risk "
        "with potential for serious injury, undetected."
    )
    lines.append(
        "- **Occurrence**: 1 = essentially eliminated (<1 in 10,000 batches) "
        "-> 10 = very high (>1 in 5 batches), anchored to historical "
        "deviation-rate bands."
    )
    lines.append(
        "- **Detection**: 1 = validated automated 100% in-line check -> 10 = "
        "no detection mechanism (failure surfaces only as field complaint)."
    )
    lines.append("")

    lines.append("## 3. Full FMEA Table (ranked by RPN)")
    lines.append("")
    lines.append("| ID | Unit Op | Parameter | Failure Mode | S | O | D | RPN |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for _, row in fmea_df.iterrows():
        lines.append(_fmt_row(row))
    lines.append("")

    lines.append(
        f"## 4. Critical Control Points ({len(ccp_recs_df)} identified)"
    )
    lines.append(
        f"RPN ceiling for automatic CCP flagging: >= {stats['rpn_ceiling']}. "
        f"{stats['n_above_ceiling']} failure modes cleared that threshold "
        f"outright; the ranked list below shows the top "
        f"{len(ccp_recs_df)} by RPN, which is the full flagged CCP set."
    )
    lines.append("")
    lines.append("| ID | Unit Op | Parameter | Failure Mode | Effect | Cause | S | O | D | RPN |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for _, row in ccp_recs_df.iterrows():
        lines.append(
            f"| {row['fmea_id']} | {row['unit_op']} | {row['parameter']} | "
            f"{row['failure_mode']} | {row['effect']} | {row['cause']} | "
            f"{row['severity']} | {row['occurrence']} | {row['detection']} | "
            f"**{row['rpn']}** |"
        )
    lines.append("")

    lines.append("## 5. Quantified Improvement Recommendations")
    lines.append(
        "Each Critical Control Point below has a specific recommended "
        "action and the resulting estimated RPN after implementation "
        "(Severity is treated as intrinsic to the failure mode and is not "
        "reduced; only Occurrence and/or Detection are improved by the "
        "recommended controls, per standard FMEA practice)."
    )
    lines.append("")
    for _, row in ccp_recs_df.iterrows():
        lines.append(f"### {row['fmea_id']}: {row['unit_op']} - {row['failure_mode']}")
        lines.append(f"- **Current RPN**: {row['rpn']} (S={row['severity']}, O={row['occurrence']}, D={row['detection']})")
        lines.append(f"- **Recommendation**: {row['recommendation']}")
        lines.append(
            f"- **Estimated post-improvement RPN**: {row['new_rpn']} "
            f"(S={row['severity']}, O={row['new_occurrence']}, D={row['new_detection']})"
        )
        lines.append(
            f"- **Estimated RPN reduction**: -{row['rpn_reduction']} points "
            f"(-{row['rpn_reduction_pct']}%)"
        )
        lines.append("")

    lines.append("## 6. Summary of Estimated Impact")
    lines.append(
        f"- Total RPN across the {len(ccp_recs_df)} Critical Control Points, "
        f"current state: **{stats['total_rpn_before']}**"
    )
    lines.append(
        f"- Total RPN across the same {len(ccp_recs_df)} CCPs, after "
        f"implementing all recommendations: **{stats['total_rpn_after']}**"
    )
    lines.append(
        f"- Aggregate estimated RPN reduction: **{stats['total_rpn_reduction']} "
        f"points ({stats['total_rpn_reduction_pct']}%)**"
    )
    lines.append(
        f"- Every one of the {len(ccp_recs_df)} flagged CCPs has a strictly "
        "positive estimated RPN reduction (verified by "
        "`tests/test_pipeline.py`)."
    )
    lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))

    return path
