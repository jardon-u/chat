"""Agent that can run shell commands"""
import boto3, json, subprocess

client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL = "global.anthropic.claude-opus-4-5-20251101-v1:0"
TOOLS = json.load(open("tools_shell.json"))

def llm(messages):
    r = client.converse(modelId=MODEL, messages=messages, toolConfig={"tools": TOOLS})
    return r["output"]["message"], r["stopReason"]

def run_shell(cmd):
    print(f"\n> {cmd}")
    if input("Run? [y/N] ").lower() != 'y':
        return "Command rejected by user"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout or "Done"

def agent(prompt):
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    while True:
        response, stop = llm(messages)
        if stop != "tool_use": return response["content"][0]["text"]
        tools = [c["toolUse"] for c in response["content"] if "toolUse" in c]
        results = [{"toolResult": {"toolUseId": t["toolUseId"], "content": [{"text": run_shell(t["input"]["command"])}]}} for t in tools]
        messages += [response, {"role": "user", "content": results}]

if __name__ == "__main__":
    print(agent("List all python files in the current directory and count them"))
