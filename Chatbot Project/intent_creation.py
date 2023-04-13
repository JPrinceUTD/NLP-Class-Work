import wikipedia
import json

if __name__ == "__main__":
    # Get topic to add
    topic = "Home Insurance Building"

    # Get summary of given topic
    summary = wikipedia.summary(topic)

    # Open intents JSON file
    with open('intents.json') as f:
        data = json.load(f)

    # Get intents JSON array
    intents = data["intents"]

    # Append summary to intents array
    intents.append({
        "tag": topic.lower(),
        "patterns": ["What is " + topic.lower(), topic.lower(), "Tell me about " + topic.lower()],
        "responses": [summary],
        "context": ""
    })

    # Create new JSON file
    with open('intents.json', 'w') as f:
        json.dump(data, f, indent=2)

    # Closing file
    f.close()
