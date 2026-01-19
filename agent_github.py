"""Agent that can search GitHub code"""
import boto3, json, requests

client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL = "global.anthropic.claude-opus-4-5-20251101-v1:0"
TOOLS = json.load(open("tools_github.json"))

def llm(messages):
    r = client.converse(modelId=MODEL, messages=messages, toolConfig={"tools": TOOLS})
    return r["output"]["message"], r["stopReason"]

def search_github(query):
    url = f"https://api.github.com/search/code?q={query}&per_page=5"
    data = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}).json()
    return "\n".join(f"- {item['repository']['full_name']}: {item['path']}" for item in data.get("items", []))

def agent(prompt):
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    while True:
        response, stop = llm(messages)
        if stop != "tool_use": return response["content"][0]["text"]
        tools = [c["toolUse"] for c in response["content"] if "toolUse" in c]
        results = [{"toolResult": {"toolUseId": t["toolUseId"], "content": [{"text": search_github(t["input"]["query"])}]}} for t in tools]
        messages += [response, {"role": "user", "content": results}]

if __name__ == "__main__":
    print(agent("Find examples of Python code using AWS Bedrock converse API"))
