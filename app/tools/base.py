class BaseToolGroup:
    namespace = "base"

    def __init__(self, *, client, context):
        self.client = client
        self.context = context
