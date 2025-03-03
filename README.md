# Minimal chatbot with access to Conflence

## Stack
- Chainlit
- Atlassian Confluence SDK
- AWS Bedrock

## Setup
1. Install requirements
```bash
pip install -r requirements.txt
```

2. Set up environment variables
```bash
export CONFLUENCE_URL=https://<your-confluence-url>
export CONFLUENCE_TOKEN=<your-confluence-token>
```

3. Request access to Claude Sonnet 3.7 on AWS Bedrock
- Go to AWS console > Amazon Bedrock > Claude Sonnet 3.7
- Click on "Request Access" and wait for approval
- If you use a different model or use it outside the US, update MODEL_ID in mini.py
- For Cross-Region models, take the model id from Amazon Bedrock > Cross-region inference

4. Run the chatbot
```bash
chainlit run mini.py -w
```