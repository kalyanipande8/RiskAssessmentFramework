import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fmea import (
    build_fmea_table,
    identify_critical_control_points,
    generate_recommendations,
)


def test_fmea_table_builds_and_scores_are_in_range():
    df = build_fmea_table()
    assert len(df) > 0
    for col in ("severity", "occurrence", "detection"):
        assert df[col].between(1, 10).all()


def test_rpn_arithmetic_is_correct():
    df = build_fmea_table()
    expected = df["severity"] * df["occurrence"] * df["detection"]
    assert (df["rpn"] == expected).all()
    # spot check a known row combination exists and is internally consistent
    for _, row in df.iterrows():
        assert row["rpn"] == row["severity"] * row["occurrence"] * row["detection"]


def test_at_least_18_critical_control_points_identified():
    df = build_fmea_table()
    ccp = identify_critical_control_points(df, min_ccps=18)
    assert len(ccp) >= 18


def test_ccps_are_the_highest_ranked_failure_modes():
    df = build_fmea_table()
    ccp = identify_critical_control_points(df, min_ccps=18)
    # every CCP's RPN must be >= the lowest RPN outside the CCP set
    min_ccp_rpn = ccp["rpn"].min()
    non_ccp = df[~df["fmea_id"].isin(ccp["fmea_id"])]
    if len(non_ccp) > 0:
        assert min_ccp_rpn >= non_ccp["rpn"].max()


def test_recommendations_reduce_rpn_for_every_flagged_ccp():
    df = build_fmea_table()
    ccp = identify_critical_control_points(df, min_ccps=18)
    recs = generate_recommendations(ccp)

    assert len(recs) >= 18
    # every single flagged CCP must show a strict RPN reduction
    assert (recs["new_rpn"] < recs["rpn"]).all()
    assert (recs["rpn_reduction"] > 0).all()
    # new RPN arithmetic must be correct
    expected_new = recs["severity"] * recs["new_occurrence"] * recs["new_detection"]
    assert (recs["new_rpn"] == expected_new).all()
    # severity must never be reduced (not something a process control fixes)
    assert (recs["new_occurrence"] <= recs["occurrence"]).all()
    assert (recs["new_detection"] <= recs["detection"]).all()
    # every recommendation has real text
    assert (recs["recommendation"].str.len() > 20).all()


def test_recommendation_text_is_specific_not_generic_placeholder():
    df = build_fmea_table()
    ccp = identify_critical_control_points(df, min_ccps=18)
    recs = generate_recommendations(ccp)
    # ensure recommendations aren't all identical (would indicate boilerplate)
    assert recs["recommendation"].nunique() >= len(recs) - 2
