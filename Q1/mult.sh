docker build -t spam-api:multistage -f Dockerfile .

docker run -d -p 8000:8000 --name multistage-container spam-api:multistage

sleep 3
curl -X GET "http://localhost:8000/healthz"
echo ""
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
echo ""

docker stop multistage-container && docker rm multistage-container

docker images | grep spam-api