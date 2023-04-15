class GetAllAssetsMessage:
    def __init__(self, assets: list[str], sender):
        self.assets: list[str] = assets
        self.sender = sender
