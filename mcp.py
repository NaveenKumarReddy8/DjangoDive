import subprocess
from langchain_aws.chat_models import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.runnables.subprocess import Subprocess
from langchain_core.runnables import RunnablePassthrough

# 1. Initialize ChatBedrock
bedrock_chat = ChatBedrock(model_id="anthropic.claude-v2")  # Replace with your desired model ID

# 2. Define the command to run your MCP Server (STDIO)
mcp_server_command = ["python", "/path/to/your/mcp_server_stdio.py"]  # Replace with your actual command

# 3. Create a Subprocess instance for the MCP Server
mcp_subprocess = Subprocess(cmd=mcp_server_command)

# 4. Define the chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("human", "{input_text}")
])

# 5. Create the Langchain chain that uses Bedrock and then the MCP Server
chain = (
    {"input_text": RunnablePassthrough()}
    | prompt
    | bedrock_chat
    | StrOutputParser()
    | mcp_subprocess  # Pass the Bedrock output to the MCP Server's stdin
    | StrOutputParser() # Parse the MCP Server's stdout
)

# 6. Run the chain with some input
input_data = "Explain the concept of artificial intelligence in simple terms."
output = chain.invoke({"input_text": input_data})

print(f"Input: {input_data}")
print(f"Bedrock Response (potentially processed by MCP Server via STDIO):\n{output}")
