from toolkit.service.exceptions import TempoBaseException


class StatusUpdateFlowError(TempoBaseException):
    status_code = 400
    detail = "Cannot update update status."
