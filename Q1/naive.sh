docker build -t spam-api:naive -f Dockerfile.naive .

docker images spam-api:naive

docker run -d -p 8000:8000 --name naive-container spam-api:naive
sleep 3
curl -X GET "http://localhost:8000/healthz"
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'

docker stop naive-container && docker rm naive-container