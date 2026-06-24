import os
import json
import time
import datetime
from google import genai
from google.genai import types

def generate_models_json():
    # 1. Authenticate with the Gemini API
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: GEMINI_API_KEY environment variable not set.")
    
    client = genai.Client(api_key=api_key)
    
    # 2. Call Gemini with application/json mime type
    prompt = """
    Create a JSON array of the top 10 AI models currently driving autonomous agent reasoning, long-context ingestion, and complex tool-use workflows in 2026.
    Include these exact models:
    1. Claude 3.5 Sonnet
    2. GPT-4o
    3. Gemini 1.5 Pro
    4. DeepSeek-V3
    5. Llama 3.1 405B
    6. Qwen 2.5 72B
    7. Mistral Large 2
    8. Claude 4.8 Opus (Next-Gen)
    9. GPT-5.5 (Next-Gen)
    10. DeepSeek-R1

    For each model, output an object with these fields:
    - name: string (e.g. "Claude 3.5 Sonnet")
    - category: string ("proprietary" or "open")
    - creator: string (e.g. "Anthropic", "OpenAI", "Google", "DeepSeek", "Meta", "Alibaba", "Mistral")
    - description: string (a concise paragraph describing its agentic strengths, developer adoption, and features)
    - contextWindow: string (e.g. "200K tokens", "128K tokens", "2,000,000 tokens", "1,000,000 tokens")
    - contextValue: number (raw context token limit as number, e.g. 200000, 128000, 2000000, 1000000)
    - primaryStrength: string (e.g. "Coding & Reasoning", "Speed & Tool Integration", "Repository Ingestion", "Logical Reasoning & Cost", "On-Premise Flagship", "Deep Autonomous Tasks", "Reasoning & Coding", "Multilingual Efficiency")
    - sweBench: number (SWE-bench verified coding score as percentage from 0 to 100. Use actual or estimated values: GPT-5.5: 58.0, Claude 3.5 Sonnet: 49.0, DeepSeek-R1: 48.7, DeepSeek-V3: 42.0, GPT-4o: 38.8, Claude 4.8 Opus: 35.0, Gemini 1.5 Pro: 27.0, Llama 3.1 405B: 23.0, Qwen 2.5 72B: 21.0, Mistral Large 2: 20.0)
    - gpqa: number (GPQA Diamond reasoning score as percentage from 0 to 100. Use actual or estimated values: GPT-5.5: 75.0, DeepSeek-R1: 71.0, DeepSeek-V3: 59.1, Claude 3.5 Sonnet: 65.0, GPT-4o: 49.9, Claude 4.8 Opus: 55.0, Gemini 1.5 Pro: 46.2, Llama 3.1 405B: 51.1, Qwen 2.5 72B: 45.0, Mistral Large 2: 38.0)
    - humanEval: number (HumanEval Python coding score as percentage from 0 to 100. Use actual or estimated values: GPT-5.5: 95.0, DeepSeek-R1: 92.8, Claude 3.5 Sonnet: 92.0, GPT-4o: 90.2, Llama 3.1 405B: 89.0, Claude 4.8 Opus: 88.0, Qwen 2.5 72B: 86.6, Gemini 1.5 Pro: 84.1, DeepSeek-V3: 82.6, Mistral Large 2: 73.0)
    - costPerMillion: number (blended input/output price in dollars per 1 million tokens, e.g. DeepSeek-V3: 0.20, Qwen 2.5 72B: 0.40, DeepSeek-R1: 0.55, Llama 3.1 405B: 2.66, Mistral Large 2: 3.00, Gemini 1.5 Pro: 3.50, GPT-4o: 4.00, Claude 3.5 Sonnet: 4.50, GPT-5.5: 6.00, Claude 4.8 Opus: 15.00)
    - costLabel: string (e.g. "$0.20", "$4.50", "$15.00")
    - color: string (Tailwind CSS gradient color classes, choose from:
        - "from-blue-500 to-cyan-500" for Claude 3.5 Sonnet/Opus
        - "from-emerald-500 to-teal-500" for GPT-4o
        - "from-indigo-500 to-purple-500" for Gemini 1.5 Pro
        - "from-purple-500 to-indigo-500" for DeepSeek-V3/R1
        - "from-purple-500 to-pink-500" for Llama 3.1
        - "from-purple-500 to-blue-500" for Qwen 2.5
        - "from-pink-500 to-rose-500" for Mistral Large 2
        - "from-blue-500 to-indigo-500" for GPT-5.5)
    
    Ensure the output is valid JSON. Return ONLY the raw JSON array.
    """

    print("Generating models intelligence data...")
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
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
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

    # 3. Write data to a local file in the workspace
    output_path = os.path.join(os.path.dirname(__file__), "top_10_models.json")
    
    # Verify we got valid JSON back
    try:
        data = json.loads(response.text)
        
        # Inject last_updated timestamp to the first model object to force Git updates
        if isinstance(data, list) and len(data) > 0:
            data[0]["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Successfully wrote top 10 models intelligence to: {output_path}")
    except json.JSONDecodeError:
        print("ERROR: Gemini returned invalid JSON. Saving raw text to error log.")
        with open(os.path.join(os.path.dirname(__file__), "error.log"), "w") as f:
            f.write(response.text)
        # Raise error to trigger runner failure on bad JSON
        raise ValueError("Invalid JSON returned by Gemini API.")

if __name__ == "__main__":
    generate_models_json()
