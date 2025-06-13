from .base import BaseClient
from .repository import RepositoryClient
from .monitor import MonitorClient
from .calendar import CalendarClient
from .collect import CollectClient
from .job import JobClient
from .monitor_result import MonitorResultClient

class HinemosClient(
    RepositoryClient,
    MonitorClient,
    CalendarClient,
    CollectClient,
    JobClient,
    MonitorResultClient,
    BaseClient
):
    pass