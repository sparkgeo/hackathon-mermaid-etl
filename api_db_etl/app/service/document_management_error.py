class DocumentManagementError(Exception):
    def __init__(self, reason):
        self.detail = reason
