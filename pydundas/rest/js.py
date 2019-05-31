class JsApi:
    """Get code to generate JavaScript objects to simplify long API calls"""
    def __init__(self, *irrelevantagrs, **irrelevantkwargs):
        pass

    @classmethod
    def SingleNumberValue(cls, parameterId, value, isInverted=False):
        return {
            "__classType": "dundas.data.SingleNumberValue",
            "parameterValueType": "SingleNumber",
            "isInverted": isInverted,
            "parameterId": parameterId,
            "value": value
        }

    @classmethod
    def SingleBooleanValue(cls, parameterId, value, isInverted=False):
        return {
            "__classType": "dundas.data.SingleBooleanValue",
            "parameterValueType": "SingleBoolean",
            "isInverted": isInverted,
            "parameterId": parameterId,
            "value": value
        }

    @classmethod
    def SingleTrueValue(cls, parameterId):
        return cls.SingleBooleanValue(parameterId, True)

    @classmethod
    def SingleFalseValue(cls, parameterId):
        return cls.SingleBooleanValue(parameterId, False)

    @classmethod
    def notificationRecipient(cls, email, isUnsubscribeAllowed=True):
        return {
            "__classType": "dundas.notifications.Recipient",
            "email": email,
            "isUnsubscribeAllowed": isUnsubscribeAllowed,
            "viewOverrides": []
        }
