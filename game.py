
from flask import Flask, request, session, render_template_string
import random
import os
import threading
import webview

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
    radial-gradient(circle at top, #263c65, transparent 55%),
    linear-gradient(135deg, #080d1c, #101b35, #050812);
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
</style>
</head>

<body>
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
</body>
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