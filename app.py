<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signature Capture</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }
        .container {
            max-width: 400px;
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        label, input, select, button {
            margin: 10px;
            padding: 10px;
            width: 100%;
            max-width: 350px;
        }
        canvas {
            border: 2px solid black;
            width: 100%;
            height: 200px;
            background-color: white;
            touch-action: none;
        }
        #confirmation-message {
            margin-top: 15px;
            font-weight: bold;
            color: green;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Signature Capture</h2>

        <label for="name">Full Name:</label>
        <input type="text" id="name" placeholder="Enter your name" required>

        <label for="subcontractor">Sub-Contractor:</label>
        <select id="subcontractor">
            <option value="" selected disabled>Select a sub-contractor</option>
            <option value="ELM Dry">ELM Dry</option>
            <option value="ELM Wet">ELM Wet</option>
            <option value="ELM PA/EWIS">ELM PA/EWIS</option>
            <option value="Ellis">Ellis</option>
            <option value="Brolec">Brolec</option>
            <option value="Nilsen LV">Nilsen LV</option>
            <option value="Nilsen Comms">Nilsen Comms</option>
            <option value="Decon">Decon</option>
            <option value="Securitas">Securitas</option>
            <option value="Schindler">Schindler</option>
        </select>

        <label for="shaft">Shaft:</label>
        <select id="shaft">
            <option value="" selected disabled>Select a shaft</option>
            <option value="Latrobe">Latrobe</option>
            <option value="Little Latrobe">Little Latrobe</option>
            <option value="A'Beckett">A'Beckett</option>
        </select>

        <label for="level">Level:</label>
        <select id="level">
            <option value="" selected disabled>Select a level</option>
            <option value="L3">L3</option>
            <option value="L2">L2</option>
            <option value="L1">L1</option>
            <option value="GF">GF</option>
            <option value="B1">B1</option>
            <option value="B2">B2</option>
            <option value="B3">B3</option>
            <option value="B4">B4</option>
            <option value="B5">B5</option>
            <option value="B6">B6</option>
            <option value="B7">B7</option>
            <option value="B8">B8</option>
        </select>

        <label for="area">Area:</label>
        <select id="area">
            <option value="" selected disabled>Select an area</option>
            <option value="BOH">BOH</option>
            <option value="FOH">FOH</option>
        </select>

        <!-- Confirmation Message (Moved Above Signature Pad) -->
        <p id="confirmation-message"></p>

        <h3>Sign Below:</h3>
        <canvas id="signature-pad"></canvas>
        <button id="clear">Clear</button>
        <button id="save">Send Signature</button>
    </div>

    <script>
        const canvas = document.getElementById("signature-pad");
        const ctx = canvas.getContext("2d");
        const confirmationMessage = document.getElementById("confirmation-message");

        let isDrawing = false;

        function resizeCanvas() {
            canvas.width = canvas.offsetWidth;
            canvas.height = 200;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        window.addEventListener("resize", resizeCanvas);
        resizeCanvas();

        function startDrawing(event) {
            isDrawing = true;
            ctx.beginPath();
            ctx.moveTo(event.offsetX, event.offsetY);
        }

        function draw(event) {
            if (!isDrawing) return;
            ctx.lineTo(event.offsetX, event.offsetY);
            ctx.strokeStyle = "black";
            ctx.lineWidth = 2;
            ctx.lineCap = "round";
            ctx.stroke();
        }

        function stopDrawing() {
            isDrawing = false;
            ctx.closePath();
        }

        canvas.addEventListener("mousedown", startDrawing);
        canvas.addEventListener("mousemove", draw);
        canvas.addEventListener("mouseup", stopDrawing);
        canvas.addEventListener("mouseout", stopDrawing);

        document.getElementById("clear").addEventListener("click", () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            confirmationMessage.style.display = "none"; // Hide confirmation message when clearing
        });

        document.getElementById("save").addEventListener("click", async () => {
            const name = document.getElementById("name").value.trim();
            const subcontractor = document.getElementById("subcontractor").value;
            const shaft = document.getElementById("shaft").value;
            const level = document.getElementById("level").value;
            const area = document.getElementById("area").value;

            if (name === "" || subcontractor === "" || shaft === "" || level === "" || area === "") {
                alert("Please fill out all fields before sending.");
                return;
            }

            const confirmationText = `I confirm that all works have been completed on ${shaft} ${level} ${area} by ${subcontractor} and any subsequent permit zone works that require LV spotters will be back-charged to ${subcontractor}.`;

            confirmationMessage.innerText = confirmationText;
            confirmationMessage.style.display = "block";

            // Pop-up confirmation before sending email
            const userConfirmed = confirm(`CONFIRM SUBMISSION:\n\n${confirmationText}\n\nClick OK to proceed or Cancel to abort.`);
            if (!userConfirmed) {
                return; // User canceled submission
            }

            const signatureDataURL = canvas.toDataURL("image/png");

            const formData = new FormData();
            formData.append("name", name);
            formData.append("confirmation_text", confirmationText);
            formData.append("signature", signatureDataURL);

            fetch("https://signature-pad-backend.onrender.com/send-email", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => alert(data.message || "Error sending email."))
            .catch(error => console.error("Error:", error));
        });
    </script>
</body>
</html>
