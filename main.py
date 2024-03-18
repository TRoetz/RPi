from flask import Flask, render_template, request
import RPi.GPIO as GPIO

# Define relay names and initial states
relay_data = [
    {"name": "Crush Light", "state": False},
    {"name": "Shelter Light", "state": False},
    {"name": "Small Paddock Light", "state": False},
    {"name": "Round Pen Shelter Light", "state": False},
    {"name": "Round Pen Entrance Light", "state": False},
    {"name": "Round Pen Opposite Light", "state": False},
    {"name": "Round Pen Roadside Light", "state": False},
    {"name": "Main Pen Saddle light", "state": False},
]

# Define GPIO pin numbers (replace with your actual pins)
RELAY_PINS = [2, 3, 4, 17, 27, 22, 10, 9]

# Define initial relay states (all off)
relay_states = [data["state"] for data in relay_data]

# Set up GPIO pins (BCM numbering)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PINS, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html", relay_data=relay_data)

@app.route("/toggle_all", methods=["POST"])
def toggle_all():
  global relay_states
  new_state = not all(relay_states)  # Toggle all relays to opposite state
  relay_states = [new_state] * 8
  set_relays(relay_states)
  return "OK"

@app.route("/toggle/<int:relay_id>", methods=["POST"])
def toggle_relay(relay_id):
  global relay_states
  if 0 <= relay_id < 8:
    relay_states[relay_id] = not relay_states[relay_id]
    set_relays(relay_states)
    return "OK"
  else:
    return "Invalid relay ID", 400

def set_relays(states):
  for i, state in enumerate(states):
    GPIO.output(RELAY_PINS[i], GPIO.LOW if state else GPIO.HIGH)

if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0", debug=True)
  finally:
    GPIO.cleanup()