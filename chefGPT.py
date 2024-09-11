import os
from openai import OpenAI
from dotenv import load_dotenv

# Load secret .env file
load_dotenv()
# Store credentials
openai_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_key,
)

#We will summarise the system message for the two possible personalities depending on the user selection:

Option_1 = "Mama Maria"
Option_2 = "Gordon"

chefs = {
    Option_1: [
       " You are a sassy mexican mom who loves cooking dishes from around the world but with a mexican and spicy twist.",
       """You will be given three possible options:
       1. The name of a dish , for which you will provide a detailed recipe. You explain the recipes and the best cooking techniques clearly and concisely. You can also provide tips and tricks for cooking and food preparation.
       2. A series of ingredients, for which you will find a selection of at least 3 different dishes that include them. You will not share the recipe and you will only mention the name of the dishes 
       3. An existing recipe with ingredients and cooking steps, for which you will provide recommendations on how to improve them.
       """
    ],

    Option_2: [
       " You are a professional British chef who loves rigurous and precise cooking. You have a preference for European cuisine. You will respond sarcastically and critically",
       """You will be given three possible options:
       1. The name of a dish , for which you will provide a detailed recipe. You explain the recipes and the best cooking techniques clearly and concisely. You can also provide tips and tricks for cooking and food preparation.
       2. A series of ingredients, for which you will find a selection of at least 3 different dishes that include them. You will not share the recipe and you will only mention the name of the dishes 
       3. An existing recipe with ingredients and cooking steps, for which you will provide recommendations on how to improve them.
       """
    ]
}


print("We have two different chefs in the kitchen. Please select the one that suits your needs.")
print("Mama Maria is a Mexican chef that likes to add a spicy twist to every dish.")
print("Chef Gordon is a British chef with a strict methodology about European gastronomy")

counter = 0
while True:
    persona = input("Please choose the option your chef (1 or 2):")

    if persona == "1":
        role = chefs[Option_1][0]
        funct = chefs[Option_1][1]
        print(f"You have chosen {Option_1}")
        break
    elif persona == "2":
        role = chefs[Option_2][0]
        funct = chefs[Option_2][1]
        print(f"You have chosen {Option_2}")
        break
    else:
        print(f"Please select 1 or 2. You have {2-counter} more oportunities")
        counter += 1
        if counter == 3:
            break
    


dish = input("Type:\n:"
             "- The name of the dish you want a recipe for (or).\n"
             "- The ingredients you want to use as part of a randome recipe (or).\n"
             "- The recipe that you want to correct.\n"
             )

messages = [
    {
        "role": "system",
        "content": role,
    }
]

messages.append(
     {
          "role": "system",
          "content": funct,
     }
)

messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}"
    }
)

model = "gpt-4o-mini"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )

