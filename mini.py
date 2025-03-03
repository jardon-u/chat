import chainlit as cl
import boto3, os, json
from atlassian import Confluence

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
SYSTEM_PROMPT = """You are Arlo helpful assistant. You can retrieve information from Confluence.
After receiving tool results, do not request another tool call. Reply using short answers."""
TOOL_LIST = json.load(open("claude-config.json"))

confluence_client = Confluence(
    url=os.getenv('CONFLUENCE_URL'),
    token=os.getenv('CONFLUENCE_TOKEN'),
)

def converse(messages):
    response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=messages,
        system=[{"text": SYSTEM_PROMPT}],
        toolConfig={"tools": TOOL_LIST}
    )
    return response.get("output", {}).get("message", {})

@cl.step(type="tool")
async def confluence_search(cql, max_results=10) -> str:
    return str(confluence_client.cql(cql, limit=max_results, expand='content.body.view'))

async def process_tools(response_message, bedrock_messages):
    tools_results = []
    for content_block in response_message.get("content", []):
        tool_use_block = content_block.get("toolUse", {})
        if tool_use_block.get("name") == "confluence":
            query = tool_use_block["input"]["cql"]
            tools_results.append({ "toolResult": {
                "toolUseId": tool_use_block["toolUseId"],
                "content": [{"text": await confluence_search(query)}]
            }})
    if tools_results:
        bedrock_messages.extend([response_message, {"role": "user", "content": tools_results}])
        tools_response = converse(bedrock_messages)
        tools_reponse_text = tools_response.get("content", [{}])[0].get("text")
        await cl.Message(content=tools_reponse_text).send()

@cl.on_message
async def on_message(user_message: cl.Message):
    bedrock_messages = [{"role": "user", "content": [{"text": user_message.content}]}]
    response_message = converse(bedrock_messages)
    await cl.Message(content=response_message.get("content", [{}])[0].get("text")).send()
    await process_tools(response_message, bedrock_messages)
