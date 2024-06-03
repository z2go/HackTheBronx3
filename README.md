# Hack the Bronx


<b>To run locally:</b>

1. Clone the repository
2. Install dependencies through ```pip install -r requirements.txt```
3. Navigate to the main.py file and run it
4. The server will be running on your localhost:5000, which you should be able to acesss and use the website from

<b>How it works:</b>

<ul>
    <li>Uses HTML / CSS for the frontend</li>
    <li>Python's Flask for the backend</li>
    <li>JavaScript for communicating between the backend and frontend</li>
    <li>Flask SQLAlchemy for the database</li>
</ul>

<b>Other details:</b>

<ul>
    <li>Default login: Username: Testing, Password: testing123</li>
    <li>To get map feature working, create .env file in main directory and write MAPS_API_KEY={the api key}. The google maps api key can be obtained from these steps: https://developers.google.com/maps/documentation/javascript/get-api-key</li>
    <li>Similarly, to get the "find job matches" working, to that same .env file, add OPENAI_GPT_KEY={the api key}. This can be obtained through the OpenAI API website</li>
</ul>