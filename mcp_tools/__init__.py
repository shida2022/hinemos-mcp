from .repository import get_tools as repo_tools, dispatch as repo_dispatch
from .calendar import get_tools as calendar_tools, dispatch as calendar_dispatch
from .monitor import get_tools as monitor_tools, dispatch as monitor_dispatch
from .monitor_result import get_tools as monitor_result_tools, dispatch as monitor_result_dispatch
from .job import get_tools as job_tools, dispatch as job_dispatch

ALL_TOOL_MODULES = [
    (repo_tools, repo_dispatch),
    (calendar_tools, calendar_dispatch),
    (monitor_tools, monitor_dispatch),
    (monitor_result_tools, monitor_result_dispatch),
    (job_tools, job_dispatch),
]

def get_all_tools():
    tools = []
    for get_tools, _ in ALL_TOOL_MODULES:
        tools.extend(get_tools())
    return tools

async def dispatch_tool(name, manager, arguments):
    for get_tools, dispatch in ALL_TOOL_MODULES:
        tool_names = [tool.name for tool in get_tools()]
        if name in tool_names:
            return await dispatch(name, manager, arguments)
    return None