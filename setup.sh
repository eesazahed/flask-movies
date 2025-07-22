echo "Starting process..."

# Exit if no port number is provided
if [ "$#" -ne 1 ]; then
  echo "Parameter required PORT"
  exit 1
fi

PORT="$1"

# Exit if the port is not a non-negative integer
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "PORT must be a non-negative integer."
  exit 1
fi

# Kill any process currently using the specified port
PIDS=$(timeout 2s lsof -ti ":$PORT")
if [ -n "$PIDS" ]; then
  kill -9 $PIDS
fi

# Update code from GitHub repo
if ! git pull; then
  echo "git pull failed"
  exit 1
fi

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the Flask app using Gunicorn on the specified port
gunicorn -b ":$PORT" app:app
