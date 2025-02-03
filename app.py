from flask import Flask, request, jsonify
import smtplib
import base64
import os
from email.message import EmailMessage
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Email sender configuration (using environment variables)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "cypdigitalsignatures@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "CYPpassword")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "cypdigitalsignatures@gmail.com")

@app.route("/send-email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    subcontractor = request.form.get("subcontractor")
    shaft = request.form.get("shaft")
    level = request.form.get("level")
    area = request.form.get("area")
    signature_data = request.form.get("signature")

    if not name or not subcontractor or not shaft or not level or not area or not signature_data:
        return jsonify({"error": "Missing data"}), 400

    # Convert Base64 signature data to an actual image file
    signature_data = signature_data.replace("data:image/png;base64,", "")
    signature_bytes = base64.b64decode(signature_data)

    # Create email content
    msg = EmailMessage()
    msg["Subject"] = "New Signature Submission"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(f"""
    New signature submitted:

    - Name: {name}
    - Sub-Contractor: {subcontractor}
    - Shaft: {shaft}
    - Level: {level}
    - Area: {area}
    """)

    # Attach the signature image
    msg.add_attachment(signature_bytes, maintype="image", subtype="png", filename="signature.png")

    # Send email via SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return jsonify({"message": "Signature emailed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
