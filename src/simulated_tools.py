def send_email_simulated(*args, **kwargs):
    raise RuntimeError("Simulated tool should not execute during policy evaluation.")

def write_memory_simulated(*args, **kwargs):
    raise RuntimeError("Simulated tool should not execute during policy evaluation.")

def call_webhook_simulated(*args, **kwargs):
    raise RuntimeError("Simulated tool should not execute during policy evaluation.")

def delete_file_simulated(*args, **kwargs):
    raise RuntimeError("Simulated tool should not execute during policy evaluation.")
