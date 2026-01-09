import asyncio
import json
import os
from dotenv import load_dotenv
load_dotenv()

from mcp import Resource
from mcp.types import Prompt

from agent.mcp_client import MCPClient
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

async def main():
    # 1. Create MCP client and open connection to the MCP server
    mcp_server_url = "http://mcp-server:8005/mcp"
    
    async with MCPClient(mcp_server_url) as mcp_client:
        # 2. Get Available MCP Resources and print them
        print("\n=== Available MCP Resources ===")
        resources = await mcp_client.get_resources()
        for resource in resources:
            print(f"  - {resource.uri}: {resource.name}")
        
        # 3. Get Available MCP Tools, assign to tools variable, print them
        print("\n=== Available MCP Tools ===")
        tools = await mcp_client.get_tools()
        for tool in tools:
            print(f"  - {tool['function']['name']}: {tool['function']['description']}")
        
        # 4. Create DialClient
        api_key = os.getenv("DIAL_API_KEY", "")
        endpoint = os.getenv("DIAL_ENDPOINT", "")
        
        if not api_key or not endpoint:
            print("\n⚠️  Warning: DIAL_API_KEY and DIAL_ENDPOINT environment variables not set!")
            print("Please set them to use the agent.\n")
            return
        
        dial_client = DialClient(
            api_key=api_key,
            endpoint=endpoint,
            tools=tools,
            mcp_client=mcp_client
        )
        
        # 5. Create list with messages and add SYSTEM_PROMPT
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]
        
        # 6. Add Prompts from MCP server as User messages
        print("\n=== Loading MCP Prompts ===")
        prompts = await mcp_client.get_prompts()
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description}")
            prompt_content = await mcp_client.get_prompt(prompt.name)
            messages.append(Message(role=Role.USER, content=f"[System Guidance - {prompt.name}]\n{prompt_content}"))
        
        # 7. Create console chat
        print("\n" + "="*60)
        print("🎯 User Management Agent")
        print("="*60)
        print("Type your questions or commands. Type 'exit' or 'quit' to end.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Add user message
                messages.append(Message(role=Role.USER, content=user_input))
                
                # Get completion from dial client
                response = await dial_client.get_completion(messages)
                
                # Add AI response to history
                messages.append(response)
                print()  # Extra line for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")



asyncio.run(main())
