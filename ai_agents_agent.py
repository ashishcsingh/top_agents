import os
from google import genai

def generate_agents_markdown():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: GEMINI_API_KEY environment variable not set.")
    
    client = genai.Client(api_key=api_key)
    
    prompt = """
    Create a clean markdown list of the top 10 AI agents, multi-agent frameworks, and autonomous software platforms driving development in 2026.
    Include these exact leading agents and frameworks:
    1. Devin (Cognition AI)
    2. CrewAI
    3. LangGraph (LangChain)
    4. Microsoft AutoGen
    5. Anthropic Computer Use
    6. Smolagents (Hugging Face)
    7. OpenAI Operator
    8. Multi-On
    9. Agency Swarm
    10. Camel-AI
    
    Format the output EXACTLY like this for each entry, with NO bullet points, no extra bolding, and no markdown code-block wrapping the response.
    Example entry:
    ## Devin (Cognition AI)
    https://www.cognition.ai/blog/devin
    The world's first fully autonomous AI software engineer, capable of planning, coding, executing, and debugging entire projects from a single prompt within a secure sandbox.
    
    Ensure each agent block has:
    - Line 1: `## [Agent/Framework Name]`
    - Line 2: The exact URL (must be valid, no markdown link syntax, just plain text URL)
    - Line 3: A concise single-paragraph description explaining its agentic architecture, tool integration, or capabilities.
    
    Return ONLY the raw markdown text. Do not wrap it in ```markdown ``` code blocks. Do not add any introduction or conclusion text.
    """

    import time
    print("Generating agents registry data...")
    max_retries = 3
    retry_delay = 5
    response = None
    last_exception = None

    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-flash-latest"
    ]

    for model_name in models_to_try:
        print(f"Attempting model: {model_name}...")
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                break
            except Exception as e:
                print(f"Model {model_name} (Attempt {attempt}/{max_retries}) failed with error: {str(e)}")
                last_exception = e
                if attempt == max_retries:
                    break
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                
        if response:
            print(f"SUCCESS: Generated content using model '{model_name}'.")
            break

    if not response:
        print("CRITICAL: All models and fallbacks failed to generate content.")
        raise last_exception

    output_path = os.path.join(os.path.dirname(__file__), "top_10_agents.md")
    
    # Save the text directly
    with open(output_path, "w") as f:
        f.write(response.text.strip())
    
    print(f"Successfully wrote top 10 agents markdown to: {output_path}")

if __name__ == "__main__":
    generate_agents_markdown()
