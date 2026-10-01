# RiskAssessmentFramework: FMEA Risk Assessment for Manufacturing

Builds a real Failure Mode and Effects Analysis (FMEA) for a simulated
pharmaceutical tablet manufacturing process: scores Severity (S),
Occurrence (O), and Detection (D) for every failure mode against a
documented 1-10 rationale basis, computes the Risk Priority Number
(RPN = S x O x D), flags the highest-risk failure modes as Critical
Control Points (CCPs), and generates a specific, quantified improvement
recommendation for each one.

> **Disclaimer:** This is a portfolio/demo project. The process, unit
> operations, and FMEA scores are a realistic but **synthetically
> constructed** model built from general pharmaceutical manufacturing and
> ICH Q9 quality-risk-management knowledge. No real plant, product, or
> employer data is used.

## The process modeled

A tablet manufacturing line with 10 unit operations / systems:
**Dispensing -> Blending -> Granulation -> Drying -> Milling ->
Compression -> Coating -> Packaging**, plus two cross-cutting systems,
**Facility** (environmental controls) and **QC/IPC** (in-process quality
systems), since failure modes in those areas drive risk just as much as
the physical unit operations.

## What it does

1. **`fmea.py`** holds the FMEA source data (40 failure modes, each with
   a unit operation, parameter, effect, and root cause) and the scoring
   engine:
   - Severity, Occurrence, and Detection are each assigned on a 1-10
     scale against a **documented rationale table** (e.g. Detection=1
     means "validated automated 100% in-line check," Detection=10 means
     "no detection mechanism, surfaces only as a field complaint").
   - RPN = S x O x D is computed per failure mode.
   - Failure modes with RPN >= 120 (or the top 18 by RPN, whichever is
     larger) are flagged as **Critical Control Points**.
   - A rule-based recommendation engine maps each CCP's specific failure
     mode to a concrete corrective action (e.g. "replace fixed-time
     drying with in-line NIR moisture endpoint determination") and
     computes the resulting post-improvement RPN by reducing Occurrence
     and/or Detection only -- Severity is treated as intrinsic to the
     failure mode's quality/safety consequence and is never discounted.

2. **`generate_report.py`** writes the full FMEA table and CCP table to
   CSV and assembles a markdown technical report
   (`output/reports/fmea_technical_report.md`) with the scoring
   rationale, the ranked FMEA table, the CCP list, and a
   recommendation + quantified RPN reduction for every CCP.

3. **`run_all.py`** runs the whole pipeline end to end.

## How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_all.py
pytest -q
```

## Results

_All numbers below are copied directly from an actual run of `python
run_all.py` -- nothing is hardcoded; the FMEA source data is fixed, so
re-running reproduces these exactly._

- **40 failure modes** analyzed across **10 unit operations/systems**.
- **20 failure modes scored RPN >= 120** and were flagged as **Critical
  Control Points** -- exceeding the 18+ target.
- CCP RPN range: **120 - 252**.
- Highest-risk CCP: **FM-001, Blending - "Segregation during discharge"**
  (S=9, O=4, D=7, **RPN=252**) -- poor bin design and transfer vibration
  can desegregate an otherwise well-blended batch right before
  compression, risking a content-uniformity failure that would otherwise
  go undetected until release testing.
- Total RPN across the 20 CCPs, current state: **3,138**.
- Total RPN across the same 20 CCPs, after implementing all 20
  recommendations: **1,354**.
- **Aggregate estimated RPN reduction: 1,784 points (56.9%)**.
- Every one of the 20 flagged CCPs has a strictly positive RPN reduction
  from its paired recommendation (enforced by
  `tests/test_pipeline.py::test_recommendations_reduce_rpn_for_every_flagged_ccp`).

### Example recommendations (highest-RPN CCPs)

| CCP | Failure Mode | Current RPN | Recommendation | New RPN | Reduction |
|---|---|---|---|---|---|
| FM-001 | Segregation during discharge (Blending) | 252 | Redesign discharge chute to minimize free-fall/vibration; add post-discharge uniformity sampling at 3 bin locations every batch | 135 | -117 (-46.4%) |
| FM-002 | Under-blending | 216 | Install in-line NIR blend-uniformity monitoring to replace fixed-timer endpoint with a real-time homogeneity endpoint | 36 | -180 (-83.3%) |
| FM-014 | Tablet weight out of range (Compression) | 135 | Install 100% checkweigher with automated reject at press discharge, replacing periodic manual IPC checks | 36 | -99 (-73.3%) |

(Full table of all 20 recommendations in
`output/reports/fmea_technical_report.md` and
`output/critical_control_points.csv`.)

### Test suite

```
6 passed in 0.26s
```

Covers: RPN arithmetic correctness (sanity check against raw S x O x D),
score ranges (1-10), at least 18 Critical Control Points identified,
CCPs are genuinely the highest-ranked failure modes, and every flagged
CCP's recommendation produces a strict RPN reduction.

## Repo layout

```
fmea.py                 # FMEA data, scoring, CCP identification, recommendations
generate_report.py      # writes CSV + markdown technical report
run_all.py               # runs the full pipeline
tests/test_pipeline.py  # pytest suite
output/
  fmea_full_table.csv
  critical_control_points.csv
  reports/fmea_technical_report.md
```
