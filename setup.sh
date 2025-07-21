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

kill -9 $(lsof -ti ":$PORT") 2>/dev/null
git pull
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo ":$PORT"

gunicorn -b ":$PORT" app:app

