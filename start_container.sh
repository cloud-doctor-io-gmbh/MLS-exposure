sudo docker build -f docker/Dockerfile -t exposure-api .
sudo docker run -d -p 8080:8080 --restart always -v "${PWD}":/app exposure-api
