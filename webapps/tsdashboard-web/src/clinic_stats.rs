//! Aggregate clinic registration statistics for the dashboard.

use chrono::{Datelike, NaiveDate, NaiveDateTime, Timelike};
use serde::Serialize;

use crate::client::{Patient, Registration};
use crate::clinic_filter::Clinic;

#[derive(Debug, Clone, Serialize)]
pub struct HourBucket {
    pub hour: u32,
    pub count: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum Busyness {
    Busy,
    Moderate,
    Slow,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum StartTiming {
    Earlier,
    Average,
    Later,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum RatePace {
    Faster,
    Normal,
    Slower,
}

/// One-word overall registration-day grade from volume / start / rate.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum OverallGrade {
    Great,
    Good,
    Average,
    BelowAverage,
    Poor,
}

impl OverallGrade {
    pub fn label(self) -> &'static str {
        match self {
            OverallGrade::Great => "Great",
            OverallGrade::Good => "Good",
            OverallGrade::Average => "Average",
            OverallGrade::BelowAverage => "Below Average",
            OverallGrade::Poor => "Poor",
        }
    }

    pub fn smiley(self) -> &'static str {
        match self {
            OverallGrade::Great => "😄",
            OverallGrade::Good => "🙂",
            OverallGrade::Average => "😐",
            OverallGrade::BelowAverage => "😕",
            OverallGrade::Poor => "😞",
        }
    }

    pub fn css_class(self) -> &'static str {
        match self {
            OverallGrade::Great => "grade-great",
            OverallGrade::Good => "grade-good",
            OverallGrade::Average => "grade-average",
            OverallGrade::BelowAverage => "grade-below",
            OverallGrade::Poor => "grade-poor",
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct ArrivalProfile {
    pub clinic_id: i64,
    pub registered: usize,
    pub arrivals: usize,
    /// Minutes since midnight of the earliest check-in.
    pub first_arrival_minutes: Option<u32>,
    pub peak_hour_count: usize,
    /// Check-ins per hour over the first→last arrival window.
    pub rate_per_hour: Option<f64>,
}

#[derive(Debug, Clone, Serialize)]
pub struct PerformanceRanking {
    pub peers_all: usize,
    pub peers_similar: usize,
    pub busyness: Option<Busyness>,
    pub start_timing: Option<StartTiming>,
    pub rate_pace: Option<RatePace>,
    pub overall: Option<OverallGrade>,
    pub this_peak: usize,
    pub median_peak: Option<f64>,
    pub this_first_label: Option<String>,
    pub median_first_label: Option<String>,
    pub this_rate: Option<f64>,
    pub median_similar_rate: Option<f64>,
    pub similar_size_lo: usize,
    pub similar_size_hi: usize,
}

#[derive(Debug, Clone, Serialize)]
pub struct ClinicStats {
    pub registered: usize,
    pub with_dob: usize,
    pub age_min: Option<u32>,
    pub age_max: Option<u32>,
    pub age_avg: Option<f64>,
    pub boys: usize,
    pub girls: usize,
    pub gender_unknown: usize,
    pub new_patients: usize,
    pub return_patients: usize,
    pub arrival_by_hour: Vec<HourBucket>,
    pub arrivals_parsed: usize,
}

pub fn compute_stats(
    clinic: &Clinic,
    regs: &[Registration],
    patients: &[(i64, Patient)],
    // Patient IDs that already registered at an earlier clinic.
    prior_patient_ids: &std::collections::HashSet<i64>,
) -> ClinicStats {
    let registered = regs.len();
    let mut boys = 0usize;
    let mut girls = 0usize;
    let mut gender_unknown = 0usize;
    let mut ages: Vec<u32> = Vec::new();

    let patient_map: std::collections::HashMap<i64, &Patient> =
        patients.iter().map(|(id, p)| (*id, p)).collect();

    // Demographics are per unique patient (multi-day re-check-ins must not double-count).
    let mut seen_demo = std::collections::HashSet::new();
    for r in regs {
        if !seen_demo.insert(r.patient) {
            continue;
        }
        match patient_map.get(&r.patient) {
            Some(p) => {
                match gender_bucket(&p.gender) {
                    GenderBucket::Male => boys += 1,
                    GenderBucket::Female => girls += 1,
                    GenderBucket::Unknown => gender_unknown += 1,
                }
                if let Some(dob) = parse_dob(&p.dob) {
                    if let Some(age) = age_years(dob, clinic.start) {
                        ages.push(age);
                    }
                }
            }
            None => gender_unknown += 1,
        }
    }

    let mut seen = std::collections::HashSet::new();
    let mut new_patients = 0usize;
    let mut return_patients = 0usize;
    for r in regs {
        if !seen.insert(r.patient) {
            continue;
        }
        if prior_patient_ids.contains(&r.patient) {
            return_patients += 1;
        } else {
            new_patients += 1;
        }
    }

    let mut hour_counts = [0usize; 24];
    let mut arrivals_parsed = 0usize;
    for r in regs {
        if let Some(ref t) = r.timein {
            if let Some(dt) = parse_timein(t) {
                hour_counts[dt.hour() as usize] += 1;
                arrivals_parsed += 1;
            }
        }
    }

    let arrival_by_hour: Vec<HourBucket> = (0u32..24)
        .filter(|&h| hour_counts[h as usize] > 0)
        .map(|h| HourBucket {
            hour: h,
            count: hour_counts[h as usize],
        })
        .collect();

    let age_min = ages.iter().copied().min();
    let age_max = ages.iter().copied().max();
    let age_avg = if ages.is_empty() {
        None
    } else {
        Some(ages.iter().map(|&a| a as f64).sum::<f64>() / ages.len() as f64)
    };

    ClinicStats {
        registered,
        with_dob: ages.len(),
        age_min,
        age_max,
        age_avg,
        boys,
        girls,
        gender_unknown,
        new_patients,
        return_patients,
        arrival_by_hour,
        arrivals_parsed,
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum GenderBucket {
    Male,
    Female,
    Unknown,
}

pub fn gender_bucket(g: &str) -> GenderBucket {
    match g.trim().to_ascii_lowercase().as_str() {
        "male" | "m" | "boy" | "hombre" => GenderBucket::Male,
        "female" | "f" | "girl" | "mujer" => GenderBucket::Female,
        _ => GenderBucket::Unknown,
    }
}

pub fn parse_dob(s: &str) -> Option<NaiveDate> {
    let s = s.trim();
    NaiveDate::parse_from_str(s, "%m/%d/%Y")
        .or_else(|_| NaiveDate::parse_from_str(s, "%m-%d-%Y"))
        .or_else(|_| NaiveDate::parse_from_str(s, "%Y-%m-%d"))
        .ok()
}

pub fn age_years(dob: NaiveDate, on: NaiveDate) -> Option<u32> {
    if dob > on {
        return None;
    }
    let mut years = on.year() - dob.year();
    if (on.month(), on.day()) < (dob.month(), dob.day()) {
        years -= 1;
    }
    if years < 0 {
        None
    } else {
        Some(years as u32)
    }
}

pub fn parse_timein(s: &str) -> Option<NaiveDateTime> {
    let s = s.trim();
    if let Ok(dt) = chrono::DateTime::parse_from_rfc3339(s) {
        return Some(dt.naive_local());
    }
    // Django sometimes omits timezone / uses fractional seconds.
    NaiveDateTime::parse_from_str(s, "%Y-%m-%dT%H:%M:%S%.f")
        .or_else(|_| NaiveDateTime::parse_from_str(s, "%Y-%m-%dT%H:%M:%S"))
        .or_else(|_| NaiveDateTime::parse_from_str(s, "%Y-%m-%d %H:%M:%S%.f"))
        .or_else(|_| NaiveDateTime::parse_from_str(s, "%Y-%m-%d %H:%M:%S"))
        .ok()
}

pub fn minutes_since_midnight(dt: NaiveDateTime) -> u32 {
    dt.hour() * 60 + dt.minute()
}

pub fn format_minutes_clock(mins: u32) -> String {
    let h = mins / 60;
    let m = mins % 60;
    format!("{h:02}:{m:02}")
}

/// Registrations whose check-in date falls on a clinic calendar day.
///
/// Dashboard (and other) enrollments made between clinics often land after
/// `clinic.end`; those must not count toward day tabs or performance ranking.
pub fn regs_in_clinic_window(clinic: &Clinic, regs: &[Registration]) -> Vec<Registration> {
    regs.iter()
        .filter(|r| {
            r.timein
                .as_deref()
                .and_then(parse_timein)
                .map(|dt| {
                    let d = dt.date();
                    d >= clinic.start && d <= clinic.end
                })
                .unwrap_or(false)
        })
        .cloned()
        .collect()
}

/// Group registrations by check-in calendar day (days with no check-ins are omitted).
pub fn group_regs_by_day(regs: &[Registration]) -> std::collections::BTreeMap<NaiveDate, Vec<Registration>> {
    let mut map: std::collections::BTreeMap<NaiveDate, Vec<Registration>> =
        std::collections::BTreeMap::new();
    for r in regs {
        if let Some(dt) = r.timein.as_deref().and_then(parse_timein) {
            map.entry(dt.date()).or_default().push(r.clone());
        }
    }
    map
}

/// Build an arrival/throughput profile from registration check-in times.
pub fn arrival_profile(clinic_id: i64, regs: &[Registration]) -> ArrivalProfile {
    let mut times: Vec<NaiveDateTime> = regs
        .iter()
        .filter_map(|r| r.timein.as_deref().and_then(parse_timein))
        .collect();
    times.sort();

    let mut hour_counts = [0usize; 24];
    for t in &times {
        hour_counts[t.hour() as usize] += 1;
    }
    let peak_hour_count = *hour_counts.iter().max().unwrap_or(&0);

    let first_arrival_minutes = times.first().map(|t| minutes_since_midnight(*t));
    let rate_per_hour = match (times.first(), times.last()) {
        (Some(first), Some(last)) => {
            let span_secs = (*last - *first).num_seconds().max(0) as f64;
            let span_hours = (span_secs / 3600.0).max(1.0 / 60.0); // at least 1 minute
            Some(times.len() as f64 / span_hours)
        }
        _ => None,
    };

    ArrivalProfile {
        clinic_id,
        registered: regs.len(),
        arrivals: times.len(),
        first_arrival_minutes,
        peak_hour_count,
        rate_per_hour,
    }
}

fn percentile_nearest(sorted: &[f64], p: f64) -> Option<f64> {
    if sorted.is_empty() {
        return None;
    }
    let p = p.clamp(0.0, 1.0);
    let idx = ((sorted.len() as f64 - 1.0) * p).round() as usize;
    Some(sorted[idx.min(sorted.len() - 1)])
}

fn median(sorted: &[f64]) -> Option<f64> {
    percentile_nearest(sorted, 0.5)
}

/// Tercile vs peers: returns -1 (low), 0 (mid), 1 (high) for `value`.
/// If `higher_means_high_label` is false, the scale is inverted (lower value → high label).
fn tercile_rank(value: f64, peers: &[f64], higher_means_high_label: bool) -> Option<i8> {
    if peers.len() < 3 {
        return None;
    }
    let mut sorted = peers.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let p33 = percentile_nearest(&sorted, 1.0 / 3.0)?;
    let p67 = percentile_nearest(&sorted, 2.0 / 3.0)?;
    let raw = if value <= p33 {
        -1
    } else if value >= p67 {
        1
    } else {
        0
    };
    Some(if higher_means_high_label { raw } else { -raw })
}

fn size_window(size: usize) -> (usize, usize) {
    let pad = ((size as f64) * 0.25).ceil() as usize;
    let pad = pad.max(5);
    (size.saturating_sub(pad), size + pad)
}

/// Clinics of similar size: within ±25% of `size` (at least ±5).
pub fn similarly_sized<'a>(
    profiles: &'a [ArrivalProfile],
    size: usize,
) -> Vec<&'a ArrivalProfile> {
    let (lo, hi) = size_window(size);
    profiles
        .iter()
        .filter(|p| p.registered >= lo && p.registered <= hi && p.arrivals >= 3)
        .collect()
}

fn sort_f64(values: &mut [f64]) {
    values.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
}

/// Rank this clinic's registration histogram performance against peers.
pub fn rank_performance(
    this: &ArrivalProfile,
    all_profiles: &[ArrivalProfile],
) -> PerformanceRanking {
    let peers: Vec<&ArrivalProfile> = all_profiles
        .iter()
        .filter(|p| p.arrivals >= 3)
        .collect();

    let peaks: Vec<f64> = peers.iter().map(|p| p.peak_hour_count as f64).collect();
    let firsts: Vec<f64> = peers
        .iter()
        .filter_map(|p| p.first_arrival_minutes.map(|m| m as f64))
        .collect();

    let (lo, hi) = size_window(this.registered);
    let peer_owned: Vec<ArrivalProfile> = peers.iter().map(|p| (*p).clone()).collect();
    let similar_refs = similarly_sized(&peer_owned, this.registered);
    let similar_rates: Vec<f64> = similar_refs
        .iter()
        .filter_map(|p| p.rate_per_hour)
        .collect();

    let busyness = tercile_rank(this.peak_hour_count as f64, &peaks, true).map(|r| match r {
        1 => Busyness::Busy,
        -1 => Busyness::Slow,
        _ => Busyness::Moderate,
    });

    // Lower first-arrival minutes ⇒ earlier. Invert so high label = Earlier.
    let start_timing = this
        .first_arrival_minutes
        .and_then(|m| tercile_rank(m as f64, &firsts, false))
        .map(|r| match r {
            1 => StartTiming::Earlier,
            -1 => StartTiming::Later,
            _ => StartTiming::Average,
        });

    let rate_pace = this
        .rate_per_hour
        .and_then(|r| tercile_rank(r, &similar_rates, true))
        .map(|r| match r {
            1 => RatePace::Faster,
            -1 => RatePace::Slower,
            _ => RatePace::Normal,
        });

    let mut peaks_sorted = peaks;
    sort_f64(&mut peaks_sorted);
    let mut firsts_sorted = firsts;
    sort_f64(&mut firsts_sorted);
    let mut rates_sorted = similar_rates;
    sort_f64(&mut rates_sorted);

    let overall = overall_grade(busyness, start_timing, rate_pace);

    PerformanceRanking {
        peers_all: peers.len(),
        peers_similar: similar_refs.len(),
        busyness,
        start_timing,
        rate_pace,
        overall,
        this_peak: this.peak_hour_count,
        median_peak: median(&peaks_sorted),
        this_first_label: this.first_arrival_minutes.map(format_minutes_clock),
        median_first_label: median(&firsts_sorted).map(|m| format_minutes_clock(m.round() as u32)),
        this_rate: this.rate_per_hour,
        median_similar_rate: median(&rates_sorted),
        similar_size_lo: lo,
        similar_size_hi: hi,
    }
}

/// Combine volume / start / rate into a single grade.
/// Each available signal scores 0 (weak), 1 (typical), or 2 (strong); average maps to the label.
pub fn overall_grade(
    busyness: Option<Busyness>,
    start_timing: Option<StartTiming>,
    rate_pace: Option<RatePace>,
) -> Option<OverallGrade> {
    let mut scores: Vec<u8> = Vec::new();
    if let Some(b) = busyness {
        scores.push(match b {
            Busyness::Busy => 2,
            Busyness::Moderate => 1,
            Busyness::Slow => 0,
        });
    }
    if let Some(s) = start_timing {
        scores.push(match s {
            StartTiming::Earlier => 2,
            StartTiming::Average => 1,
            StartTiming::Later => 0,
        });
    }
    if let Some(r) = rate_pace {
        scores.push(match r {
            RatePace::Faster => 2,
            RatePace::Normal => 1,
            RatePace::Slower => 0,
        });
    }
    if scores.is_empty() {
        return None;
    }
    let avg = scores.iter().map(|&s| s as f64).sum::<f64>() / scores.len() as f64;
    Some(if avg >= 1.75 {
        OverallGrade::Great
    } else if avg >= 1.35 {
        OverallGrade::Good
    } else if avg >= 0.9 {
        OverallGrade::Average
    } else if avg >= 0.4 {
        OverallGrade::BelowAverage
    } else {
        OverallGrade::Poor
    })
}

/// True if the patient has any registration at a clinic that started before `clinic`.
pub fn is_return_patient(
    patient_regs: &[Registration],
    clinic: &Clinic,
    clinic_start_by_id: &std::collections::HashMap<i64, NaiveDate>,
) -> bool {
    patient_regs.iter().any(|r| {
        if r.clinic == clinic.id {
            return false;
        }
        clinic_start_by_id
            .get(&r.clinic)
            .map(|start| *start < clinic.start)
            .unwrap_or(false)
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::client::Patient;

    fn d(y: i32, m: u32, day: u32) -> NaiveDate {
        NaiveDate::from_ymd_opt(y, m, day).unwrap()
    }

    #[test]
    fn filters_regs_outside_clinic_window() {
        let clinic = Clinic {
            id: 1,
            place: "Ensenada".into(),
            start: d(2025, 8, 28),
            end: d(2025, 8, 31),
        };
        let regs = vec![
            Registration {
                id: 1,
                patient: 10,
                clinic: 1,
                state: None,
                timein: Some("2025-08-29T09:00:00".into()),
                timeout: None,
            },
            Registration {
                id: 2,
                patient: 11,
                clinic: 1,
                state: None,
                timein: Some("2025-11-07T09:50:00".into()),
                timeout: None,
            },
        ];
        let in_window = regs_in_clinic_window(&clinic, &regs);
        assert_eq!(in_window.len(), 1);
        assert_eq!(in_window[0].id, 1);
        let days = group_regs_by_day(&in_window);
        assert_eq!(days.len(), 1);
        assert!(days.contains_key(&d(2025, 8, 29)));
    }

    #[test]
    fn age_and_gender_stats() {
        let clinic = Clinic {
            id: 1,
            place: "Ensenada".into(),
            start: d(2026, 8, 8),
            end: d(2026, 8, 9),
        };
        let regs = vec![
            Registration {
                id: 1,
                patient: 10,
                clinic: 1,
                state: None,
                timein: Some("2026-08-08T09:15:00Z".into()),
                timeout: None,
            },
            Registration {
                id: 2,
                patient: 11,
                clinic: 1,
                state: None,
                timein: Some("2026-08-08T09:45:00Z".into()),
                timeout: None,
            },
            Registration {
                id: 3,
                patient: 12,
                clinic: 1,
                state: None,
                timein: Some("2026-08-08T14:00:00Z".into()),
                timeout: None,
            },
        ];
        let patients = vec![
            (
                10,
                Patient {
                    dob: "08/08/2016".into(),
                    gender: "Male".into(),
                    ..Patient::default()
                },
            ),
            (
                11,
                Patient {
                    dob: "01/01/2020".into(),
                    gender: "Female".into(),
                    ..Patient::default()
                },
            ),
            (
                12,
                Patient {
                    dob: "08/08/2010".into(),
                    gender: "m".into(),
                    ..Patient::default()
                },
            ),
        ];
        let mut prior = std::collections::HashSet::new();
        prior.insert(11);
        let s = compute_stats(&clinic, &regs, &patients, &prior);
        assert_eq!(s.registered, 3);
        assert_eq!(s.boys, 2);
        assert_eq!(s.girls, 1);
        // Duplicate check-in for patient 10 must not inflate boy count.
        let mut regs2 = regs.clone();
        regs2.push(Registration {
            id: 99,
            patient: 10,
            clinic: 1,
            state: Some("i".into()),
            timein: Some("2026-08-09T09:00:00Z".into()),
            timeout: None,
        });
        let s2 = compute_stats(&clinic, &regs2, &patients, &prior);
        assert_eq!(s2.registered, 4);
        assert_eq!(s2.boys, 2);
        assert_eq!(s2.girls, 1);
        assert_eq!(s.age_min, Some(6));
        assert_eq!(s.age_max, Some(16));
        assert_eq!(s.new_patients, 2);
        assert_eq!(s.return_patients, 1);
        assert_eq!(s.arrival_by_hour.len(), 2);
        assert_eq!(s.arrival_by_hour[0].hour, 9);
        assert_eq!(s.arrival_by_hour[0].count, 2);
        assert_eq!(s.arrival_by_hour[1].hour, 14);
        assert_eq!(s.arrival_by_hour[1].count, 1);
    }

    #[test]
    fn parse_timein_variants() {
        assert!(parse_timein("2017-04-21T05:52:54Z").is_some());
        assert!(parse_timein("2021-08-06T10:18:20.594").is_some());
    }

    fn profile(id: i64, times: &[&str]) -> ArrivalProfile {
        let regs: Vec<Registration> = times
            .iter()
            .enumerate()
            .map(|(i, t)| Registration {
                id: i as i64 + 1,
                patient: i as i64 + 1,
                clinic: id,
                state: None,
                timein: Some((*t).into()),
                timeout: None,
            })
            .collect();
        arrival_profile(id, &regs)
    }

    #[test]
    fn ranks_busy_early_fast() {
        // Peers with low peaks / later starts / slower rates.
        let peers = vec![
            profile(1, &["2026-01-01T09:00:00Z", "2026-01-01T10:00:00Z", "2026-01-01T11:00:00Z"]),
            profile(2, &["2026-01-01T09:30:00Z", "2026-01-01T10:30:00Z", "2026-01-01T11:30:00Z"]),
            profile(3, &["2026-01-01T08:45:00Z", "2026-01-01T09:45:00Z", "2026-01-01T10:45:00Z"]),
            // This clinic: early start, bursty peak, fast rate
            profile(
                99,
                &[
                    "2026-01-01T07:00:00Z",
                    "2026-01-01T07:05:00Z",
                    "2026-01-01T07:10:00Z",
                    "2026-01-01T07:15:00Z",
                    "2026-01-01T07:20:00Z",
                    "2026-01-01T07:25:00Z",
                ],
            ),
        ];
        let this = peers.iter().find(|p| p.clinic_id == 99).unwrap().clone();
        let rank = rank_performance(&this, &peers);
        assert_eq!(rank.busyness, Some(Busyness::Busy));
        assert_eq!(rank.start_timing, Some(StartTiming::Earlier));
        assert_eq!(rank.rate_pace, Some(RatePace::Faster));
        assert_eq!(rank.overall, Some(OverallGrade::Great));
    }

    #[test]
    fn overall_grade_mapping() {
        assert_eq!(
            overall_grade(
                Some(Busyness::Busy),
                Some(StartTiming::Earlier),
                Some(RatePace::Faster)
            ),
            Some(OverallGrade::Great)
        );
        assert_eq!(
            overall_grade(
                Some(Busyness::Moderate),
                Some(StartTiming::Average),
                Some(RatePace::Normal)
            ),
            Some(OverallGrade::Average)
        );
        assert_eq!(
            overall_grade(
                Some(Busyness::Slow),
                Some(StartTiming::Later),
                Some(RatePace::Slower)
            ),
            Some(OverallGrade::Poor)
        );
    }
}
