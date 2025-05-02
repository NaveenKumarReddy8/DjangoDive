"""
# .env file
AZURE_OPENAI_ENDPOINT="YOUR_BASE_URL" # e.g., https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION="YOUR_API_VERSION" # e.g., 2024-02-01 or 2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME" # Your specific model deployment name
AZURE_TENANT_ID="YOUR_TENANT_ID"
AZURE_CLIENT_ID="YOUR_CLIENT_ID"
AZURE_CLIENT_CERTIFICATE_PATH="/path/to/your/certificate.pem" # Absolute or relative path to your .pem file
# Optional: If your PEM file is password protected
# AZURE_CLIENT_CERTIFICATE_PASSWORD="YOUR_PEM_PASSWORD"
"""



import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import ClientCertificateCredential, get_bearer_token_provider
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Load credentials from .env file
load_dotenv()

# --- Method 1: Direct AzureOpenAI Client Configuration (for testing/understanding) ---
# This shows how to configure the client directly. You might not pass this
# exact client instance to ADK, but the credential setup is the same basis.

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
certificate_path = os.getenv("AZURE_CLIENT_CERTIFICATE_PATH")
certificate_password = os.getenv("AZURE_CLIENT_CERTIFICATE_PASSWORD") # Optional

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not all([tenant_id, client_id, certificate_path, azure_openai_endpoint, api_version, deployment_name]):
    raise ValueError("One or more required environment variables are missing.")

try:
    # 1. Create the Certificate Credential
    # If you have a password for your PEM file, include password=certificate_password
    credential_options = {"password": certificate_password} if certificate_password else {}
    cert_credential = ClientCertificateCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        certificate_path=certificate_path,
        **credential_options
    )

    # 2. Create the token provider for the OpenAI client
    # The scope "https://cognitiveservices.azure.com/.default" is standard for Azure OpenAI
    token_provider = get_bearer_token_provider(
        cert_credential, "https://cognitiveservices.azure.com/.default"
    )

    # 3. Initialize the AzureOpenAI client with AAD authentication
    direct_azure_client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_version=api_version,
        azure_ad_token_provider=token_provider,
        # deployment_name is usually passed during the actual API call (e.g., client.chat.completions.create)
    )

    print("Successfully configured direct AzureOpenAI client with certificate credentials.")

    # --- Example: Test the direct client (Optional) ---
    # print(f"Making a test call to deployment: {deployment_name}")
    # response = direct_azure_client.chat.completions.create(
    #     model=deployment_name, # Specify the deployment name here
    #     messages=[{"role": "user", "content": "What is Azure OpenAI?"}],
    #     max_tokens=100
    # )
    # print("Test call successful:", response.choices[0].message.content)

except Exception as e:
    print(f"Error configuring or testing direct Azure OpenAI client: {e}")
    direct_azure_client = None # Ensure client is None if setup fails

# --- Method 2: Integration with Google ADK via LiteLLM ---
# ADK typically uses LiteLLM, which relies heavily on environment variables.
# Ensure the required environment variables are set (as loaded from .env above).
# LiteLLM, if using DefaultAzureCredential internally, should pick up:
# AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_CERTIFICATE_PATH,
# AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION (or AZURE_OPENAI_API_VERSION)

# Note: LiteLLM expects the model name in the format "azure/<your_deployment_name>"
lite_llm_model_string = f"azure/{deployment_name}"

print(f"\nConfiguring Google ADK LlmAgent with LiteLLM model: {lite_llm_model_string}")
print("Expecting LiteLLM to use Azure AD Certificate Auth via environment variables:")
print(f"  AZURE_TENANT_ID: {tenant_id}")
print(f"  AZURE_CLIENT_ID: {client_id}")
print(f"  AZURE_CLIENT_CERTIFICATE_PATH: {certificate_path}")
print(f"  AZURE_OPENAI_ENDPOINT: {azure_openai_endpoint}")
print(f"  AZURE_OPENAI_API_VERSION: {api_version}") # Or OPENAI_API_VERSION might be needed by LiteLLM

try:
    # Configure the ADK Agent to use Azure via LiteLLM
    # ADK/LiteLLM should handle the authentication based on the environment variables
    azure_agent = LlmAgent(
        model=LiteLlm(
            model=lite_llm_model_string,
            # You might need to explicitly pass api_version and base_url if env vars aren't picked up
            api_base=azure_openai_endpoint,
            api_version=api_version
            # LiteLLM has parameters for azure specific auth but check its docs
            # for the most up-to-date way to force certificate auth if env vars fail.
        ),
        name="my_azure_cert_agent",
        instruction="You are a helpful AI assistant running on Azure OpenAI, authenticated via client certificate.",
        description="An agent that uses Azure OpenAI with certificate authentication."
        # Add other agent parameters as needed (tools, etc.)
    )

    print("Successfully configured ADK LlmAgent.")

    # Now you can use 'azure_agent' within your ADK application (e.g., in a Runner)
    # Example (conceptual - needs ADK runner setup):
    # async def run_agent():
    #     from google.adk.runners import Runner
    #     from google.adk.sessions import SessionService
    #     runner = Runner(agent=azure_agent, session_service=SessionService())
    #     async for event in runner.run("Tell me about Google ADK."):
    #         print(event)
    # import asyncio
    # asyncio.run(run_agent())

except Exception as e:
    print(f"Error configuring ADK LlmAgent: {e}")
    print("Please ensure all required environment variables are set correctly and LiteLLM supports this auth flow via environment variables.")
    print("Check LiteLLM documentation for specific Azure AD certificate authentication parameters if needed.")
