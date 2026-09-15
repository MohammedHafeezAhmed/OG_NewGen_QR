import os
import time
import secrets

from flask import Flask, render_template, request, jsonify, redirect, url_for


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# ============================================================
# IN-MEMORY DATA
# ============================================================

ACTIVE_SESSIONS = {}
TEACHER_PRESETS = []


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():
    return redirect(url_for("admin_dashboard"))


# ============================================================
# ADMIN PAGE
# ============================================================

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")


# ============================================================
# PRESETS
# ============================================================

@app.route("/api/presets", methods=["GET", "POST"])
def manage_presets():

    # SAVE PRESET
    if request.method == "POST":

        data = request.json or {}

        sub = data.get("subject", "").strip()
        phone = data.get("phone", "").strip()

        if sub and phone:

            TEACHER_PRESETS.append({
                "subject": sub,
                "phone": phone
            })

            return jsonify({
                "status": "success",
                "presets": TEACHER_PRESETS
            })

        return jsonify({
            "status": "error",
            "message": "Invalid input"
        }), 400

    # GET PRESETS
    return jsonify({
        "presets": TEACHER_PRESETS
    })


# ============================================================
# GENERATE ATTENDANCE LINK
# ============================================================

@app.route("/api/generate-link", methods=["POST"])
def generate_link():

    data = request.json or {}

    subject = data.get("subject", "").strip()
    phone = data.get("phone", "").strip()

    if not subject or not phone:

        return jsonify({
            "status": "error",
            "message": "Subject and Phone required"
        }), 400

    # Create unique attendance session
    session_id = secrets.token_urlsafe(8)

    # 10 minute expiry
    expires_at = time.time() + (10 * 60)

    ACTIVE_SESSIONS[session_id] = {
        "subject": subject,
        "phone": phone,
        "expires_at": expires_at,
        "scans": set()
    }

    # IMPORTANT:
    # Build the scan URL from the SAME server/domain
    # that the admin page is currently using.
    scan_link = url_for(
        "scan_page",
        session_id=session_id,
        _external=True
    )

    return jsonify({
        "status": "success",
        "session_id": session_id,
        "expires_at": expires_at,
        "link": scan_link
    })


# ============================================================
# STUDENT SCAN PAGE
# ============================================================

@app.route("/scan/<session_id>")
def scan_page(session_id):

    session = ACTIVE_SESSIONS.get(session_id)

    if not session:

        return """
        <h3 style="
            color:white;
            background:#000;
            text-align:center;
            font-family:sans-serif;
            padding:40px;
        ">
            Invalid or Expired Link
        </h3>
        """, 404

    is_expired = time.time() > session["expires_at"]

    return render_template(
        "scan.html",
        session_id=session_id,
        is_expired=is_expired
    )


# ============================================================
# SUBMIT SCANNED USN
# ============================================================

@app.route("/api/submit-scan", methods=["POST"])
def submit_scan():

    data = request.json or {}

    session_id = data.get("session_id")

    raw_usn = data.get("usn", "").strip().upper()

    # Find attendance session
    session = ACTIVE_SESSIONS.get(session_id)

    if not session:

        return jsonify({
            "status": "error",
            "message": "Session not found"
        }), 400

    # Check expiry
    if time.time() > session["expires_at"]:

        return jsonify({
            "status": "error",
            "message": "Link expired!"
        }), 410

    # Validate QR data
    if not raw_usn:

        return jsonify({
            "status": "error",
            "message": "Invalid QR Data"
        }), 400

    # Already scanned?
    if raw_usn in session["scans"]:

        return jsonify({
            "status": "error",
            "message": "Attendance already recorded for this USN"
        }), 409

    # Save USN
    session["scans"].add(raw_usn)

    return jsonify({
        "status": "success",
        "usn": raw_usn
    })


# ============================================================
# LIVE ATTENDANCE DATA
# ============================================================

@app.route("/api/live-data/<session_id>")
def get_live_data(session_id):

    session = ACTIVE_SESSIONS.get(session_id)

    if not session:

        return jsonify({
            "status": "error",
            "message": "Session not found"
        }), 404

    raw_usns = list(session["scans"])

    # Sort according to last 3 numeric digits
    def get_last3_numeric(usn):

        digits = ''.join(filter(str.isdigit, usn))

        return int(digits[-3:]) if len(digits) >= 3 else 9999

    sorted_usns = sorted(
        raw_usns,
        key=get_last3_numeric
    )

    # Show only last 3 characters in admin display
    formatted_short = [
        u[-3:] if len(u) >= 3 else u
        for u in sorted_usns
    ]

    time_remaining = int(
        session["expires_at"] - time.time()
    )

    return jsonify({
        "status": "success",
        "subject": session["subject"],
        "phone": session["phone"],
        "count": len(sorted_usns),
        "raw_usns": sorted_usns,
        "formatted_list": " ".join(formatted_short),
        "time_remaining": max(0, time_remaining)
    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    # Hosting services provide PORT automatically.
    # Locally it will use 5000.
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )