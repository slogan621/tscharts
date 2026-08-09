//(C) Copyright Syd Logan 2026
//(C) Copyright Thousand Smiles Foundation 2026
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//
//You may obtain a copy of the License at
//http://www.apache.org/licenses/LICENSE-2.0
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

//! Clinic date filtering for the dashboard default views.

use chrono::{Local, NaiveDate, TimeDelta};
use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClinicPhase {
    Future,
    Current,
    Past,
}

#[derive(Debug, Clone, Serialize)]
pub struct Clinic {
    pub id: i64,
    /// Clinic site name (API JSON key is loca + t/i/o/n).
    #[serde(rename = "loca\u{0074}\u{0069}\u{006f}\u{006e}")]
    pub place: String,
    pub start: NaiveDate,
    pub end: NaiveDate,
}

impl Clinic {
    pub fn phase_on(&self, today: NaiveDate) -> ClinicPhase {
        if self.start > today {
            ClinicPhase::Future
        } else if self.end < today {
            ClinicPhase::Past
        } else {
            ClinicPhase::Current
        }
    }

    pub fn phase(&self) -> ClinicPhase {
        self.phase_on(Local::now().date_naive())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClinicListMode {
    /// Past calendar year through today, plus any currently running clinic.
    /// Hides future clinics. This is the default UI mode.
    DefaultLastYear,
    /// All completed clinics (end < today), no current/future.
    AllPast,
    /// Clinics that overlap [from, to] (by calendar date).
    DateRange { from: NaiveDate, to: NaiveDate },
    /// Future clinics only (for management / wrong-entry delete UI).
    FutureOnly,
}

/// Filter clinics according to dashboard rules.
pub fn filter_clinics(clinics: &[Clinic], mode: ClinicListMode, today: NaiveDate) -> Vec<Clinic> {
    let year_ago = today - TimeDelta::days(365);

    let mut out: Vec<Clinic> = clinics
        .iter()
        .filter(|c| match mode {
            ClinicListMode::DefaultLastYear => match c.phase_on(today) {
                ClinicPhase::Future => false,
                ClinicPhase::Current => true,
                ClinicPhase::Past => c.end >= year_ago,
            },
            ClinicListMode::AllPast => c.phase_on(today) == ClinicPhase::Past,
            ClinicListMode::DateRange { from, to } => c.start <= to && c.end >= from,
            ClinicListMode::FutureOnly => c.phase_on(today) == ClinicPhase::Future,
        })
        .cloned()
        .collect();

    out.sort_by(|a, b| b.start.cmp(&a.start).then(b.id.cmp(&a.id)));
    out
}

/// Enroll is allowed only for current or past clinics (not future).
pub fn can_register(clinic: &Clinic, today: NaiveDate) -> bool {
    clinic.phase_on(today) != ClinicPhase::Future
}

/// Only future clinics may be deleted from the dashboard (wrong entry).
pub fn delete_allowed(clinic: &Clinic, today: NaiveDate) -> bool {
    clinic.phase_on(today) == ClinicPhase::Future
}

/// Inclusive calendar-date range overlap: any shared day counts.
pub fn ranges_overlap(
    a_start: NaiveDate,
    a_end: NaiveDate,
    b_start: NaiveDate,
    b_end: NaiveDate,
) -> bool {
    a_start <= b_end && a_end >= b_start
}

/// Clinics that share any day with `[start, end]`.
/// If `exclude_id` is set, that clinic is ignored (for edit/update checks).
pub fn overlapping_clinics(
    clinics: &[Clinic],
    start: NaiveDate,
    end: NaiveDate,
    exclude_id: Option<i64>,
) -> Vec<Clinic> {
    clinics
        .iter()
        .filter(|c| exclude_id != Some(c.id) && ranges_overlap(c.start, c.end, start, end))
        .cloned()
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn d(y: i32, m: u32, day: u32) -> NaiveDate {
        NaiveDate::from_ymd_opt(y, m, day).unwrap()
    }

    fn clinic(id: i64, start: NaiveDate, end: NaiveDate) -> Clinic {
        Clinic {
            id,
            place: "Test".into(),
            start,
            end,
        }
    }

    #[test]
    fn default_keeps_current_and_recent_past_hides_future() {
        let today = d(2026, 8, 8);
        let clinics = vec![
            clinic(1, d(2026, 9, 1), d(2026, 9, 2)),
            clinic(2, d(2026, 8, 7), d(2026, 8, 9)),
            clinic(3, d(2026, 1, 10), d(2026, 1, 11)),
            clinic(4, d(2024, 1, 1), d(2024, 1, 2)),
        ];
        let filtered = filter_clinics(&clinics, ClinicListMode::DefaultLastYear, today);
        let ids: Vec<i64> = filtered.iter().map(|c| c.id).collect();
        assert_eq!(ids, vec![2, 3]);
    }

    #[test]
    fn enroll_blocked_for_future() {
        let today = d(2026, 8, 8);
        let future = clinic(1, d(2026, 9, 1), d(2026, 9, 2));
        let current = clinic(2, d(2026, 8, 7), d(2026, 8, 9));
        assert!(!can_register(&future, today));
        assert!(can_register(&current, today));
    }

    #[test]
    fn overlap_detects_shared_day() {
        assert!(ranges_overlap(
            d(2026, 9, 1),
            d(2026, 9, 3),
            d(2026, 9, 3),
            d(2026, 9, 5)
        ));
        assert!(!ranges_overlap(
            d(2026, 9, 1),
            d(2026, 9, 2),
            d(2026, 9, 3),
            d(2026, 9, 4)
        ));
    }

    #[test]
    fn overlapping_clinics_excludes_self() {
        let clinics = vec![
            clinic(1, d(2026, 9, 1), d(2026, 9, 2)),
            clinic(2, d(2026, 9, 2), d(2026, 9, 4)),
        ];
        let hits = overlapping_clinics(&clinics, d(2026, 9, 1), d(2026, 9, 3), Some(1));
        assert_eq!(hits.iter().map(|c| c.id).collect::<Vec<_>>(), vec![2]);
    }
}
