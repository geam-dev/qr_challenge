class UUIDNotValid(Exception):
    def __init__(self, msg):
        super().__init__(f"Passed UUID Format is not valid. {msg}")