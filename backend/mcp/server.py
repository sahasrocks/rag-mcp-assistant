class MCPServer:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, description, func):
        self.tools[name] = {
            "description": description,
            "func": func
        }

    def list_tools(self):
        return {
            name: tool["description"]
            for name, tool in self.tools.items()
        }

    def call_tool(self, name, query):
        if name not in self.tools:
            return f"Tool {name} not found."

        return self.tools[name]["func"](query)