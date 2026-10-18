"""Forms for TrustJuggle AI using Flask-WTF and WTForms."""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Regexp, Length, EqualTo, ValidationError
from models.models import User

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class LoginForm(FlaskForm):
    """User authentication login form."""

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Regexp(EMAIL_REGEX, message="Please enter a valid email address."),
            Length(max=120),
        ],
        render_kw={"placeholder": "e.g. rider@trustjuggle.local", "autocomplete": "email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password", "autocomplete": "current-password"},
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    """New delivery rider registration form (Public registration restricted to riders)."""

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "e.g. Alex Kumar"},
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Regexp(EMAIL_REGEX, message="Please enter a valid email address."),
            Length(max=120),
        ],
        render_kw={"placeholder": "e.g. alex.kumar@example.com", "autocomplete": "email"},
    )
    phone_number = StringField(
        "Mobile Number",
        validators=[DataRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "e.g. +91 98765 43210"},
    )
    vehicle_type = SelectField(
        "Primary Delivery Vehicle",
        choices=[
            ("Motorcycle", "Motorcycle / Scooter (Petrol)"),
            ("EV Scooter", "Electric Scooter (EV)"),
            ("Bicycle", "Bicycle / E-Bike"),
            ("Compact Van", "Four-Wheeler / Van"),
        ],
        default="Motorcycle",
    )
    device_model = StringField(
        "Primary Phone Model (Baseline Reference)",
        validators=[DataRequired(), Length(min=3, max=100)],
        render_kw={"placeholder": "e.g. Samsung Galaxy A54 5G"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
        render_kw={"placeholder": "At least 8 characters", "autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match exactly."),
        ],
        render_kw={"placeholder": "Re-enter password", "autocomplete": "new-password"},
    )
    submit = SubmitField("Create Rider Account")

    def validate_email(self, field):
        """Ensure email is unique across all users."""
        if User.query.filter_by(email=field.data.lower().strip()).first():
            raise ValidationError("This email address is already registered. Please sign in.")


class ReviewDecisionForm(FlaskForm):
    """Administrator human review decision submission form."""

    decision = SelectField(
        "Review Decision",
        choices=[
            ("Legitimate Activity", "Legitimate Activity (Confirmed phone upgrade / normal change)"),
            ("Verification Completed", "Verification Completed (Step-up challenge validated)"),
            ("Further Review Required", "Further Review Required (Contact rider / dispatch team)"),
            ("Policy Escalation", "Policy Escalation (Escalate for in-person review)"),
            ("Closed — Insufficient Evidence", "Closed — Insufficient Evidence (Case resolved without penalty)"),
        ],
        validators=[DataRequired()],
    )
    explanation = TextAreaField(
        "Audited Justification & Findings",
        validators=[
            DataRequired(),
            Length(min=10, message="Please provide at least 10 characters explaining your decision."),
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Explain the rationale, verified evidence, or customer support ticket reference...",
        },
    )
    submit = SubmitField("Record Review Decision")


class VerificationChallengeForm(FlaskForm):
    """Rider step-up verification submission form."""

    challenge_type = SelectField(
        "Verification Mode",
        choices=[
            ("simulated_otp_challenge", "Simulated One-Time Code (OTP)"),
            ("biometric_selfie_liveness", "Live Facial Liveness Check (Simulated)"),
            ("device_binding_otp", "Device Secure Enclave Re-Binding"),
        ],
        validators=[DataRequired()],
    )
    otp_code = StringField(
        "Verification Code (OTP)",
        render_kw={"placeholder": "Enter 6-digit code (e.g. from banner above)", "maxlength": "10"},
    )
    device_name = StringField(
        "Device Reference",
        render_kw={"placeholder": "e.g. Current Smartphone Model"},
    )
    submit = SubmitField("Submit Verification")


class TelemetrySimulationForm(FlaskForm):
    """Admin authorized demo-event simulator form."""

    event_type = SelectField(
        "Event Type",
        choices=[
            ("order_delivered", "Order Delivered"),
            ("order_pickup", "Order Picked Up"),
            ("login", "App Login Event"),
            ("shift_start", "Shift Commenced"),
            ("shift_end", "Shift Ended"),
            ("device_ping", "Passive Telemetry Heartbeat"),
            ("simulated_test_event", "Compliance Test Event"),
        ],
        default="order_delivered",
    )
    device_ref = StringField(
        "Device Reference",
        validators=[DataRequired()],
        render_kw={"placeholder": "e.g. DEV-SAMSUNG-A54-MUMBAI-01"},
    )
    coarse_location = SelectField(
        "Coarse Location (Municipal Zone)",
        choices=[
            ("Bandra West, Mumbai", "Bandra West, Mumbai"),
            ("Andheri East, Mumbai", "Andheri East, Mumbai"),
            ("Thane Municipal, Mumbai", "Thane Municipal, Mumbai"),
            ("Connaught Place, Delhi", "Connaught Place, Delhi"),
            ("Cyber City, Gurgaon", "Cyber City, Gurgaon"),
            ("Koramangala, Bengaluru", "Koramangala, Bengaluru"),
            ("Hitec City, Hyderabad", "Hitec City, Hyderabad"),
            ("Shivajinagar, Pune", "Shivajinagar, Pune"),
        ],
        default="Bandra West, Mumbai",
    )
    network_signal = SelectField(
        "Network Infrastructure",
        choices=[
            ("4G Mobile - Carrier Jio", "Standard 4G Mobile (Jio)"),
            ("5G Mobile - Carrier Airtel", "Standard 5G Mobile (Airtel)"),
            ("WiFi - Verified Merchant Hub", "Verified Commercial WiFi"),
            ("Datacenter Proxy - Suspicious IP", "Datacenter Proxy / Anonymizer (Suspicious)"),
            ("Unknown TOR Exit Node", "TOR Node / Masked Carrier (Suspicious)"),
        ],
        default="4G Mobile - Carrier Jio",
    )
    submit = SubmitField("Ingest Simulated Telemetry Event")


class ForgotPasswordForm(FlaskForm):
    """Account password recovery request form."""

    email = StringField(
        "Registered Email Address",
        validators=[
            DataRequired(),
            Regexp(EMAIL_REGEX, message="Please enter a valid email address."),
            Length(max=120),
        ],
        render_kw={"placeholder": "e.g. rider@trustjuggle.local", "autocomplete": "email"},
    )
    submit = SubmitField("Generate Secure Recovery Link")


class ResetPasswordForm(FlaskForm):
    """Account password reset form."""

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
        render_kw={"placeholder": "At least 8 characters", "autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match exactly."),
        ],
        render_kw={"placeholder": "Re-enter new password", "autocomplete": "new-password"},
    )
    submit = SubmitField("Update Password & Invalidate Other Sessions")


class OnboardingStep1Form(FlaskForm):
    """Step 1: Personal details and legal consent."""

    full_name = StringField(
        "Full Legal Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "As shown on government identity document"},
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Regexp(EMAIL_REGEX, message="Please enter a valid email address."),
            Length(max=120),
        ],
        render_kw={"placeholder": "name@example.com"},
    )
    phone_number = StringField(
        "Mobile Number",
        validators=[DataRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "+91 98765 43210"},
    )
    date_of_birth = StringField(
        "Date of Birth (YYYY-MM-DD)",
        render_kw={"placeholder": "e.g. 1996-08-15", "type": "date"},
    )
    preferred_language = SelectField(
        "Preferred Interface Language",
        choices=[
            ("English", "English"),
            ("Hindi", "Hindi (हिन्दी)"),
            ("Marathi", "Marathi (मराठी)"),
            ("Tamil", "Tamil (தமிழ்)"),
            ("Telugu", "Telugu (తెలుగు)"),
            ("Bengali", "Bengali (বাংলা)"),
        ],
        default="English",
    )
    operating_city = SelectField(
        "Primary Operating Delivery Zone",
        choices=[
            ("Mumbai", "Mumbai Metropolitan Region"),
            ("Delhi-NCR", "Delhi - National Capital Region"),
            ("Bengaluru", "Bengaluru Urban"),
            ("Hyderabad", "Hyderabad Cyber Hub"),
            ("Pune", "Pune Municipal Area"),
            ("Chennai", "Chennai Greater Region"),
            ("Kolkata", "Kolkata City"),
        ],
        default="Mumbai",
    )
    vehicle_type = SelectField(
        "Delivery Vehicle Type",
        choices=[
            ("Motorcycle", "Motorcycle / Scooter (Petrol)"),
            ("EV Scooter", "Electric Scooter (EV)"),
            ("Bicycle", "Bicycle / E-Bike"),
            ("Compact Van", "Four-Wheeler / Commercial Van"),
        ],
        default="Motorcycle",
    )
    consent_terms = BooleanField(
        "I consent to platform terms of service, fraud prevention data processing, and identity verification.",
        validators=[DataRequired(message="Explicit consent is mandatory to continue onboarding.")],
    )
    submit = SubmitField("Save Details & Continue to Photograph Capture")


class OnboardingStep4IdentityForm(FlaskForm):
    """Step 4: Identity & KYC Verification with UIDAI compliance."""

    doc_type = SelectField(
        "Select Verification Document",
        choices=[
            ("aadhaar_masked", "Aadhaar Masked Offline e-KYC (UIDAI Compliant - No raw numbers stored)"),
            ("driving_license", "State Motor Vehicles Driving License"),
            ("voter_id", "Election Commission Voter ID Card (EPIC)"),
            ("pan_card", "Income Tax Department Permanent Account Number (PAN)"),
        ],
        default="aadhaar_masked",
    )
    identifier_input = StringField(
        "Masked Identifier / Test Reference",
        render_kw={
            "placeholder": "e.g. XXXXXXXX1234 (Only last 4 digits needed for demo)",
            "maxlength": "30",
        },
    )
    consent_kyc = BooleanField(
        "I explicitly authorize the platform to verify this document reference via authorized KYC gateway or synthetic demo sandbox.",
        validators=[DataRequired(message="Identity verification consent is required.")],
    )
    submit = SubmitField("Verify Identity Reference")


class OnboardingStep6ContactForm(FlaskForm):
    """Step 6: Contact verification OTP."""

    otp_code = StringField(
        "6-Digit Verification Code",
        validators=[DataRequired(), Length(min=4, max=10)],
        render_kw={"placeholder": "e.g. 842109", "autocomplete": "one-time-code"},
    )
    submit = SubmitField("Confirm Verification Code")


