def __init__(self):
    self.mcp = MCPServer()

    self.mcp.register_tool(
        "rag_tool",
        "Use knowledge base retrieval for system design questions",
        self.handle_rag
    )

    self.mcp.register_tool(
        "code_tool",
        "Generate backend production code",
        generate_code
    )

    self.mcp.register_tool(
        "architecture_tool",
        "Provide detailed system design explanation",
        explain_architecture
    )