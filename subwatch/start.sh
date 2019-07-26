
clear
echo "Added SSH Key for Servio HTTPS Server"
ssh -R 443:localhost:5000 serveo.net &

python /app/main.py &