import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy:
    print(proxy.connection())


def append_to_topic(text):
    print("Available topics:")
    topics = proxy.get_all_topics()
    for topic in topics:
        print(topic)
    chosen_topic = input("Write name of the topic you want to append the text")
    print(proxy.add_note(chosen_topic, "Wikipedia", text))


def get_wikipedia_summary(topic):
    text = proxy.get_wikipedia_summary(topic)
    print(text)
    print("Do you want to add this to an existing topic")
    append_choice = input("Yes or No: ")
    if append_choice == "Yes" or append_choice == "yes":
        append_to_topic(text)
    elif append_choice == "No" or append_choice == "no":
        return
    else:
        print("Not a correct input.")


def add_note(topic, name, text):
    print(proxy.add_note(topic, name, text))


def get_note(topic):
    print(proxy.get_note(topic))


def main():
    while True:
        print("1: Add a note")
        print("2: Get a note")
        print("3: Get information from wikipedia")
        print("0: Quit")
        try:
            choice = int(input("Choice: "))

            if choice == 1:
                topic = input("Topic: ")
                name = input("Note Name: ")
                text = input("Additional Information: ")
                add_note(topic, name, text)
            elif choice == 2:
                topic = input("Topic: ")
                get_note(topic)
            elif choice == 3:
                topic = input("Enter a topic to search on Wikipedia: ")
                get_wikipedia_summary(topic)
            elif choice == 0:
                break
            else:
                print("Please pick 1, 2, or 0.")

        except Exception as e:
            print("Please pick 1, 2, or 0.")

main()

