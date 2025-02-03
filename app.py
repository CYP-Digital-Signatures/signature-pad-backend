from flask import Flask, request, jsonify
import smtplib
import base64
import os
from email.message import EmailMessage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Email credentials
SENDER_EMAIL = "cypdigitalsignatures@gmail.com"
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Securely fetch from Render
RECEIVER_EMAIL = "cypdigitalsignatures@gmail.com"

# Manually defined CC emails (modify as needed)
CC_EMAILS = ["david.memish@metrotunnelcyp-dc.com.au", "cypdigitalsignatures@gmail.com"]

# ✅ Root route to confirm backend is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

# ✅ Send-email route (only allows POST requests)
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        name = request.form.get("name")
        user_email = request.form.get("email")
        confirmation_text = request.form.get("confirmation_text")
        signature_data = request.form.get("signature")

        if not name or not user_email or not confirmation_text or not signature_data:
            return jsonify({"error": "Missing data"}), 400

        # Decode Base64 signature data
        signature_bytes = base64.b64decode(signature_data.replace("data:image/png;base64,", ""))

        # Create email
        msg = EmailMessage()
        msg["Subject"] = "New Signature Submission"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Cc"] = ", ".join([user_email] + CC_EMAILS)  # CC user & additional recipients
        msg.set_content(f"{confirmation_text}\n\nSubmitted by: {name} ({user_email})")

        # Attach the signature image
        msg.add_attachment(signature_bytes, maintype="image", subtype="png", filename="signature.png")

        # Send email via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Signature emailed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Uses the correct port for Render
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
