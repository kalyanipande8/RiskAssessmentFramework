"""run_all.py - runs the full FMEA risk-assessment pipeline end to end."""

from fmea import (
    build_fmea_table,
    identify_critical_control_points,
    generate_recommendations,
)
from generate_report import write_csv_outputs, write_markdown_report


def main() -> None:
    fmea_df = build_fmea_table()
    ccp_df = identify_critical_control_points(fmea_df, min_ccps=18)
    ccp_recs_df = generate_recommendations(ccp_df)

    write_csv_outputs(fmea_df, ccp_recs_df)

    stats = {
        "n_failure_modes": len(fmea_df),
        "n_unit_ops": fmea_df["unit_op"].nunique(),
        "rpn_ceiling": 120,
        "n_above_ceiling": int((fmea_df["rpn"] >= 120).sum()),
        "total_rpn_before": int(ccp_recs_df["rpn"].sum()),
        "total_rpn_after": int(ccp_recs_df["new_rpn"].sum()),
        "total_rpn_reduction": int(ccp_recs_df["rpn_reduction"].sum()),
        "total_rpn_reduction_pct": round(
            ccp_recs_df["rpn_reduction"].sum() / ccp_recs_df["rpn"].sum() * 100, 1
        ),
    }
    report_path = write_markdown_report(fmea_df, ccp_recs_df, stats)

    print("=== FMEA Risk Assessment Pipeline ===")
    print(f"Total failure modes analyzed: {stats['n_failure_modes']} "
          f"across {stats['n_unit_ops']} unit operations/systems")
    print(f"Failure modes with RPN >= {stats['rpn_ceiling']}: {stats['n_above_ceiling']}")
    print(f"Critical Control Points identified: {len(ccp_recs_df)}")
    print(f"RPN range among CCPs: {ccp_recs_df['rpn'].min()}-{ccp_recs_df['rpn'].max()}")
    print(f"Total RPN (CCPs), before improvements: {stats['total_rpn_before']}")
    print(f"Total RPN (CCPs), after improvements:  {stats['total_rpn_after']}")
    print(f"Aggregate RPN reduction: {stats['total_rpn_reduction']} "
          f"points ({stats['total_rpn_reduction_pct']}%)")
    print(f"Report written to: {report_path}")
    print("Full FMEA table: output/fmea_full_table.csv")
    print("CCP table: output/critical_control_points.csv")


if __name__ == "__main__":
    main()
