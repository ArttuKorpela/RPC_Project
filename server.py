from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

tree = ET.parse('test.xml')
root = tree.getroot()
port = 8001


class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def add_note(topic_name, note_name, text):
    try:
        # Find the topic or create it if it doesn't exist
        topic = root.find(f".//topic[@name='{topic_name}']")
        if topic is None:
            topic = ET.SubElement(root, 'topic', name=topic_name)

        # Create a new note with name and add text and timestamp
        note = ET.SubElement(topic, 'note', name=note_name)
        text_element = ET.SubElement(note, 'text')
        text_element.text = text
        timestamp_element = ET.SubElement(note, 'timestamp')
        timestamp_element.text = datetime.now().strftime("%m/%d/%y - %H:%M:%S")

        tree.write('test.xml')
        return "Success"
    except Exception as e:
        return "Error in adding topic"


def get_note(topic_name):
    topic = root.find(f".//topic[@name='{topic_name}']")
    if topic is not None:
        notes = topic.findall(".//note")
        # Prepare a list to hold note details
        notes_details = []
        for note in notes:
            # Extract the note's name, text, and timestamp
            note_name = note.get('name')  # Get the 'name' attribute of the note
            note_text = note.find('text').text if note.find('text') is not None else "No text"
            note_timestamp = note.find('timestamp').text if note.find('timestamp') is not None else "No timestamp"
            # Append a formatted string for each note to the details list
            notes_details.append(f"Name: {note_name}, Text: {note_text}, Timestamp: {note_timestamp}")
        # Join all note details into a single string to return
        return "\n".join(notes_details) if notes_details else "No notes found"
    return "No such note"


def get_wikipedia_summary(topic):
    wikipedia_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        response = requests.get(wikipedia_api_url)
        if response.status_code == 200:
            data = response.json()
            return data['extract']
        else:
            return "Failed to retrieve information"
    except Exception as e:
        return "Error in adding topic"

def get_all_topics():
    topics = root.findall(".//topic")
    topic_names = [topic.get('name') for topic in topics]
    return topic_names


def connection():
    return "Connected successfully"


server = ThreadedXMLRPCServer(("localhost", port))
print(f"Listening on {port}")

server.register_function(add_note, "add_note")
server.register_function(get_note, "get_note")
server.register_function(get_wikipedia_summary, "get_wikipedia_summary")
server.register_function(get_all_topics, "get_all_topics")
server.register_function(connection, "connection")

server.serve_forever()
