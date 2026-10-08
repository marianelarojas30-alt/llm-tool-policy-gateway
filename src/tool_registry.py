"""The single list of tools the gateway knows, and the risk category of each.

Every other module asks this one; adding a tool means adding one line here.
"""

from typing import Dict

EXTERNAL = "external"        # sends data outside (email, webhooks)
MEMORY = "memory"            # writes long-term agent memory
DESTRUCTIVE = "destructive"  # deletes or overwrites data
READ = "read"                # reads files or retrieved context

TOOLS: Dict[str, str] = {
    "send_email_simulated": EXTERNAL,
    "write_memory_simulated": MEMORY,
    "delete_file_simulated": DESTRUCTIVE,
    "call_webhook_simulated": EXTERNAL,
    "read_file_simulated": READ,
    "retrieve_context_simulated": READ,
}
