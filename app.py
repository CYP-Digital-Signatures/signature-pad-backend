from flask import Flask, request, jsonify
import smtplib
import base64
import os
from email.message import EmailMessage
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "cypdigitalsignatures@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "qllxxvtkwmzkzzxv")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "cypdigitalsignatures@gmail.com")

# Manually define CC emails (Add more emails here if needed)
CC_EMAILS = ["manager@example.com", "admin@example.com"]

@app.route("/send-email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    user_email = request.form.get("email")
    confirmation_text = request.form.get("confirmation_text")
    signature_data = request.form.get("signature")

    if not name or not user_email or not confirmation_text or not signature_data:
        return jsonify({"error": "Missing data"}), 400

    signature_bytes = base64.b64decode(signature_data.replace("data:image/png;base64,", ""))

    msg = EmailMessage()
    msg["Subject"] = "New Signature Submission"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Cc"] = ", ".join([user_email] + CC_EMAILS)  # CC user & additional recipients
    msg.set_content(f"{confirmation_text}\n\nSubmitted by: {name} ({user_email})")

    msg.add_attachment(signature_bytes, maintype="image", subtype="png", filename="signature.png")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return jsonify({"message": "Signature emailed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
