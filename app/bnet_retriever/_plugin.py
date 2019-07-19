from bson import ObjectId


class Plugin:
    def __init__(self, runner: 'Runner'):
        self.root: 'Runner' = runner
        self._id: ObjectId = runner._id
