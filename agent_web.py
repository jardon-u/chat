"""Agent that can fetch and summarize any URL"""
import boto3, json, requests
from bs4 import BeautifulSoup

client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL = "global.anthropic.claude-opus-4-5-20251101-v1:0"
TOOLS = json.load(open("tools_web.json"))

def llm(messages):
    r = client.converse(modelId=MODEL, messages=messages, toolConfig={"tools": TOOLS})
    return r["output"]["message"], r["stopReason"]

def fetch_url(url):
    html = requests.get(url, timeout=10).text
    return BeautifulSoup(html, 'html.parser').get_text()[:8000]

def agent(prompt):
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    while True:
        response, stop = llm(messages)
        if stop != "tool_use": return response["content"][0]["text"]
        tools = [c["toolUse"] for c in response["content"] if "toolUse" in c]
        results = [{"toolResult": {"toolUseId": t["toolUseId"], "content": [{"text": fetch_url(t["input"]["url"])}]}} for t in tools]
        messages += [response, {"role": "user", "content": results}]

if __name__ == "__main__":
    print(agent("Summarize https://en.wikipedia.org/wiki/Artificial_intelligence"))
