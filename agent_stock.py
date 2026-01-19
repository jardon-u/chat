"""Agent that can fetch stock prices"""
import boto3, json, requests

client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL = "global.anthropic.claude-opus-4-5-20251101-v1:0"
TOOLS = json.load(open("tools_stock.json"))

def llm(messages):
    r = client.converse(modelId=MODEL, messages=messages, toolConfig={"tools": TOOLS})
    return r["output"]["message"], r["stopReason"]

def get_stock(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    return f"{symbol}: ${price}"

def agent(prompt):
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    while True:
        response, stop = llm(messages)
        if stop != "tool_use": return response["content"][0]["text"]
        tools = [c["toolUse"] for c in response["content"] if "toolUse" in c]
        results = [{"toolResult": {"toolUseId": t["toolUseId"], "content": [{"text": get_stock(t["input"]["symbol"])}]}} for t in tools]
        messages += [response, {"role": "user", "content": results}]

if __name__ == "__main__":
    print(agent("What's the current price of NVIDIA and Apple? Which one is higher?"))
