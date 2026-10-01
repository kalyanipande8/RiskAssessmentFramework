# FMEA Risk Assessment Technical Report
## Simulated Tablet Manufacturing Process

> Portfolio/demo project. Process, parameters, and FMEA scores are a realistic synthetic model built from general pharmaceutical manufacturing and ICH Q9 quality-risk-management knowledge, not from any real plant, product, or employer dataset.

## 1. Scope
- **40 failure modes** analyzed across **10 unit operations** of a tablet manufacturing line (dispensing through packaging, plus facility and QC/IPC systems).
- Severity (S), Occurrence (O), Detection (D) scored 1-10 using a documented rationale basis (see Section 2); RPN = S x O x D.

## 2. Scoring Rationale Basis
- **Severity**: 1 = no quality impact -> 10 = patient-safety risk with potential for serious injury, undetected.
- **Occurrence**: 1 = essentially eliminated (<1 in 10,000 batches) -> 10 = very high (>1 in 5 batches), anchored to historical deviation-rate bands.
- **Detection**: 1 = validated automated 100% in-line check -> 10 = no detection mechanism (failure surfaces only as field complaint).

## 3. Full FMEA Table (ranked by RPN)

| ID | Unit Op | Parameter | Failure Mode | S | O | D | RPN |
|---|---|---|---|---|---|---|---|
| FM-001 | Blending | Blend uniformity | Segregation during discharge | 9 | 4 | 7 | **252** |
| FM-002 | Blending | Blend time | Under-blending | 9 | 4 | 6 | **216** |
| FM-003 | QC/IPC | Deviation handling | Deviation not escalated per procedure | 7 | 4 | 7 | **196** |
| FM-004 | Drying | Drying endpoint (LOD) | Under-drying (residual moisture high) | 8 | 4 | 6 | **192** |
| FM-005 | Blending | Blend time | Over-blending | 6 | 5 | 6 | **180** |
| FM-006 | Compression | Tablet hardness | Hardness variability within batch | 7 | 5 | 5 | **175** |
| FM-007 | Facility | Room relative humidity | RH excursion during granulation/compression | 7 | 4 | 6 | **168** |
| FM-008 | Packaging | Blister seal integrity | Incomplete heat seal | 8 | 3 | 7 | **168** |
| FM-009 | Compression | Punch/die wear | Excessive punch tip wear | 5 | 5 | 6 | **150** |
| FM-010 | QC/IPC | In-process sampling | IPC sample not representative of batch | 8 | 3 | 6 | **144** |
| FM-011 | Coating | Coating weight gain | Over-coating (weight gain above target) | 8 | 3 | 6 | **144** |
| FM-012 | Compression | Compression force | Compression force too low | 7 | 5 | 4 | **140** |
| FM-013 | Compression | Press speed (turret RPM) | Press speed exceeds validated range | 7 | 4 | 5 | **140** |
| FM-014 | Compression | Tablet weight | Tablet weight out of range | 9 | 5 | 3 | **135** |
| FM-015 | Packaging | Desiccant insertion | Missing desiccant | 6 | 3 | 7 | **126** |
| FM-016 | Coating | Coating weight gain | Under-coating (weight gain below target) | 7 | 3 | 6 | **126** |
| FM-017 | Blending | Blender speed (RPM) | Blender speed deviation | 7 | 3 | 6 | **126** |
| FM-018 | Drying | Drying endpoint (LOD) | Over-drying | 5 | 4 | 6 | **120** |
| FM-019 | Granulation | Water addition rate | Water added too fast | 6 | 4 | 5 | **120** |
| FM-020 | Dispensing | Excipient weight | Lubricant (Mg stearate) over-weighed | 6 | 4 | 5 | **120** |
| FM-021 | Compression | Compression force | Compression force too high | 7 | 4 | 4 | **112** |
| FM-022 | Dispensing | API weight | API under-weighed into batch | 9 | 3 | 4 | **108** |
| FM-023 | Milling | Mill speed (RPM) | Mill speed deviation | 6 | 3 | 6 | **108** |
| FM-024 | Granulation | Binder concentration | Binder solution under-concentrated | 6 | 3 | 6 | **108** |
| FM-025 | QC/IPC | Equipment calibration program | Calibration overdue on critical instrument | 7 | 3 | 5 | **105** |
| FM-026 | Granulation | Granulation endpoint | Endpoint (power consumption) missed | 7 | 3 | 5 | **105** |
| FM-027 | Coating | Spray rate | Spray rate too high relative to drying | 5 | 4 | 5 | **100** |
| FM-028 | Facility | Equipment cleaning verification | Inadequate cleaning between batches/products | 10 | 2 | 5 | **100** |
| FM-029 | Facility | Compressed air quality | Moisture/oil carryover in compressed air | 7 | 2 | 7 | **98** |
| FM-030 | Packaging | Fill count | Incorrect tablet count per bottle | 8 | 3 | 4 | **96** |
| FM-031 | Dispensing | Balance calibration | Balance out of calibration | 8 | 2 | 6 | **96** |
| FM-032 | QC/IPC | Change control | Process change implemented without re-validation | 8 | 2 | 6 | **96** |
| FM-033 | Drying | Air flow rate | Fluidization air flow loss | 6 | 3 | 5 | **90** |
| FM-034 | Coating | Inlet air temperature | Coating inlet temp too low | 6 | 3 | 5 | **90** |
| FM-035 | Drying | Inlet air temperature | Inlet temp exceeds setpoint | 7 | 3 | 4 | **84** |
| FM-036 | Milling | Screen size / mill speed | Screen tear or wrong screen installed | 6 | 2 | 7 | **84** |
| FM-037 | Coating | Pan speed | Pan speed deviation | 4 | 3 | 6 | **72** |
| FM-038 | Dispensing | API weight | API over-weighed into batch | 9 | 2 | 4 | **72** |
| FM-039 | Packaging | Label/carton reconciliation | Wrong label applied | 10 | 2 | 3 | **60** |
| FM-040 | Dispensing | Material ID | Wrong raw material lot staged | 10 | 2 | 2 | **40** |

## 4. Critical Control Points (20 identified)
RPN ceiling for automatic CCP flagging: >= 120. 20 failure modes cleared that threshold outright; the ranked list below shows the top 20 by RPN, which is the full flagged CCP set.

| ID | Unit Op | Parameter | Failure Mode | Effect | Cause | S | O | D | RPN |
|---|---|---|---|---|---|---|---|---|---|
| FM-001 | Blending | Blend uniformity | Segregation during discharge | Content uniformity failure at tablet press | Poor bin design / vibration during transfer | 9 | 4 | 7 | **252** |
| FM-002 | Blending | Blend time | Under-blending | Poor content uniformity (CQA) | Timer bypass / power interruption | 9 | 4 | 6 | **216** |
| FM-003 | QC/IPC | Deviation handling | Deviation not escalated per procedure | Systemic issue recurs, undetected trend | Training gap / procedural non-compliance | 7 | 4 | 7 | **196** |
| FM-004 | Drying | Drying endpoint (LOD) | Under-drying (residual moisture high) | Microbial risk, poor stability, capping on compression | LOD probe drift / rushed cycle | 8 | 4 | 6 | **192** |
| FM-005 | Blending | Blend time | Over-blending | Lubricant over-lubrication, reduced dissolution | Operator error, no auto shut-off | 6 | 5 | 6 | **180** |
| FM-006 | Compression | Tablet hardness | Hardness variability within batch | Inconsistent dissolution profile across batch | Powder flow inconsistency, turret speed variation | 7 | 5 | 5 | **175** |
| FM-007 | Facility | Room relative humidity | RH excursion during granulation/compression | Hygroscopic API degradation, capping | HVAC dehumidification fault | 7 | 4 | 6 | **168** |
| FM-008 | Packaging | Blister seal integrity | Incomplete heat seal | Moisture ingress, stability failure in field | Sealing roller temperature drift | 8 | 3 | 7 | **168** |
| FM-009 | Compression | Punch/die wear | Excessive punch tip wear | Sticking, picking, visual defects | Exceeded punch maintenance interval | 5 | 5 | 6 | **150** |
| FM-011 | Coating | Coating weight gain | Over-coating (weight gain above target) | Delayed/failed dissolution for enteric or MR product | Extended spray cycle beyond endpoint | 8 | 3 | 6 | **144** |
| FM-010 | QC/IPC | In-process sampling | IPC sample not representative of batch | Out-of-spec batch released undetected | Sampling plan not followed (grab vs. composite) | 8 | 3 | 6 | **144** |
| FM-012 | Compression | Compression force | Compression force too low | Soft tablets, friability failure, breakage in transit | Punch wear / press tooling drift | 7 | 5 | 4 | **140** |
| FM-013 | Compression | Press speed (turret RPM) | Press speed exceeds validated range | Capping/lamination defects, weight variability | Operator override to meet throughput target | 7 | 4 | 5 | **140** |
| FM-014 | Compression | Tablet weight | Tablet weight out of range | Dose non-uniformity (CQA) | Feed frame starvation / powder flow variability | 9 | 5 | 3 | **135** |
| FM-015 | Packaging | Desiccant insertion | Missing desiccant | Accelerated moisture-related degradation in field | Feeder jam not detected | 6 | 3 | 7 | **126** |
| FM-016 | Coating | Coating weight gain | Under-coating (weight gain below target) | Inadequate moisture/taste barrier, modified release failure | Spray interruption not detected | 7 | 3 | 6 | **126** |
| FM-017 | Blending | Blender speed (RPM) | Blender speed deviation | Non-homogeneous blend | VFD drift / mechanical wear | 7 | 3 | 6 | **126** |
| FM-018 | Drying | Drying endpoint (LOD) | Over-drying | Reduced tablet hardness, friability | Extended cycle beyond endpoint | 5 | 4 | 6 | **120** |
| FM-019 | Granulation | Water addition rate | Water added too fast | Over-wetted granules, poor flow | Pump calibration drift | 6 | 4 | 5 | **120** |
| FM-020 | Dispensing | Excipient weight | Lubricant (Mg stearate) over-weighed | Reduced dissolution rate | Operator error / scale miscalibration | 6 | 4 | 5 | **120** |

## 5. Quantified Improvement Recommendations
Each Critical Control Point below has a specific recommended action and the resulting estimated RPN after implementation (Severity is treated as intrinsic to the failure mode and is not reduced; only Occurrence and/or Detection are improved by the recommended controls, per standard FMEA practice).

### FM-001: Blending - Segregation during discharge
- **Current RPN**: 252 (S=9, O=4, D=7)
- **Recommendation**: Redesign discharge chute to minimize free-fall/vibration and add post-discharge uniformity sampling at 3 bin locations every batch.
- **Estimated post-improvement RPN**: 135 (S=9, O=3, D=5)
- **Estimated RPN reduction**: -117 points (-46.4%)

### FM-002: Blending - Under-blending
- **Current RPN**: 216 (S=9, O=4, D=6)
- **Recommendation**: Install in-line NIR blend-uniformity monitoring to replace fixed timer endpoint with a real-time homogeneity endpoint.
- **Estimated post-improvement RPN**: 36 (S=9, O=2, D=2)
- **Estimated RPN reduction**: -180 points (-83.3%)

### FM-003: QC/IPC - Deviation not escalated per procedure
- **Current RPN**: 196 (S=7, O=4, D=7)
- **Recommendation**: Add electronic QMS workflow with automatic escalation timer (deviation auto-escalates if not actioned within 24h).
- **Estimated post-improvement RPN**: 105 (S=7, O=3, D=5)
- **Estimated RPN reduction**: -91 points (-46.4%)

### FM-004: Drying - Under-drying (residual moisture high)
- **Current RPN**: 192 (S=8, O=4, D=6)
- **Recommendation**: Replace fixed-time drying with in-line NIR moisture endpoint determination, verified against LOD every batch.
- **Estimated post-improvement RPN**: 48 (S=8, O=2, D=3)
- **Estimated RPN reduction**: -144 points (-75.0%)

### FM-005: Blending - Over-blending
- **Current RPN**: 180 (S=6, O=5, D=6)
- **Recommendation**: Add automatic blender shut-off tied to validated blend-time setpoint with high-time alarm.
- **Estimated post-improvement RPN**: 72 (S=6, O=3, D=4)
- **Estimated RPN reduction**: -108 points (-60.0%)

### FM-006: Compression - Hardness variability within batch
- **Current RPN**: 175 (S=7, O=5, D=5)
- **Recommendation**: Add feed-frame powder-level sensor with low-level alarm and increase hardness IPC frequency from every 30 min to every 15 min.
- **Estimated post-improvement RPN**: 112 (S=7, O=4, D=4)
- **Estimated RPN reduction**: -63 points (-36.0%)

### FM-007: Facility - RH excursion during granulation/compression
- **Current RPN**: 168 (S=7, O=4, D=6)
- **Recommendation**: Add redundant RH sensor with automated process-hold interlock if RH exceeds validated range for >5 minutes.
- **Estimated post-improvement RPN**: 84 (S=7, O=3, D=4)
- **Estimated RPN reduction**: -84 points (-50.0%)

### FM-008: Packaging - Incomplete heat seal
- **Current RPN**: 168 (S=8, O=3, D=7)
- **Recommendation**: Add 100% in-line seal-integrity vision inspection with automatic reject (replacing periodic pull tests).
- **Estimated post-improvement RPN**: 64 (S=8, O=2, D=4)
- **Estimated RPN reduction**: -104 points (-61.9%)

### FM-009: Compression - Excessive punch tip wear
- **Current RPN**: 150 (S=5, O=5, D=6)
- **Recommendation**: Shift punch maintenance from calendar-based to cycle-count-based preventive replacement (replace at 80% of validated wear life).
- **Estimated post-improvement RPN**: 75 (S=5, O=3, D=5)
- **Estimated RPN reduction**: -75 points (-50.0%)

### FM-011: Coating - Over-coating (weight gain above target)
- **Current RPN**: 144 (S=8, O=3, D=6)
- **Recommendation**: Switch from time-based to weight-gain-based automated spray endpoint (in-process tablet sampling every 15 min).
- **Estimated post-improvement RPN**: 64 (S=8, O=2, D=4)
- **Estimated RPN reduction**: -80 points (-55.6%)

### FM-010: QC/IPC - IPC sample not representative of batch
- **Current RPN**: 144 (S=8, O=3, D=6)
- **Recommendation**: Replace grab sampling with validated stratified composite sampling plan per batch.
- **Estimated post-improvement RPN**: 64 (S=8, O=2, D=4)
- **Estimated RPN reduction**: -80 points (-55.6%)

### FM-012: Compression - Compression force too low
- **Current RPN**: 140 (S=7, O=5, D=4)
- **Recommendation**: Add automated force-feedback rejection (reject-on-force-band) at the press, 100% tablet screening instead of periodic IPC.
- **Estimated post-improvement RPN**: 63 (S=7, O=3, D=3)
- **Estimated RPN reduction**: -77 points (-55.0%)

### FM-013: Compression - Press speed exceeds validated range
- **Current RPN**: 140 (S=7, O=4, D=5)
- **Recommendation**: Lock turret speed to validated range via software limit; remove operator override capability.
- **Estimated post-improvement RPN**: 56 (S=7, O=2, D=4)
- **Estimated RPN reduction**: -84 points (-60.0%)

### FM-014: Compression - Tablet weight out of range
- **Current RPN**: 135 (S=9, O=5, D=3)
- **Recommendation**: Install 100% checkweigher with automated reject at the press discharge (replacing periodic manual IPC weight checks).
- **Estimated post-improvement RPN**: 36 (S=9, O=4, D=1)
- **Estimated RPN reduction**: -99 points (-73.3%)

### FM-015: Packaging - Missing desiccant
- **Current RPN**: 126 (S=6, O=3, D=7)
- **Recommendation**: Add vision-based desiccant-presence check per bottle with automatic reject.
- **Estimated post-improvement RPN**: 48 (S=6, O=2, D=4)
- **Estimated RPN reduction**: -78 points (-61.9%)

### FM-016: Coating - Under-coating (weight gain below target)
- **Current RPN**: 126 (S=7, O=3, D=6)
- **Recommendation**: Add in-line spray-interruption detection with automatic cycle pause and operator alert.
- **Estimated post-improvement RPN**: 56 (S=7, O=2, D=4)
- **Estimated RPN reduction**: -70 points (-55.6%)

### FM-017: Blending - Blender speed deviation
- **Current RPN**: 126 (S=7, O=3, D=6)
- **Recommendation**: Add continuous VFD speed logging with automated deviation alarm at +/-5% of setpoint.
- **Estimated post-improvement RPN**: 56 (S=7, O=2, D=4)
- **Estimated RPN reduction**: -70 points (-55.6%)

### FM-018: Drying - Over-drying
- **Current RPN**: 120 (S=5, O=4, D=6)
- **Recommendation**: Add automated endpoint cutoff referencing validated LOD target band, +/-0.2%.
- **Estimated post-improvement RPN**: 60 (S=5, O=3, D=4)
- **Estimated RPN reduction**: -60 points (-50.0%)

### FM-019: Granulation - Water added too fast
- **Current RPN**: 120 (S=6, O=4, D=5)
- **Recommendation**: Add mass-flow controller with closed-loop rate control in place of open-loop pump setpoint.
- **Estimated post-improvement RPN**: 48 (S=6, O=2, D=4)
- **Estimated RPN reduction**: -72 points (-60.0%)

### FM-020: Dispensing - Lubricant (Mg stearate) over-weighed
- **Current RPN**: 120 (S=6, O=4, D=5)
- **Recommendation**: Tighten excipient weight control limits and add a documented secondary verification step for Dispensing.
- **Estimated post-improvement RPN**: 72 (S=6, O=3, D=4)
- **Estimated RPN reduction**: -48 points (-40.0%)

## 6. Summary of Estimated Impact
- Total RPN across the 20 Critical Control Points, current state: **3138**
- Total RPN across the same 20 CCPs, after implementing all recommendations: **1354**
- Aggregate estimated RPN reduction: **1784 points (56.9%)**
- Every one of the 20 flagged CCPs has a strictly positive estimated RPN reduction (verified by `tests/test_pipeline.py`).
