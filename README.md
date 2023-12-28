# Discord ChatBot

> To-Do List
> - [x] discord chatbot
> - [ ] use mongo to store memory
> - [ ] support ChatGPT Proxy

> Supported tools list
> - Open Weather API
> - Google Programmable Search Engine API
> - ... (you can request another tools in issue, I will try my best to add it to this chatbot)

## Set up

## Critical prerequisites to install

* run ```pip3 install -r requirements.txt```

* **Rename the file `.env.example` to `.env`**

* Recommended python version `3.9` +

## Get your discord bot

1. Go to https://discord.com/developers/applications create an application
2. Build a Discord bot under the application
3. Get the token from bot setting
   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`
   ![image](https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png)
5. Turn MESSAGE CONTENT INTENT `ON`
   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)
6. Invite your bot to your server via OAuth2 URL Generator
   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)

## Get you OpenAI token

1. Go to https://beta.openai.com/account/api-keys
2. Click Create new secret key
   ![image](https://user-images.githubusercontent.com/89479282/207970699-2e0cb671-8636-4e27-b1f3-b75d6db9b57e.PNG)
3. Store the SECRET KEY to `.env` under the `OPENAI_API_KEY`

## (Optional) Setup system prompt

* A system prompt would be invoked when the bot is first started or reset
* You can set it up by modifying the content in `system_prompt.txt`
* All the text in the file will be fired as a prompt to the bot
* Get the first message from ChatGPT in your discord channel!
* Go Discord setting turn `developer mode` on

1. Right-click the channel you want to receive the message, `Copy  ID`
   ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

2. paste it into `.env` under `DISCORD_CHANNEL_ID`

## (Optional) Get Your Id

* Go Discord setting turn `developer mode` on

1. right-click your discord icon and copy user id
2. paste it into `.env` under `DISCORD_ADMIN`
3. also you can add multi admin like `admin-1,admin-2,admin-3`

## (Optional) Get Your Open Weather API Key

1. go to [Open Weather Official Website](https://openweathermap.org/)
2. Create an Account
3. go to API Keys tab
4. copy the key
5. paste it into `.env` under `OPEN_WEATHER_API`

## (Optional) Get Your Google Programmable Search Engine API Key and Get Your Google Programmable Search Engine ID

- ### Google Programmable Search Engine API Key
   1. go to [Programmable Search Engine Overview page](https://developers.google.com/custom-search/v1/overview)
   2. Click the `Get a Key` button
   3. Select Google Cloud Project
   4. Copy the key under `YOUR API KEY`
   5. paste it into `.env` under `GOOGLE_SEARCH_API_KEY`

- ### Get Your Google Programmable Search Engine ID
   1. go to [Programmable Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/create)
   2. Create your own Search Engine
   3. you will get a script like this
      ```javascript
      <script async src="https://cse.google.com/cse.js?cx=d3218cb6a43f949bc">
      </script>
      <div class="gcse-search"></div>
      ```
   4. Copy the parameters value named `cx`
   5. paste it into `.env` under `GOOGLE_CX`

------

## Commands

* `/chat [message]` Chat with ChatGPT every model
* `/imagine [prompt]` Generate an image with the DALL·E 2 or 3 model
* `/reset` Reset sender conversation history
* `/remove` Clear all conversation history by admin only