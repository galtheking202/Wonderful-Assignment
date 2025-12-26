sudo docker build -t mongo-single-app .
sudo docker run -p 27017:27017 -e OPENAI_API_KEY=YOUR_API_KEY_HERE mongo-single-app
