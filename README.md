# 🛡️ TrustJuggle AI — Advanced Rider Identity Verification & Anti-Account-Sharing Platform

> **Tagline:** One Account. One Verified Rider. Smarter Trust.  
> **Problem Statement:** The Rented Account Problem in Gig Delivery Platforms (NMIMS Hackathon — Advanced Upgrade)

---

## 1. Problem Statement & Executive Summary

In rapid on-demand food and grocery delivery ecosystems (e.g. Swiggy, Zomato, Blinkit, Zepto), rider identity is verified primarily during initial driver onboarding. Following approval, delivery accounts are frequently rented out, subcontracted, or shared across multiple individuals or unregistered devices without platform authorization. 

This unauthorized account sharing leads to:
- **Severe customer safety vulnerabilities** from unvetted individuals entering residential premises.
- **Regulatory, labor, and legal non-compliance** regarding worker background verification and vehicle roadworthiness.
- **Insurance invalidation** if an unlisted driver causes an accident while logged into another worker's profile.
- **Brand and consumer trust erosion**.

### Platform Objectives
**TrustJuggle AI** provides an enterprise-grade identity-verification and behavioral anti-account-sharing platform that:
1. **Onboards riders via a multi-step verification wizard** (live camera capture with face positioning oval, HTML5 digital signature pad, consent-based geolocation, UIDAI/DigiLocker compliant masked Aadhaar KYC, and contact OTP verification).
2. **Protects biometric and signature artifacts** in a private, encrypted filesystem (`instance/private_artifacts/`) accessible only via role-based access control (RBAC).
3. **Monitors multi-device concurrency and fleet sessions** via an **Administrator Device & Session Intelligence** module (`/admin/device-intelligence`) featuring individual deep-dive inspection (`/admin/rider/<id>/devices`) and server-side session revocation.
4. **Enforces intelligent concurrent session limits** (`MAX_CONCURRENT_SESSIONS = 2`) with server-side request invalidation via `@app.before_request`.
5. **Passively ingests delivery telemetry** (device references, coarse municipal zones, and shift timelines) and computes an explainable behavioral risk score (0 to 100).
6. **Maintains algorithmic fairness and compliance:** UIDAI compliance strictly forbids storing raw Aadhaar numbers or OTPs; demo mode is prominently labeled.

---

## 2. System Architecture

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TrustJuggle AI Core Platform                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
          ┌─────────────────────────────────┼────────────────────────────────┐
          ▼                                 ▼                                ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────────────┐
│   Rider Onboarding Wizard     │ │  Device & Session Intel Engine│ │  Risk & Step-Up Verification  │
│  - Step 1: Personal Details   │ │  - Device binding & tokens    │ │  - BehaviorAnalyzer (72h Churn│
│  - Step 2: Camera Live Photo  │ │  - Concurrent session limit   │ │  - Velocity & Shift checks    │
│  - Step 3: Digital Signature  │ │  - Server-side revocation hook│ │  - Explainable score (0-100)  │
│  - Step 4: Masked Aadhaar KYC │ │  - Multi-device fleet metrics │ │  - Cryptographic 6-digit OTP  │
│  - Step 5: Geolocation Signal │ │  - Individual deep-dive view  │ │  - Neutral review workflow    │
│  - Step 6: Contact OTP        │ └───────────────────────────────┘ └───────────────────────────────┘
│  - Step 7: Final Review       │                   │                                │
└───────────────────────────────┘                   │                                │
          │                                         │                                │
          └─────────────────────────────────────────┼────────────────────────────────┘
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 Persistence & Storage                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  1. SQLite Relational Database:                                                        │
│     - users | rider_profiles | rider_devices | rider_sessions                          │
│     - verification_artifacts | rider_consents | rider_notifications                    │
│     - activity_events | risk_assessments | verification_cases | audit_logs             │
│                                                                                        │
│  2. Private Protected Storage (`instance/private_artifacts/`):                         │
│     - Live webcam captures & digital signatures stored off public web root             │
│     - SHA-256 integrity hash verification & RBAC authorization streaming              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

- **Core Language:** Python 3.11+ / Python 3.14 (fully verified, zero deprecation warnings)
- **Web Framework:** Flask 3.0.0
- **Database & ORM:** SQLite 3 & Flask-SQLAlchemy 3.0.5 (SQLAlchemy 2.0 syntax)
- **Session & Identity:** Flask-Login 0.6.3
- **Security & Forms:** Werkzeug 3.0.1 (password hashing & cryptographic randomness via `secrets`), Flask-WTF 1.3.0 (CSRF protection)
- **Data Science & ML Analytics:** scikit-learn 1.9.1, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1
- **UI Design System:** HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, Chart.js, Bootstrap Icons
- **Test Suite:** pytest 9.1.1 (56 automated unit, integration, and security tests)

---

## 4. Multi-Step Rider Onboarding Wizard

Rider onboarding has been redesigned into a modern 7-step wizard (`/onboarding/step-<1-7>`) with a persistent progress indicator, verification badges, and save-and-resume capability:

1. **Step 1 — Personal Details:** Full legal name, system-generated Rider ID (`RDR-XXXX`), email address, mobile number, preferred language, and explicit privacy consent checkbox.
2. **Step 2 — Live Rider Photograph:**
   - HTML5 `navigator.mediaDevices.getUserMedia` integration with live camera stream.
   - SVG visual oval face-positioning guide.
   - Live Capture, Retake, and Confirm controls.
   - Clearly labeled alternative file upload for environments without webcams.
   - Secure server storage in `instance/private_artifacts/` with RBAC streaming via `/media/artifact/<id>`.
3. **Step 3 — Live Signature Capture:**
   - HTML5 `<canvas>` digital signature pad supporting mouse, touchscreen, and stylus.
   - Real-time drawing, Clear, Preview, and Confirm buttons.
   - Base64 PNG encoding and secure storage with recorded timestamp and consent record.
4. **Step 4 — Aadhaar / Identity Verification (UIDAI / DigiLocker Compliance):**
   - Clear compliance disclosure explaining the verification purpose.
   - Simulated UIDAI / DigiLocker offline XML verification gateway.
   - **Strict Privacy Rule:** Zero raw 12-digit Aadhaar numbers or Aadhaar OTPs are stored. Only masked numbers (`XXXXXXXX1234`) and provider reference IDs are saved.
   - Prominently labeled **Simulated Demo Verification Mode** with synthetic test cases (`Pass`, `Review`, `Fail`).
5. **Step 5 — Location Verification:**
   - Consent-based browser `navigator.geolocation` API trigger.
   - Displays real-time latitude, longitude, and accuracy radius (meters).
   - Records permission status and verification timestamp; includes manual area declaration fallback.
6. **Step 6 — Contact Verification:**
   - Secure 6-digit OTP generated via `secrets.randbelow`.
   - Werkzeug hash storage, 10-minute expiry, max 3 attempts, rate limiting, and resend cooldown.
   - Convenient demo OTP helper for local test environments.
7. **Step 7 — Final Identity Review:**
   - Comprehensive checklist of all 6 verification stages.
   - Only marks the profile as **Fully Verified** when all mandatory steps have succeeded.
   - Profile activation confirmation screen.

---

## 5. Device Intelligence & Session Monitoring (Admin)

Under the dedicated **Device & Session Intelligence** module (`/admin/device-intelligence`):

### Fleet-Wide Overview Metrics
- **Total Registered Riders**
- **Total Registered Device References**
- **Currently Active Sessions**
- **Riders with Multiple Active Sessions**
- **Recently Added Devices (last 7 days)**
- **Revoked Sessions**

### Searchable & Filterable Rider Device Table
- Filter by verification status (`All`, `Fully Verified`, `Pending`, `Suspended`).
- Sort by active session count or registered devices.
- Direct links to inspect individual rider device profiles (`/admin/rider/<id>/devices`).

### Individual Rider Device Deep-Dive
- Inspect registered hardware references, device types, browser/OS user-agents, IP addresses, and registration dates.
- View active and revoked sessions with last activity timestamps.
- **Server-Side Session Revocation:** Administrators can revoke active sessions with a mandatory documented reason.
- **Device Revocation:** Administrators can revoke trust from suspicious devices.
- Comprehensive device activity events, risk assessment history, and administrative review records.

### Concurrent Session Security Engine
- Configurable `MAX_CONCURRENT_SESSIONS = 2` (set in `app.config`).
- Enforced at login: automatically revokes oldest sessions if limit is exceeded.
- Server-side request validation in `@app.before_request`: if a session is revoked in the database, subsequent HTTP requests immediately invalidate the Flask session and redirect to `/login` with an informative security notice.
- Self-service session revocation on the rider's dashboard (`/rider/dashboard`).

---

## 6. Complete 10-Section Administrator Control Panel

The admin interface has been expanded into an enterprise security operations center:

1. **Overview (`/admin/dashboard`):** Fleet KPI cards, risk distribution chart, pending review cases, and quick actions.
2. **Rider Management (`/admin/riders`):** Complete fleet directory, search by name/Rider ID/email, filter by status, view verification badges.
3. **Identity Verification (`/admin/identity-verification`):** Verification status breakdown, pending KYC queues, artifact inspection links, and compliance statistics.
4. **Device & Session Intelligence (`/admin/device-intelligence`):** Multi-device fleet tracking, concurrent session monitoring, and deep-dive inspection.
5. **Risk Monitoring (`/admin/risk-monitoring`):** Real-time risk distribution across Low, Moderate, High, and Very High bands with telemetry simulator.
6. **Verification Cases (`/admin/review-queue`):** Step-up challenge case queue with neutral determinations (`Legitimate Activity`, `Verification Completed`, `Further Review Required`, `Policy Escalation`, `Closed — Insufficient Evidence`).
7. **Alerts & Notifications (`/admin/alerts`):** High-priority alerts, anomalous location jumps, and rapid device churn notifications.
8. **Reports & Analytics (`/admin/reports`):** Fleet metrics, pandas-generated compliance summaries, and sanitized CSV exports.
9. **Audit Logs (`/admin/audit-logs`):** Immutable chronological record of logins, session revocations, KYC completions, and admin decisions.
10. **System Settings (`/admin/settings`):** Configurable risk thresholds, concurrent session limits, provider API keys, and demo mode toggles.

---

## 7. Account Recovery & Password Reset Workflow

- **Forgot Password Request (`/forgot-password`):** Enter registered email to generate a cryptographically secure reset token.
- **Expiring Reset Token (`/reset-password/<token>`):** 1-hour expiration, single-use invalidation, and server-side password validation.
- In demo mode, the secure reset link is displayed directly in an alert for convenient local testing.

---

## 8. Synthetic Demo Personas & Scenarios

The platform includes 7 comprehensive synthetic test personas covering the entire operational spectrum:

| Rider ID | Name | Email | Scenario | Risk Score & Status |
|---|---|---|---|---|
| `TJ-RIDER-1001` | **Alex Kumar** | `rider@trustjuggle.local` | **Normal Rider:** 1 phone, daytime deliveries in Mumbai. | `0.0 / 100` — Fully Verified |
| `TJ-RIDER-1002` | **Priya Sharma** | `priya@trustjuggle.local` | **Legitimate Phone Upgrade:** Transitioned cleanly to a new phone. | `8.8 / 100` — Fully Verified |
| `TJ-RIDER-1003` | **Rahul Verma** | `rahul@trustjuggle.local` | **Location Velocity Jump:** Delhi pickup to Mumbai dropoff in 30m (>2,000 km/h). | `30.0 / 100` — Verified |
| `TJ-RIDER-1004` | **Dev Patel** | `dev@trustjuggle.local` | **Repeated Device Churn:** 4 alternating phones in 48h. | `63.0 / 100` — Challenge Active |
| `TJ-RIDER-1005` | **Vikram Singh** | `vikram@trustjuggle.local` | **Multi-Signal Anomaly:** Alternating devices + location jump + off-hours. | `80.0 / 100` — Priority Review |
| `TJ-RIDER-1006` | **Sameer Khan** | `sameer@trustjuggle.local` | **Resolved Legitimate:** Case reviewed and approved by compliance. | `8.8 / 100` — Legitimate Activity |
| `RDR-1024` | **Suresh Patel** | `rdr1024@trustjuggle.local` | **Multi-Device Scenario:** 3 registered devices, 2 active sessions, 1 recent device, 1 verification challenge. | `68.5 / 100` — Under Review |

### Default Credentials
All rider passwords: **`Rider123!`**  
Admin password: **`admin@trustjuggle.local` / `Admin123!`**

Quick-fill demo buttons are provided on the `/login` screen for one-click access.

---

## 9. Installation & Launch Instructions (Windows)

### Prerequisites
- Python 3.11, 3.12, 3.13, or 3.14
- Windows PowerShell or Command Prompt

### Step 1: Create Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Populate Database with Synthetic Scenarios
```powershell
python scripts/seed_demo_data.py --force
```

### Step 4: Launch Flask Application
```powershell
python app.py
```

The application will start on: **`http://127.0.0.1:5000/`**

---

## 10. Automated Test Results

Run the complete 56-test automated test suite:

```powershell
python -m pytest -v
```

Or for concise output:
```powershell
python -m pytest -q
```

### Test Suite Execution Summary
```text
........................................................                 [100%]
56 passed, 1 warning in 13.72s
```

### Test Coverage Breakdown
- `tests/test_onboarding_wizard.py` (8 tests): 7-step wizard progression, valid registration, duplicate email rejection, signature submission, private artifact RBAC isolation, Aadhaar masking, location consent, profile activation.
- `tests/test_device_sessions.py` (7 tests): Device registration, session binding, concurrent session limit enforcement (`MAX_CONCURRENT_SESSIONS=2`), server-side session revocation hook, admin fleet device metrics, multi-device persona `RDR-1024`.
- `tests/test_auth.py` (6 tests): Startup, password hashing, rider registration RBAC, duplicate email handling, session management, route protection.
- `tests/test_dashboards.py` (4 tests): Empty database zero-count handling, rider data isolation, risk engine bounds [0, 100], custom 404 page.
- `tests/test_ingestion_api.py` (6 tests): Machine-to-machine authentication (`X-API-Key`), missing field validation, malformed timestamp handling, idempotency deduplication replay, automated step-up triggering on score $\ge 60$.
- `tests/test_reports.py` (7 tests): Zero-divide safety on empty database, metric aggregations, sanitized CSV exports for riders, cases, and events, role-based export protection.
- `tests/test_review_workflow.py` (5 tests): Review queue RBAC, verification IDOR prevention, admin filter queue, neutral review determinations, explanation length enforcement.
- `tests/test_risk_engine.py` (7 tests): Bounds verification, normal activity scoring, clean phone upgrade safety, alternating device switching, velocity anomaly detection, multi-signal scoring, duplicate event neutrality.
- `tests/test_verification.py` (6 tests): OTP generation, valid challenge completion, incorrect OTP attempt countdown, 3-attempt lockout, expiry rejection, token reuse prevention.

---

## 11. Real Integration vs Demo Mode Configuration

### Identity Verification Provider
In production, configure an authorized Aadhaar offline KYC / DigiLocker gateway in `config.py` or via environment variables:
```bash
set IDENTITY_PROVIDER=digilocker_kyc
set IDENTITY_PROVIDER_API_KEY=your_production_api_key
set IDENTITY_PROVIDER_URL=https://api.digilocker.gov.in/v1/kyc
```
- **Demo Mode:** When `IDENTITY_PROVIDER_API_KEY` is unset or set to `demo`, the system operates in **Demo Verification Mode**, using synthetic test cases and clear UI disclaimers.

### OTP Delivery Provider
In production, configure Twilio or Gupshup SMS gateway:
```bash
set SMS_PROVIDER=twilio
set TWILIO_ACCOUNT_SID=your_sid
set TWILIO_AUTH_TOKEN=your_token
set TWILIO_PHONE_NUMBER=+1234567890
```
- **Demo Mode:** When credentials are unset, OTPs are stored securely in the database and shown on the authenticated demo test screen for local evaluation.

---

## 12. Known Limitations & Prototype Boundaries

1. **Aadhaar Privacy Compliance:** No raw 12-digit Aadhaar numbers or Aadhaar OTPs are accepted or stored in this application. Only masked numbers (`XXXXXXXX1234`) and provider reference IDs are retained, adhering strictly to Indian privacy laws.
2. **Camera Biometric Liveness:** Web camera capture verifies live interaction and photo alignment using an interactive oval positioning guide. Enterprise deployment would incorporate active 3D face liveness models (e.g. blink or depth challenge).
3. **Simulated Telemetry:** In this hackathon prototype, delivery dispatch telemetry is synthetically generated or ingested via `/api/v1/telemetry/ingest`.
4. **Coarse Location Signals:** Continuous GPS tracking is avoided to respect worker privacy. Coarse municipal zones and browser geolocation permissions are used solely for identity and zone validation.
5. **Non-Punitive Design:** Automated heuristic scores never trigger permanent account bans. All severe anomalies open a verification case for human compliance review.
