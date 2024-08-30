# 🚀 6573 Realty

![badge for project](https://wakapi.xiaobo.app/api/badge/%e5%b0%8f%e6%b3%a2/interval:today/project:6573Realty?label=Wakapi)

### 🌐 Description

6573 Realty is a rental search website enhanced by AI!
Sellers (landlords or agents) can simply input the price, address, and public facilities, and upload photos. The AI will then generate corresponding titles, descriptions, and list the facilities in the house based on the photos. This makes it convenient and fast for landlords, saving them from spending a lot of time thinking about titles and inputting tedious information!

For buyers, we use a tag mechanism. Each property has a set of tags that describe it. By combining these tags, we can accurately describe the property. Therefore, by obtaining the user's preferred tags and fitting the similarity between the user's preferences and the property's tags, we can achieve the best algorithmic results. This significantly reduces the time spent searching for a desired property, saving more than 90% of the time!
65, 73? Why is it called 6573 Realty?

Because in the ASCII table, A is 65 and I is 73. We hope to revolutionize the search method with AI!

### Quick Preview



https://github.com/user-attachments/assets/c8275129-3087-46e7-9bef-2d45cbfcf8e3



## 🚀 Deployment

Before deploying the app, make sure you have all the prerequisites installed and api keys ready.

### 📋 Prerequisites
* Python 3.12
* MongoDB
* Redis
* Docker (optional)
#### 🔑 APIs
* OpenAI (or Azure OpenAI)
* Google (OAuth)

You can deploy the app using Docker or just setup self.
### 🐳 Docker
You can just use docker run, also use docker-compose.  
Docker image:
```
xiaobocute/time_traveler:latest
```

### 🛠 Setup
#### 1️⃣ Install requirements
Recommend to use virtual environment for python 3.12.  
All requirements are listed in the `requirements.txt` file. To install them, using `pip install -r requirements.txt` should suffice.
#### 2️⃣ Configure environment variables
Edit `.env` file in the root directory and add the following environment variables:
```
# -- Flask --
HOST="0.0.0.0"
PORT=80
# If DEBUG True, flask will run in debug mode.
# If SECRET_KEY not False, flask will generate a random key every time it starts.
DEBUG=True
SECRET_KEY="123456789"
SESSION_TIMEOUT=604800
HOST_DOMAIN=""
TORCH_DEVICE="cuda" # cuda or cpu

# -- Settings --
# If True, the app will use Azure OpenAI API, otherwise it will use OpenAI API.
USE_AZURE_OPENAI=True
MODEL_SMART_NAME="gpt4o" # For assistant
MODEL_FAST_NAME="gpt4o"
MODEL_CHAT_DEFAULT="gpt4o" # For chat (openai_chat)

# -- AZURE --
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_API_VERSION=""

# -- Keys --
GOOGLE_OAUTH_CLIENT_ID=""
GOOGLE_OAUTH_CLIENT_SECRET=""
OPENAI_API_KEY=""
MAPBOX_ACCESS_TOKEN=""
TURNSTILE_SECRET_KEY=""

# -- Database --
MONGO_URI=""
REDIS_URI=""

# -- Assistant --

# -- Mail --
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME="mail.xiaobo.tw@gmail.com"
MAIL_PASSWORD="bmfionntwbnemefs"
MAIL_DEFAULT_SENDER="6573@xiaobo.tw"
```

#### 3️⃣ Run the app
Use `python run.py` to run the app in development.  
! Do not use the flask run command to start the application; instead, use python run.py. !

## 📜 License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license. 

### 📌 Key Points:

1. **NonCommercial**: You may not use the material for commercial purposes.
2. **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
3. **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

### 📝 Additional Notes:

- **Technical Modifications**: You are allowed to make necessary technical modifications to the material.
- **No Additional Restrictions**: You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
  
If you want to see the official description of the CC BY-NC-SA 4.0 license, you can visit https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.

### 🚨 Important:

If there is any conflict between the contents of this project and the CC BY-NC-SA 4.0 license, the terms of the CC BY-NC-SA 4.0 license shall prevail. Any interpretations that conflict with the CC BY-NC-SA 4.0 license are invalid unless formally agreed upon by the author in a signed contract.
