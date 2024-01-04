class emptySQLTableException(Exception):
    def __init__(self,message="SQL Empty Table Excpetion"):
        self.message ="SQL Empty Table Exception"
        super().__init__(self.message)