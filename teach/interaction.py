def discuss(topic) :
    """Discuss a topic with the user and return their response.

    Ask if the user likes the topic and why.

    Parameters:
        topic (str): The topic under discussion.

    Return:
        str: Response to the question of why they like the topic.
    """
    like = input("Do you like " + topic + "? ")
    response = input("Why do you think that? ")
    return response


# Greet the user.
name = input("What is your name? ")
if name == "Tim" :
    print("Greetings, Tim the Enchanter")
elif name == "Brian" :
    print("Bad luck, Brian")
else :
    print("Hello " + name + ".")

discuss("university")
print("That's very interesting.")

# Ask for topics to discuss.
while True :
    topic = input("What do you want to talk about? ")
    if topic == "nothing" :
        break
    response = discuss(topic)
    print("I also think that", response)

# Exit when the user stops coming up with topics
print("Okay. Goodbye, " + name + "!")
