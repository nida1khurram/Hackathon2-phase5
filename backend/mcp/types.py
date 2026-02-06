"""
Mock MCP types module to satisfy imports
"""
class TextContent:
    def __init__(self, type=None, text=None):
        self.type = type
        self.text = text