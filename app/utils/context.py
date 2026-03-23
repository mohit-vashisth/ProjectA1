from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default="None")
ip_ctx = ContextVar("ip", default="Unknown")
user_agent_ctx = ContextVar("user_agent", default="Unknown")
path_ctx = ContextVar("path", default="Unknown")

def set_request_context(request_id: str, ip: str, user_agent: str, path: str):
    request_id_ctx.set(request_id)
    ip_ctx.set(ip)
    user_agent_ctx.set(user_agent)
    path_ctx.set(path)

def get_request_id():
    return request_id_ctx.get()

def get_ip():
    return ip_ctx.get()

def get_user_agent():
    return user_agent_ctx.get()

def get_path():
    return path_ctx.get()
