# dh-llm
Large Language Model Hallucinations Detector (Python/Flask + React/PrimeReact)


1. Build app docker image: ```docker build -t dh-llm-img .```
2. Run docker image in container ```docker run -dp 5005:5000 -w /app -v "$(pwd):/app" dh-llm-img```.
   <br />
   App API will be available under this address: ```http://127.0.0.1:5005/path```

3. API schema can be viewed in swagger interface: ```http://127.0.0.1:5005/swagger-ui```

4. CD into frontend directory and run ```npm install```
5. Start frontend app ```npm start```.
   <br />
   SPA should start in browser with the address: ```http://127.0.0.1:3000/```
