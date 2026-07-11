class AutomationStateManager:

    _states = {}

    @classmethod
    def update(cls, app_id, data):

        cls._states[app_id] = {

            **cls._states.get(app_id, {}),

            **data,

        }

    @classmethod
    def get(cls, app_id):

        return cls._states.get(app_id)

    @classmethod
    def remove(cls, app_id):

        cls._states.pop(app_id, None)