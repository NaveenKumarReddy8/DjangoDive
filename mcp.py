import subprocess
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.runnables.subprocess import Subprocess

# 1. Define the command to run your MCP Server
mcp_server_command = ["python", "/path/to/your/mcp_server.py"]  # Replace with your actual command

# 2. Define the prompt template for the input you want to send
prompt_template = """Process the following text using your MCP Server:

Text: {input_text}
"""
prompt = PromptTemplate.from_template(prompt_template)

# 3. Create a Subprocess instance
subprocess_runnable = Subprocess(cmd=mcp_server_command)

# 4. Create a Langchain chain
chain = (
    {"input_text": RunnablePassthrough()}
    | prompt
    | subprocess_runnable
    | StrOutputParser()
)

# 5. Run the chain with some input
input_data = "This is some text I want to send to the MCP Server via STDIO."
output = chain.invoke(input_data)

print(f"Input: {input_data}")
print(f"MCP Server Response (via STDIO):\n{output}")
