"""
fmea.py - FMEA-style risk assessment engine for a simulated pharmaceutical
oral solid dosage (tablet) manufacturing process.

Builds a Failure Mode and Effects Analysis (FMEA) table across the unit
operations of a tablet manufacturing line, scores each failure mode on
Severity (S), Occurrence (O), and Detection (D) using a documented 1-10
rationale basis (standard AIAG/FMEA-style anchors adapted to pharma
manufacturing), computes the Risk Priority Number (RPN = S x O x D),
flags the highest-RPN failure modes as Critical Control Points (CCPs),
and generates a quantified improvement recommendation for each CCP with
an estimated post-improvement RPN.

This is a portfolio/demo project. The process, parameters, and FMEA
scores are a realistic but synthetic model built from general pharma
manufacturing / ICH Q9 quality-risk-management knowledge -- not from any
real plant, product, or employer dataset.
"""

from __future__ import annotations

import pandas as pd

# ---------------------------------------------------------------------------
# Scoring rationale (documented basis, 1-10 scale, standard FMEA anchors)
# ---------------------------------------------------------------------------
SEVERITY_SCALE = {
    1: "No discernible effect on product quality or patient safety.",
    2: "Minor effect, cosmetic only, no quality impact.",
    3: "Slight effect; in-spec but near edge of normal variability.",
    4: "Minor quality attribute drift; reworkable without patient impact.",
    5: "Moderate quality impact; batch requires investigation/deviation.",
    6: "Significant quality impact; partial batch rejection likely.",
    7: "Major quality impact; batch rejection, no patient exposure.",
    8: "Critical quality attribute (CQA) failure; risk of out-of-spec release.",
    9: "Patient safety risk without warning (e.g., content uniformity, "
       "dissolution failure reaching market).",
    10: "Patient safety risk with potential for serious injury (e.g., "
        "dose failure, contamination reaching patient undetected).",
}

OCCURRENCE_SCALE = {
    1: "Failure essentially eliminated by design; <1 in 10,000 batches.",
    2: "Very rare; ~1 in 5,000 batches (historical deviation rate).",
    3: "Rare; ~1 in 2,000 batches.",
    4: "Occasional; ~1 in 500 batches.",
    5: "Occasional-moderate; ~1 in 200 batches.",
    6: "Moderate; ~1 in 100 batches.",
    7: "Moderate-frequent; ~1 in 50 batches.",
    8: "Frequent; ~1 in 20 batches.",
    9: "High; ~1 in 10 batches.",
    10: "Very high; failure occurs almost every batch (>1 in 5).",
}

DETECTION_SCALE = {
    1: "Automated 100% in-line/PAT sensor with validated alarm, no bypass.",
    2: "Automated in-line monitoring, periodic manual verification.",
    3: "Automated at-line testing every batch, fast turnaround.",
    4: "Manual in-process check every batch (e.g., IPC weight checks).",
    5: "Manual in-process check at fixed intervals (e.g., every 30 min).",
    6: "End-of-stage sampling/testing (e.g., blend uniformity at discharge).",
    7: "Release testing only (QC lab, post-batch).",
    8: "Periodic/skip-lot testing; not every batch verified.",
    9: "Relies on operator visual inspection only, no instrumental check.",
    10: "No detection mechanism; failure would only surface as a field "
        "complaint or stability failure.",
}

RPN_CEILING_FOR_CCP = 120  # failure modes scoring >= this are Critical Control Points

# ---------------------------------------------------------------------------
# FMEA source data: (unit_op, parameter, failure_mode, effect, cause,
#                     severity, occurrence, detection)
# ---------------------------------------------------------------------------
FMEA_ROWS = [
    # --- Dispensing / Raw Material Weighing ---
    ("Dispensing", "API weight", "API under-weighed into batch", "Sub-potent tablets", "Balance drift / operator transcription error", 9, 3, 4),
    ("Dispensing", "API weight", "API over-weighed into batch", "Super-potent tablets", "Balance drift / wrong tare", 9, 2, 4),
    ("Dispensing", "Excipient weight", "Lubricant (Mg stearate) over-weighed", "Reduced dissolution rate", "Operator error / scale miscalibration", 6, 4, 5),
    ("Dispensing", "Material ID", "Wrong raw material lot staged", "Cross-contamination / wrong formulation", "Barcode scan bypassed", 10, 2, 2),
    ("Dispensing", "Balance calibration", "Balance out of calibration", "Systematic weighing error across batch", "Missed calibration schedule", 8, 2, 6),

    # --- Blending ---
    ("Blending", "Blend time", "Under-blending", "Poor content uniformity (CQA)", "Timer bypass / power interruption", 9, 4, 6),
    ("Blending", "Blend time", "Over-blending", "Lubricant over-lubrication, reduced dissolution", "Operator error, no auto shut-off", 6, 5, 6),
    ("Blending", "Blender speed (RPM)", "Blender speed deviation", "Non-homogeneous blend", "VFD drift / mechanical wear", 7, 3, 6,),
    ("Blending", "Blend uniformity", "Segregation during discharge", "Content uniformity failure at tablet press", "Poor bin design / vibration during transfer", 9, 4, 7),

    # --- Granulation (wet granulation) ---
    ("Granulation", "Water addition rate", "Water added too fast", "Over-wetted granules, poor flow", "Pump calibration drift", 6, 4, 5),
    ("Granulation", "Granulation endpoint", "Endpoint (power consumption) missed", "Inconsistent granule size distribution", "Sensor miscalibration / manual override", 7, 3, 5),
    ("Granulation", "Binder concentration", "Binder solution under-concentrated", "Weak, friable granules", "Prep error in binder makeup", 6, 3, 6),

    # --- Drying (fluid bed dryer) ---
    ("Drying", "Inlet air temperature", "Inlet temp exceeds setpoint", "API degradation, granule discoloration", "Heater control loop fault", 7, 3, 4),
    ("Drying", "Drying endpoint (LOD)", "Under-drying (residual moisture high)", "Microbial risk, poor stability, capping on compression", "LOD probe drift / rushed cycle", 8, 4, 6),
    ("Drying", "Drying endpoint (LOD)", "Over-drying", "Reduced tablet hardness, friability", "Extended cycle beyond endpoint", 5, 4, 6),
    ("Drying", "Air flow rate", "Fluidization air flow loss", "Localized over-heating of granule bed", "Filter clogging / damper fault", 6, 3, 5),

    # --- Milling ---
    ("Milling", "Screen size / mill speed", "Screen tear or wrong screen installed", "Oversized granule fraction, poor uniformity", "Improper changeover verification", 6, 2, 7),
    ("Milling", "Mill speed (RPM)", "Mill speed deviation", "Inconsistent particle size distribution", "Motor control fault", 6, 3, 6),

    # --- Compression (tablet press) ---
    ("Compression", "Compression force", "Compression force too low", "Soft tablets, friability failure, breakage in transit", "Punch wear / press tooling drift", 7, 5, 4),
    ("Compression", "Compression force", "Compression force too high", "Over-hard tablets, delayed dissolution", "Press setpoint error", 7, 4, 4),
    ("Compression", "Tablet weight", "Tablet weight out of range", "Dose non-uniformity (CQA)", "Feed frame starvation / powder flow variability", 9, 5, 3),
    ("Compression", "Tablet hardness", "Hardness variability within batch", "Inconsistent dissolution profile across batch", "Powder flow inconsistency, turret speed variation", 7, 5, 5),
    ("Compression", "Press speed (turret RPM)", "Press speed exceeds validated range", "Capping/lamination defects, weight variability", "Operator override to meet throughput target", 7, 4, 5),
    ("Compression", "Punch/die wear", "Excessive punch tip wear", "Sticking, picking, visual defects", "Exceeded punch maintenance interval", 5, 5, 6),

    # --- Coating ---
    ("Coating", "Spray rate", "Spray rate too high relative to drying", "Tablet twinning, coating defects, over-wetting", "Pump calibration / recipe error", 5, 4, 5),
    ("Coating", "Pan speed", "Pan speed deviation", "Uneven coating distribution, appearance defects", "Drive control fault", 4, 3, 6),
    ("Coating", "Inlet air temperature", "Coating inlet temp too low", "Incomplete film formation, tackiness", "HVAC/AHU fault", 6, 3, 5),
    ("Coating", "Coating weight gain", "Under-coating (weight gain below target)", "Inadequate moisture/taste barrier, modified release failure", "Spray interruption not detected", 7, 3, 6),
    ("Coating", "Coating weight gain", "Over-coating (weight gain above target)", "Delayed/failed dissolution for enteric or MR product", "Extended spray cycle beyond endpoint", 8, 3, 6),

    # --- Packaging ---
    ("Packaging", "Blister seal integrity", "Incomplete heat seal", "Moisture ingress, stability failure in field", "Sealing roller temperature drift", 8, 3, 7),
    ("Packaging", "Label/carton reconciliation", "Wrong label applied", "Mislabeling, patient safety/recall risk", "Line clearance failure, changeover error", 10, 2, 3),
    ("Packaging", "Fill count", "Incorrect tablet count per bottle", "Under/over dispensing to patient", "Counter miscalibration / fill-line jam", 8, 3, 4),
    ("Packaging", "Desiccant insertion", "Missing desiccant", "Accelerated moisture-related degradation in field", "Feeder jam not detected", 6, 3, 7),

    # --- Environmental / Facility (cross-cutting) ---
    ("Facility", "Room relative humidity", "RH excursion during granulation/compression", "Hygroscopic API degradation, capping", "HVAC dehumidification fault", 7, 4, 6),
    ("Facility", "Compressed air quality", "Moisture/oil carryover in compressed air", "Contamination of product-contact surfaces", "Filter/dryer maintenance lapse", 7, 2, 7),
    ("Facility", "Equipment cleaning verification", "Inadequate cleaning between batches/products", "Cross-contamination, carryover of prior product", "Cleaning validation swab missed / rushed turnover", 10, 2, 5),

    # --- In-process control / Quality systems ---
    ("QC/IPC", "In-process sampling", "IPC sample not representative of batch", "Out-of-spec batch released undetected", "Sampling plan not followed (grab vs. composite)", 8, 3, 6),
    ("QC/IPC", "Deviation handling", "Deviation not escalated per procedure", "Systemic issue recurs, undetected trend", "Training gap / procedural non-compliance", 7, 4, 7),
    ("QC/IPC", "Equipment calibration program", "Calibration overdue on critical instrument", "Measurement bias propagates across multiple batches", "Calibration tracking system gap", 7, 3, 5),
    ("QC/IPC", "Change control", "Process change implemented without re-validation", "Unqualified process drift, unknown CQA impact", "Change control bypass under schedule pressure", 8, 2, 6),
]

COLUMNS = [
    "unit_op", "parameter", "failure_mode", "effect", "cause",
    "severity", "occurrence", "detection",
]


def build_fmea_table() -> pd.DataFrame:
    """Assemble the FMEA dataframe and compute RPN for every failure mode."""
    df = pd.DataFrame(FMEA_ROWS, columns=COLUMNS)
    df["rpn"] = df["severity"] * df["occurrence"] * df["detection"]
    df["severity_rationale"] = df["severity"].map(SEVERITY_SCALE)
    df["occurrence_rationale"] = df["occurrence"].map(OCCURRENCE_SCALE)
    df["detection_rationale"] = df["detection"].map(DETECTION_SCALE)
    df = df.sort_values("rpn", ascending=False).reset_index(drop=True)
    df.insert(0, "fmea_id", [f"FM-{i+1:03d}" for i in range(len(df))])
    return df


def identify_critical_control_points(df: pd.DataFrame, min_ccps: int = 18) -> pd.DataFrame:
    """
    Flag Critical Control Points: failure modes at/above the RPN ceiling.
    If fewer than `min_ccps` clear that bar, extend down the ranked list
    until at least `min_ccps` are flagged (guarantees the required minimum
    coverage while keeping the ranking RPN-driven).
    """
    ccp = df[df["rpn"] >= RPN_CEILING_FOR_CCP].copy()
    if len(ccp) < min_ccps:
        ccp = df.head(min_ccps).copy()
    return ccp.sort_values("rpn", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Recommendations: each is a concrete, quantified action mapped to a specific
# failure-mode pattern, with an explicit new O and/or D score it is expected
# to achieve. The mapping is matched by (unit_op, failure_mode) so every CCP
# gets a specific, non-generic action rather than boilerplate text.
# ---------------------------------------------------------------------------
def _rule_based_recommendation(row) -> tuple[str, int, int]:
    """
    Return (recommendation_text, new_occurrence, new_detection).
    Severity is treated as intrinsic to the failure mode's clinical/quality
    consequence and is not reduced by process controls (per standard FMEA
    practice) -- only occurrence and/or detection are improved.
    """
    fm = row["failure_mode"]
    op = row["unit_op"]
    o, d = row["occurrence"], row["detection"]

    # Default conservative improvement if no specific rule matches.
    new_o, new_d = max(o - 1, 1), max(d - 1, 1)
    text = (f"Tighten {row['parameter'].lower()} control limits and add a "
            f"documented secondary verification step for {op}.")

    rules = {
        "API under-weighed into batch": (
            "Add dual-verification (second-operator check) weighing step and "
            "interface balance directly to batch record system to eliminate "
            "transcription error.", max(o - 2, 1), max(d - 2, 1)),
        "API over-weighed into batch": (
            "Add dual-verification weighing step with automated tare "
            "confirmation before dispense.", max(o - 1, 1), max(d - 2, 1)),
        "Wrong raw material lot staged": (
            "Enforce hard barcode-scan interlock that physically prevents "
            "dispensing until material ID is system-verified (no manual "
            "override).", max(o - 1, 1), 1),
        "Balance out of calibration": (
            "Move balance calibration from scheduled-only to calibration-due "
            "automated lockout (balance disabled past due date).", max(o - 1, 1), max(d - 3, 1)),
        "Under-blending": (
            "Install in-line NIR blend-uniformity monitoring to replace fixed "
            "timer endpoint with a real-time homogeneity endpoint.", max(o - 2, 1), 2),
        "Over-blending": (
            "Add automatic blender shut-off tied to validated blend-time "
            "setpoint with high-time alarm.", max(o - 2, 1), max(d - 2, 1)),
        "Blender speed deviation": (
            "Add continuous VFD speed logging with automated deviation alarm "
            "at +/-5% of setpoint.", max(o - 1, 1), max(d - 2, 1)),
        "Segregation during discharge": (
            "Redesign discharge chute to minimize free-fall/vibration and add "
            "post-discharge uniformity sampling at 3 bin locations every "
            "batch.", max(o - 1, 1), max(d - 2, 1)),
        "Water added too fast": (
            "Add mass-flow controller with closed-loop rate control in place "
            "of open-loop pump setpoint.", max(o - 2, 1), max(d - 1, 1)),
        "Endpoint (power consumption) missed": (
            "Switch granulation endpoint determination to torque/power-based "
            "automated endpoint with operator override disabled.", max(o - 2, 1), max(d - 2, 1)),
        "Binder solution under-concentrated": (
            "Add refractometer/density in-line check of binder solution "
            "immediately before use, every batch.", max(o - 1, 1), max(d - 3, 1)),
        "Inlet temp exceeds setpoint": (
            "Add redundant high-temperature interlock with automatic heater "
            "cutoff independent of primary control loop.", max(o - 1, 1), max(d - 2, 1)),
        "Under-drying (residual moisture high)": (
            "Replace fixed-time drying with in-line NIR moisture endpoint "
            "determination, verified against LOD every batch.", max(o - 2, 1), max(d - 3, 1)),
        "Over-drying": (
            "Add automated endpoint cutoff referencing validated LOD target "
            "band, +/-0.2%.", max(o - 1, 1), max(d - 2, 1)),
        "Fluidization air flow loss": (
            "Add differential-pressure filter-monitoring sensor with "
            "preventive filter-change alarm before flow drops below "
            "threshold.", max(o - 1, 1), max(d - 2, 1)),
        "Screen tear or wrong screen installed": (
            "Add mandatory photo-verification changeover checklist scanned "
            "into batch record before mill start.", max(o - 1, 1), max(d - 3, 1)),
        "Mill speed deviation": (
            "Add continuous speed logging with automated deviation alarm.",
            max(o - 1, 1), max(d - 2, 1)),
        "Compression force too low": (
            "Add automated force-feedback rejection (reject-on-force-band) at "
            "the press, 100% tablet screening instead of periodic IPC.", max(o - 2, 1), max(d - 1, 1)),
        "Compression force too high": (
            "Add automated force-feedback rejection with narrowed force band "
            "(tightened from vendor default +/-15% to +/-7%).", max(o - 1, 1), max(d - 1, 1)),
        "Tablet weight out of range": (
            "Install 100% checkweigher with automated reject at the press "
            "discharge (replacing periodic manual IPC weight checks).", max(o - 1, 1), max(d - 2, 1)),
        "Hardness variability within batch": (
            "Add feed-frame powder-level sensor with low-level alarm and "
            "increase hardness IPC frequency from every 30 min to every 15 "
            "min.", max(o - 1, 1), max(d - 1, 1)),
        "Press speed exceeds validated range": (
            "Lock turret speed to validated range via software limit; remove "
            "operator override capability.", max(o - 2, 1), max(d - 1, 1)),
        "Excessive punch tip wear": (
            "Shift punch maintenance from calendar-based to cycle-count-based "
            "preventive replacement (replace at 80% of validated wear life).", max(o - 2, 1), max(d - 1, 1)),
        "Spray rate too high relative to drying": (
            "Add closed-loop spray-rate control referenced to exhaust air "
            "dew point rather than fixed pump setpoint.", max(o - 1, 1), max(d - 1, 1)),
        "Pan speed deviation": (
            "Add continuous pan-speed logging with automated deviation "
            "alarm.", max(o - 1, 1), max(d - 2, 1)),
        "Coating inlet temp too low": (
            "Add redundant AHU temperature sensor with automated low-temp "
            "alarm independent of primary control loop.", max(o - 1, 1), max(d - 1, 1)),
        "Under-coating (weight gain below target)": (
            "Add in-line spray-interruption detection with automatic cycle "
            "pause and operator alert.", max(o - 1, 1), max(d - 2, 1)),
        "Over-coating (weight gain above target)": (
            "Switch from time-based to weight-gain-based automated spray "
            "endpoint (in-process tablet sampling every 15 min).", max(o - 1, 1), max(d - 2, 1)),
        "Incomplete heat seal": (
            "Add 100% in-line seal-integrity vision inspection with automatic "
            "reject (replacing periodic pull tests).", max(o - 1, 1), max(d - 3, 1)),
        "Wrong label applied": (
            "Add vision-system label verification with hard line stop on "
            "mismatch (replacing manual line-clearance check alone).", max(o - 1, 1), 1),
        "Incorrect tablet count per bottle": (
            "Add redundant electronic count verification (checkweigh by "
            "bottle weight) downstream of the primary counter.", max(o - 1, 1), max(d - 2, 1)),
        "Missing desiccant": (
            "Add vision-based desiccant-presence check per bottle with "
            "automatic reject.", max(o - 1, 1), max(d - 3, 1)),
        "RH excursion during granulation/compression": (
            "Add redundant RH sensor with automated process-hold interlock "
            "if RH exceeds validated range for >5 minutes.", max(o - 1, 1), max(d - 2, 1)),
        "Moisture/oil carryover in compressed air": (
            "Increase compressed-air quality testing frequency from annual "
            "to quarterly, with continuous dew-point monitoring added.", max(o - 1, 1), max(d - 3, 1)),
        "Inadequate cleaning between batches/products": (
            "Add mandatory swab/TOC verification with quantitative pass/fail "
            "limit before next-product changeover is permitted.", max(o - 1, 1), max(d - 2, 1)),
        "IPC sample not representative of batch": (
            "Replace grab sampling with validated stratified composite "
            "sampling plan per batch.", max(o - 1, 1), max(d - 2, 1)),
        "Deviation not escalated per procedure": (
            "Add electronic QMS workflow with automatic escalation timer "
            "(deviation auto-escalates if not actioned within 24h).", max(o - 1, 1), max(d - 2, 1)),
        "Calibration overdue on critical instrument": (
            "Implement automated calibration-due lockout at the instrument "
            "level (instrument disabled past due date).", max(o - 1, 1), max(d - 3, 1)),
        "Process change implemented without re-validation": (
            "Add electronic change-control gate that blocks batch release "
            "until re-validation checklist is signed off.", max(o - 1, 1), max(d - 2, 1)),
    }

    if fm in rules:
        text, new_o, new_d = rules[fm]
    return text, new_o, new_d


def generate_recommendations(ccp_df: pd.DataFrame) -> pd.DataFrame:
    """Add recommendation, estimated new O/D, new RPN, and RPN reduction."""
    recs = ccp_df.copy()
    texts, new_os, new_ds = [], [], []
    for _, row in recs.iterrows():
        text, new_o, new_d = _rule_based_recommendation(row)
        texts.append(text)
        new_os.append(new_o)
        new_ds.append(new_d)
    recs["recommendation"] = texts
    recs["new_occurrence"] = new_os
    recs["new_detection"] = new_ds
    recs["new_rpn"] = recs["severity"] * recs["new_occurrence"] * recs["new_detection"]
    recs["rpn_reduction"] = recs["rpn"] - recs["new_rpn"]
    recs["rpn_reduction_pct"] = (recs["rpn_reduction"] / recs["rpn"] * 100).round(1)
    return recs
