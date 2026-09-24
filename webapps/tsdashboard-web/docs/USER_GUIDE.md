# Thousand Smiles Clinic Ops — User Guide

Clinic Ops is a web dashboard for planning clinics, maintaining patient records
between events, and reviewing or correcting data after volunteers register
patients on Android tablets.

It talks to the same **tscharts** backend used by the tablet registration app
([tscharts-register](https://github.com/slogan621/tscharts-register)). Demographics
and clinic enrollments you change here are what the tablets (and the rest of the
EMR) see.

---

## Who this is for

| Role | Typical use |
|------|-------------|
| Clinic coordinators | Create upcoming clinics; clean up data after an event |
| Registration leads | Fix wrong names/DOB/CURP; add headshots; resolve duplicates |
| On-site supervisors | Watch daily check-in volume and timing on Stats |
| Between-clinic staff | Create patients ahead of time; register late arrivals after the fact |

Tablet volunteers still do day-of check-in with
[tscharts-register](https://github.com/slogan621/tscharts-register). This site
complements that workflow; it does not replace the tablet UI for high-volume
registration lines.

---

## Sign in

1. Open the Clinic Ops URL provided by your administrator.
2. Sign in with your **tscharts** username and password (same account as other
   Thousand Smiles chart tools).
3. Use **Logout** in the top navigation when finished, especially on shared
   computers.

If login fails, confirm the API server is reachable and that your account is
active. You do not create a separate password for Clinic Ops.

---

## Navigation

Top bar:

- **Clinics** — list and open clinics  
- **New patient** — create a patient record (does not enroll them)  
- **Imaging** — X-ray module (stub; use for navigation only until enabled)  
- **Logout**

---

## Clinics list

**Clinics** shows a filtered list of events.

### Views

| Button | Shows |
|--------|--------|
| **Last year + current** | Default. Clinics from the past calendar year, plus any clinic running today. Hides future clinics. |
| **All past** | Completed clinics only |
| **Future** | Clinics that have not started yet |
| **Apply range** | Clinics overlapping the From/To dates you enter |

Each row shows place, start/end, patient (enrollment) count, and status
(`current`, `past`, or `future`).

Actions:

- **Stats** — performance and demographics for that clinic  
- **Edit** / **Delete** — only for **future** clinics (correct a mistaken entry
  before the event)

### Create a future clinic

1. Open **Future** (or stay on the list) and click **Create future clinic**.  
2. Enter **Place**, **Start**, and **End**. Start must be **after today**.  
3. **Create**.

Overlap rules:

- Overlapping a clinic that is **currently running** is blocked.  
- Overlapping another **future** clinic shows a confirmation so you can adjust
  names/dates instead of creating a duplicate window.  
- Past clinics are not edited from this screen.

Use clinic dates that cover setup through teardown if you need them on the
calendar, but remember: **performance stats only count check-ins on those
calendar days**. Prefer dates that match when registration actually happens
when you care about Stats accuracy.

---

## Clinic detail (registered patients)

Open a clinic from the list. The header shows:

- **Location** and **Dates** (clinic window as stored)  
- **Unique patients**, **Boys / girls**, **Check-ins** — based on enrollments
  whose check-in date falls **inside** the clinic start–end window  

Toolbar:

- **Register patient** — enroll an existing patient by ID (current/past clinics
  only; disabled for future clinics)  
- **Stats**  
- **New patient** / **Find patient**  
- **Back to clinics**

### Day tabs

When a clinic has check-ins on more than one day, patients are grouped under
tabs labeled by date (for example `02/06/2026`). Days with **no** check-ins
(typical setup/teardown days) do not appear.

Each day shows that day’s check-ins, check-in time, and actions:

- **Edit** — demographics and headshot  
- **X-rays** — imaging stub for that patient  
- **Unregister** — remove that enrollment row  

The same patient can appear on multiple days if they checked in more than once
(the tablet/API allow one registration per calendar day per clinic). Summary
counts use **unique patients**, so multi-day re-check-ins are not double-counted
for boys/girls.

### Outside clinic dates and All

If someone was enrolled when the check-in timestamp fell **before start or after
end** (common when staff use Clinic Ops on a **past** clinic between events),
those rows appear in an **Outside clinic dates** tab to the right of the
clinic-day tabs (only shown when such enrollments exist).

When there is more than one day tab, or an outside tab, an **All** tab lists
every enrollment for the clinic (clinic-day and outside). Outside rows are
marked in that list.

- Outside enrollments remain visible so you can edit or unregister them.  
- Header summary counts and **Stats** use **clinic-day check-ins only** — outside
  enrollments do not affect rankings or boys/girls/unique totals.

---

## Working with the tablet app

Volunteers register patients on Android tablets running
[tscharts-register](https://github.com/slogan621/tscharts-register). That app
creates or updates patients and creates clinic enrollments against tscharts in
real time.

Clinic Ops is the place to:

1. **Prepare** before volunteers arrive (future clinic, clean patient list).  
2. **Monitor** during/after the event (Stats, day lists).  
3. **Correct** mistakes that are hard to fix on a busy tablet line.

Both tools share one database. A patient created here is available on the
tablet; a registration made on the tablet appears here after refresh.

### Suggested clinic-day loop

1. Confirm the correct **current** clinic is open on Clinics.  
2. Let tablets handle the registration line.  
3. On Clinic Ops, open the clinic → day tab for today to spot gaps (missing
   headshot, wrong gender, bad CURP).  
4. Use **Edit** on a row to fix demographics or upload a headshot without
   interrupting the tablet queue.  
5. After the day (or clinic), open **Stats** for that day to review volume,
   start time, and rate versus other clinic days.

### After the clinic

Useful cleanup:

- Fix spelling, DOB, gender, CURP on **Edit patient**.  
- Upload or replace headshots.  
- **Unregister** accidental double enrollments for the same day if needed.  
- Leave legitimate multi-day check-ins alone (one row per day is expected).  
- Review **Outside clinic dates** and either unregister test/late admin
  enrollments or leave them with the understanding they do not affect Stats.

---

## Maintaining data between clinics

Between events, Clinic Ops is often more convenient than tablets.

### Plan the next clinic

1. **Future** → **Create future clinic** with place and dates.  
2. Double-check for overlap with other future clinics.  
3. Do **not** expect to register patients against a future clinic from this UI
   (enroll is blocked until the clinic is current or past). Create patients now;
   enroll them when the clinic is active, or let tablets enroll on clinic days.

### Create and clean patient records

1. **New patient** — enter demographics. The form checks for duplicates as you
   type (same idea as the tablet: name + DOB + gender, CURP, similar names).  
2. If a match appears, prefer **Open existing** instead of creating a duplicate.  
3. After create, use **Edit / add headshot** if you have a photo.  
4. **Find patient** — search by name or CURP when you are unsure of the ID.

Remember: **creating a patient is not the same as registering them for a
clinic**. Registration is always a separate step on the clinic page (or on the
tablet).

### Enroll after the fact

For a **past** or **current** clinic you may **Register patient** by patient ID
(for example someone missed the line but should appear on the clinic roster).

Be aware:

- Check-in time is recorded as **now**.  
- If “now” is outside the clinic’s start–end dates, the enrollment appears in the
  **Outside clinic dates** tab (and in **All**) and is excluded from Stats.  
- Prefer registering on a real clinic day when performance metrics matter; use
  between-clinic enrollments for roster correctness, not for inflating daily
  rankings.

### Avoid duplicate patients

Before creating:

1. Search (**Find patient**) by paternal last name and/or CURP.  
2. Use **New patient** and watch the live match panel.  
3. If create is blocked for an exact match, open the existing record and update
   it instead.

Duplicates make tablet search harder and split a child’s history across IDs.

---

## Statistics

Open **Stats** from the clinic list or clinic detail.

- One **tab per registration day** inside the clinic window (days with no
  check-ins omitted).  
- Each day has its own **Performance ranking** and demographic cards.  
- Rankings compare that day to other **clinic days** (not whole multi-day
  clinics), using check-in timestamps.  
- Grades blend volume (busy peak hour), how early registration started, and
  check-ins per hour versus similarly sized days.  
- **Boys / girls**, ages, and new vs return use **unique patients** for that
  day.  
- Enrollments outside the clinic calendar show a warning and are excluded.

Use Stats to:

- See whether a morning started late compared with peers.  
- Spot an unusually slow or busy day.  
- Compare boys/girls and new vs returning patients after the fact.  
- Decide process changes for the next clinic (more tablet stations, earlier
  open, etc.).

---

## Headshots

- Thumbnails appear on clinic lists, search results, and duplicate panels.  
- On **Edit patient**, use **Upload or replace photo** → **Save headshot**.  
- A new upload replaces previous headshot images for that patient.  
- Photos live on the tscharts server image store; if headshots are missing after
  a migration, ask an administrator to restore `/opt/thousandsmiles/images` (see
  the Docker stack README). Clinic Ops cannot invent photos that were never
  copied to the server.

---

## Imaging (X-rays)

The **Imaging** area and per-patient **X-rays** links are placeholders for a
future module. They do not yet list or upload X-rays. Continue using existing
imaging tools until this section is enabled.

---

## Quick reference

| Task | Where |
|------|--------|
| Sign in | `/login` |
| See recent / current clinics | **Clinics** → **Last year + current** |
| Schedule next event | **Create future clinic** |
| Fix a volunteer’s typo | Clinic → day tab → **Edit** |
| Add a photo after the line | **Edit patient** → Headshot |
| Enroll someone missed on tablets | Clinic → **Register patient** (current/past) |
| Remove a bad enrollment | Row → **Unregister** |
| Find someone by CURP | **Find patient** |
| Review day performance | Clinic → **Stats** → day tab |
| See admin enrollments after clinic | Clinic → **Outside clinic dates** tab |

---

## Privacy and good practice

- Patient data is confidential. Sign out on shared machines.  
- Prefer correcting the existing patient over creating a second record.  
- Do not commit exports, dumps, or photos to email threads or public repos.  
- Between-clinic enrollments are fine for roster accuracy; do not treat them as
  measures of registration-line performance.

---

## Related software

| System | Role |
|--------|------|
| [tscharts](https://github.com/slogan621/tscharts) | Backend API and database |
| [tscharts-register](https://github.com/slogan621/tscharts-register) | Android tablet registration at the clinic |
| Clinic Ops (`tsdashboard-web`) | This website — planning, cleanup, monitoring |

For deployment and API configuration, see the app [README](../README.md) and
[docker/README.md](../docker/README.md).
