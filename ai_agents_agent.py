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

    print("Generating agents registry data...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    output_path = os.path.join(os.path.dirname(__file__), "top_10_agents.md")
    
    # Save the text directly
    with open(output_path, "w") as f:
        f.write(response.text.strip())
    
    print(f"Successfully wrote top 10 agents markdown to: {output_path}")

if __name__ == "__main__":
    generate_agents_markdown()
