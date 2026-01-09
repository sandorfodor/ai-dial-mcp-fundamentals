# Framework-based MCP (Server & Client)
Python implementation for building Users Management Agent with MCP tools and MCP server

Create .env based on the .env.example in the task folder.

### Build & Run


#### Server

```bash
docker build -f Dockerfile.server -t python-docker-server .;docker run -it --rm --network ai-dial-mcp-fundamentals_my-network python-docker-server
```

#### Agent
```bash
docker build -f  Dockerfile.agent -t python-docker-agent .;docker run -it --rm --network ai-dial-mcp-fundamentals_my-network python-docker-agent
```