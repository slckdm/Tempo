from toolkit.service.exceptions import TempoException


class StatusUpdateFlowError(TempoException):
    status_code = 400
    detail = "Cannot update update status."
