import os
import openai

#Initialize a client
client = openai.OpenAI(api_key=openai_api_key) 



my_file = client.files.create(
  file=open("sample.pdf", "rb"),
  purpose='assistants'
)
print(f"This is the file object: {my_file} \n")


# Step 2: Create an Assistant
my_assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo-1106",
    instructions="You are a FINANCE ANALYST. Use your knowledge base to best respond to FINANCE queries.",
    name="FINANCE ANALYST",
    tools=[{"type": "retrieval"}]
)
print(f"This is the assistant object: {my_assistant} \n")


my_thread = client.beta.threads.create()
print(f"This is the thread object: {my_thread} \n")



# Step 4: Add a Message to a Thread
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content="What can I buy in your online store?",
  file_ids=[my_file.id]
)
print(f"This is the message object: {my_thread_message} \n")


# Step 5: Run the Assistant

PROMPT = """In the given finance document we need to extract the following information:
            - key data requirement
            - key rules and regulations along with the source and description 
            - action required for the compliance"""
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id,
  instructions=PROMPT
)
print(f"This is the run object: {my_run} \n")


# Step 6: Periodically retrieve the Run to check on its status to see if it has moved to completed
while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")

        # Step 7: Retrieve the Messages added by the Assistant to the Thread
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )

        print("------------------------------------------------------------ \n")

        print(f"User: {my_thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")

        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
        break
