from tempo_toolkit.application.errors import TempoBaseError


class StatusUpdateFlowError(TempoBaseError):
    status_code = 400
    detail = "Cannot update update status."
