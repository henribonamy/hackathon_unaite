import os
import subprocess
from smolagents.tools import Tool
from typing import List, Dict, Any


class ShellExecutorTool(Tool):
    """A tool that can execute shell commands safely"""

    name = "shell_executor"
    description = """
    Execute shell commands in the terminal. 
    Use this to run installation commands, git clone, pip install, npm install, etc.
    Always be careful with commands that could be destructive.
    """
    inputs = {
        "working_directory": {
            "type": "string",
            "description": "directory to run the command in",
            "required": False,
            "nullable": True,
        },
        "command": {
            "type": "string",
            "description": "Command to execute in the shell",
            "required": True,
        },
    }
    output_type = "object"

    def forward(self, command: str, working_directory: str = None) -> Dict[str, Any]:
        """
        Execute a shell command and return the result

        Args:
            command: The shell command to execute
            working_directory: Optional directory to run the command in

        Returns:
            Dict with 'stdout', 'stderr', 'return_code', and 'success' keys
        """
        try:
            # Change to working directory if specified
            original_cwd = os.getcwd()
            if working_directory and os.path.exists(working_directory):
                os.chdir(working_directory)

            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            # Return to original directory
            os.chdir(original_cwd)

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0,
                "command": command,
            }

        except subprocess.TimeoutExpired:
            os.chdir(original_cwd)
            return {
                "stdout": "",
                "stderr": "Command timed out after 5 minutes",
                "return_code": -1,
                "success": False,
                "command": command,
            }
        except Exception as e:
            os.chdir(original_cwd)
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
                "success": False,
                "command": command,
            }


class FileSystemTool(Tool):
    """A tool for basic file system operations"""

    name = "filesystem"
    description = """
    Perform basic file system operations like checking if files/directories exist,
    creating directories, reading file contents, etc.
    """

    inputs = {
        "operation": {
            "type": "string",
            "description": "Operation to perform: 'exists', 'mkdir', 'read', 'write', 'list', 'rename'",
        },
        "path": {"type": "string", "description": "File or directory path"},
        "content": {
            "type": "string",
            "description": "Content for write operations",
            "required": False,
            "nullable": True,
        },
        "new_path": {
            "type": "string",
            "description": "New path for rename operations",
            "required": False,
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(
        self, operation: str, path: str, content: str = None, new_path: str = None
    ) -> Dict[str, Any]:
        """
        Perform file system operations

        Args:
            operation: 'exists', 'mkdir', 'read', 'write', 'list'
            path: File or directory path
            content: Content for write operations

        Returns:
            Dict with operation result
        """
        try:
            if operation == "exists":
                return {"success": True, "result": os.path.exists(path)}

            elif operation == "mkdir":
                os.makedirs(path, exist_ok=True)
                return {"success": True, "result": f"Directory {path} created"}

            elif operation == "read":
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"success": True, "result": content}

            elif operation == "write":
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content or "")
                return {"success": True, "result": f"File {path} written"}

            elif operation == "list":
                items = os.listdir(path)
                return {"success": True, "result": items}

            elif operation == "rename":
                if not new_path:
                    return {
                        "success": False,
                        "result": "New path must be provided for rename operation",
                    }
                os.rename(path, new_path)
                return {"success": True, "result": f"Renamed {path} to {new_path}"}

            else:
                return {"success": False, "result": f"Unknown operation: {operation}"}

        except Exception as e:
            return {"success": False, "result": str(e)}
