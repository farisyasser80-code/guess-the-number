
from flask import Flask, request, session, render_template_string
import random
import os
import threading


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Guess The Number</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial, sans-serif;
    color: white;
   background:
radial-gradient(circle at 20% 20%, #7c3aed55, transparent 40%),
radial-gradient(circle at 80% 80%, #06b6d455, transparent 40%),
linear-gradient(135deg, #050816, #111827, #090b20);
}

.game {
    width: 90%;
    max-width: 430px;
    padding: 40px 25px;
    text-align: center;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 25px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    backdrop-filter: blur(15px);
}

h1 {
    font-size: 30px;
    color: #55d6ff;
}

p {
    color: #c5d1e8;
}

input {
    width: 100%;
    padding: 15px;
    margin: 20px 0;
    border-radius: 12px;
    border: 1px solid #405575;
    background: #101a30;
    color: white;
    font-size: 20px;
    text-align: center;
}

button {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #087cff, #36d6ff);
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    opacity: 0.85;
}

.message {
    margin-top: 22px;
    font-size: 18px;
    color: #55d6ff;
}

.footer {
    margin-top: 30px;
    font-size: 12px;
    color: #71819c;
}
.number-rain {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.floating-number {
    position: absolute;
    bottom: -50px;
    color: #38bdf8;
    font-size: 22px;
    font-weight: bold;
    opacity: 0.35;
    text-shadow: 0 0 12px #06b6d4;
    animation: numberFloat linear infinite;
}

@keyframes numberFloat {
    from { transform: translateY(0); opacity: 0; }
    20% { opacity: 0.5; }
    to { transform: translateY(-110vh); opacity: 0; }
}

.game {
    position: relative;
    z-index: 2;
}
</style>
</head>

<body>
<div class="number-bg">
    <span class="floating-number">01</span>
    <span class="floating-number">42</span>
    <span class="floating-number">87</span>
    <span class="floating-number">13</span>
    <span class="floating-number">99</span>
    <span class="floating-number">56</span>
    <span class="floating-number">24</span>
</div>
<div class="game">

<h1>GUESS THE NUMBER</h1>
<p>Choose a number between 1 and 100</p>

<form method="POST">
<input type="number" name="guess"
min="1" max="100" required placeholder="Your guess">

<button type="submit">CHECK NUMBER</button>
</form>

<div class="message">{{ message }}</div>

<p>Attempts: {{ attempts }}</p>

<form method="GET">
<button type="submit">NEW GAME</button>
</form>

<div class="footer">GUESS GAME • GOOD LUCK</div>

</div>

<button id="musicBtn" onclick="toggleMusic()">
    🎵 Music ON/OFF
</button>

<script>
let audioCtx;
let musicOn = false;
let musicTimer;

function startMusic() {
    if (musicOn) return;

    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    musicOn = true;

    const notes = [261.63, 329.63, 392, 329.63, 293.66, 349.23, 440, 392];
    let i = 0;

    function playNote() {
        if (!musicOn) return;

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = "sine";
        osc.frequency.value = notes[i % notes.length];

        gain.gain.setValueAtTime(0.035, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + 0.4);

        i++;
    }

    playNote();
    musicTimer = setInterval(playNote, 500);
}

function toggleMusic() {
    if (!musicOn) {
        startMusic();
    } else {
        musicOn = false;
        clearInterval(musicTimer);
    }
}

document.addEventListener("click", function() {
    if (!musicOn) startMusic();
}, { once: true });
</script></body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def game():

    if "secret" not in session or request.method == "GET":
        session["secret"] = random.randint(1, 100)
        session["attempts"] = 0

    message = "Start guessing!"

    if request.method == "POST":
        guess = int(request.form["guess"])
        session["attempts"] += 1
        secret = session["secret"]

        if guess < secret:
            message = "Too Low! Try Higher 🔼"

        elif guess > secret:
            message = "Too High! Try Lower 🔽"

        else:
            message = "Correct! You Won 🎉"
            session["secret"] = random.randint(1, 100)
            session["attempts"] = 0

    return render_template_string(
        HTML,
        message=message,
        attempts=session["attempts"]
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
