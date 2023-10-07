if command -v python3 &>/dev/null; then
    python3_path=$(command -v python3)
    $python3_path -m pip install -r requirements.txt

    echo "Benodigheden voor server klaar"
    gunicorn --bind 0.0.0.0:9090 main:app
    # $python3_path $(echo "$(pwd)/main.py")
else
    echo "Python 3 is not niet geinstalleerd."
fi



