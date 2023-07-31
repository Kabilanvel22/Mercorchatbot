
import openai
import requests


api_key = "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"


openai.api_key = api_key


todo_list = {}


reminders = {}


user_info = {}


knowledge_base = {
    "What is the capital of France?": "The capital of France is Paris.",
    "What is the square root of 16?": "The square root of 16 is 4.",
    "What is the boiling point of water?": "The boiling point of water is 100°C or 212°F.",
  
}


def handle_message(message):
    if message.lower() in ["hi", "hello", "hey"]:
        return "Hello! I'm your Personal Assistant. How can I assist you today?"

    elif message.startswith("help"):
        return "Available commands:\n" \
               "- Ask a question\n" \
               "- Calculate: <expression>\n" \
               "- Add task: <task>\n" \
               "- View tasks\n" \
               "- Remove task: <task>\n" \
               "- Set reminder: <time> for <event>\n" \
               "- Weather in <location>\n" \
               "- Translate: <text> to <language>\n" \
               "- Define <word>\n" \
               "- Search: <query>\n" \
               "- Tell me a joke\n" \
               "- My name is <name>\n" \
               "- My favorite color is <color>"

    elif message.startswith("ask a question"):
        question = message.split(":")[1].strip()
        return get_answer_to_question(question)

    elif message.startswith("calculate"):
        try:
            expression = message.split(":")[1].strip()
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

    elif message.startswith("add task"):
        task = message.split(":")[1].strip()
        todo_list[task] = False
        return f"Task '{task}' added to the to-do list."

    elif message.startswith("view tasks"):
        if not todo_list:
            return "No tasks in the to-do list."
        else:
            tasks = "\n".join(todo_list.keys())
            return f"Tasks in the to-do list:\n{tasks}"

    elif message.startswith("remove task"):
        task = message.split(":")[1].strip()
        if task in todo_list:
            del todo_list[task]
            return f"Task '{task}' removed from the to-do list."
        else:
            return f"Task '{task}' not found in the to-do list."

    elif message.startswith("set reminder"):
        try:
            event = message.split("for")[1].strip()
            reminders[event] = False
            return f"Reminder set for '{event}'."
        except Exception as e:
            return f"Error setting the reminder: {str(e)}"

    elif message.startswith("weather in"):
        location = message.split("weather in")[1].strip()
        return get_weather_info(location)

    elif message.startswith("translate"):
        translation_request = message.split(":")[1].strip()
        return translate_text(translation_request)

    elif message.startswith("define"):
        word = message.split(":")[1].strip()
        return get_word_definition(word)

    elif message.startswith("search"):
        query = message.split(":")[1].strip()
        return search_web(query)

    elif message.lower() == "tell me a joke":
        return get_random_joke()

    elif message.startswith("my name is"):
        user_name = message.split("is")[1].strip()
        user_info["name"] = user_name
        return f"Nice to meet you, {user_name}!"

    elif message.startswith("my favorite color is"):
        favorite_color = message.split("is")[1].strip()
        user_info["color"] = favorite_color
        return f"Got it! Your favorite color is {favorite_color}."

  
    response = openai.ChatCompletion.create(
        model="text-davinci-002",  
        messages=[
            {"role": "system", "content": "You are a Personal Assistant."},
            {"role": "user", "content": message},
        ]
    )
    return response['choices'][0]['message']['content']

def get_answer_to_question(question):
    if question in knowledge_base:
        return knowledge_base[question]
    else:
        return "I'm sorry, I don't know the answer to that question."

def get_weather_info(location):
   
    api_key = "YOUR_WEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            temperature_celsius = temperature - 273.15
            return f"The weather in {location} is currently {weather_description} with a temperature of {temperature_celsius:.2f}°C."
        else:
            return "Weather information not available for the specified location."
    except Exception as e:
        return f"Error fetching weather information: {str(e)}"

def translate_text(translation_request):
   
    api_key = "YOUR_TRANSLATION_API_KEY"
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}&q={translation_request}"

    try:
        response = requests.get(url)
        data = response.json()
        if "data" in data and "translations" in data["data"]:
            translated_text = data["data"]["translations"][0]["translatedText"]
            return f"Translation: {translated_text}"
        else:
            return "Translation not available for the specified text."
    except Exception as e:
        return f"Error translating text: {str(e)}"

def get_word_definition(word):
  
    api_key = "YOUR_DICTIONARY_API_KEY"
    url = f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            definition = data[0].get("shortdef")
            if definition:
                return f"Definition of '{word}': {', '.join(definition)}"
        return f"Definition of '{word}' not found in the dictionary."
    except Exception as e:
        return f"Error fetching word definition: {str(e)}"

def search_web(query):

    api_key = "YOUR_SEARCH_ENGINE_API_KEY"
    search_engine_id = "YOUR_SEARCH_ENGINE_ID"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"

    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            top_result = data["items"][0]
            title = top_result["title"]
            link = top_result["link"]
            snippet = top_result["snippet"]
            return f"Top result:\n{title}\n{link}\n{snippet}"
        else:
            return "No results found."
    except Exception as e:
        return f"Error searching the web: {str(e)}"

def get_random_joke():

    url = "YOUR_JOKES_API_URL"

    try:
        response = requests.get(url)
        data = response.json()
        if "joke" in data:
            return data["joke"]
        else:
            return "Why did the chicken cross the road? To get to the other side!"
    except Exception as e:
        return f"Error fetching a joke: {str(e)}"



@app.route('/handle_messages', methods=['POST'])

def handle_messages(messages):
    response_msgs = []
    for msg in messages:
        user_message = msg['content']
        bot_response = handle_message(user_message)
        response_msgs.append({"role": "assistant", "content": bot_response})
    return response_msgs


if __name__ == "__main__":
    app.run(debug=True)
