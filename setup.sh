echo "Starting process..."

if [ "$#" -ne 1 ]; then
  echo "Parameter required PORT"
  exit 1
fi

PORT="$1"

if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "PORT must be a non-negative integer."
  exit 1
fi

PIDS=$(timeout 2s lsof -ti ":$PORT")
if [ -n "$PIDS" ]; then
  kill -9 $PIDS
fi

git pull
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

gunicorn -b ":$PORT" app:app --access-logfile - --error-logfile -
