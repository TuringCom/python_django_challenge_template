from rest_framework.response import Response


class Error:
    def __init__(self, code, message, _status=None, field=None):
        self._message = message
        self.status = _status
        self.field = field
        self.code = code

    def __str__(self):
        return self.code

    @property
    def message(self):
        if self.code == "USR_07" and self.field is not None:
            return self.field + self._message
        return self._message

    @message.setter
    def message(self, value):
        self._message = value


# Authentication's Errors
AUT_01 = Error(code="AUT_01", message="Authorization code is empty", _status=400)
AUT_02 = Error(code="AUT_02", message="Access Unauthorized", _status=401)

# Pagination's Errors
PAG_01 = Error(code="PAG_01", message="The order is not matched 'field,(DESC|ASC)'", _status=400)
PAG_02 = Error(code="PAG_02", message="The field of order is not allow sorting", _status=400)

# User's Errors
USR_01 = Error(code="USR_01", message="Email or Password is invalid", _status=400)
USR_02 = Error(code="USR_02", message="The field(s) are/is required", _status=400)
USR_03 = Error(code="USR_03", message="The email is invalid", _status=400, field='email')
USR_04 = Error(code="USR_04", message="The email already exists", _status=400, field='email')
USR_05 = Error(code="USR_05", message="The email doesn't exist", _status=404, field='email')
USR_06 = Error(code="USR_06", message="This is an invalid phone number", _status=400, field='phone')
USR_07 = Error(code="USR_07", message=" is too long", _status=400)
USR_08 = Error(code="USR_08", message="This is an invalid Credit Card", _status=400, field='credit_card')
USR_09 = Error(code="USR_09", message="The Shipping Region ID is not number", _status=400, field='shipping_region')
USR_10 = Error(code="USR_10", message="You must login first", _status=400)

# Category's Errors
CAT_01 = Error(code="CAT_01", message="Don't exist category with this ID", _status=404)

# Department's Errors
DEP_01 = Error(code="DEP_01", message="The ID is not a number", _status=400, field='id')
DEP_02 = Error(code="DEP_02", message="Don'exist department with this ID.", _status=404)

# Product's Errors
PRO_01 = Error(code="PRO_01", message="Don't exist product with this ID", _status=404)

# Order's Errors
ORD_01 = Error(code="ORD_01", message="Don't exist order with this ID", _status=404)
ORD_02 = Error(code="ORD_02", message="Don't exist order detail with this ID", _status=404)

# Commons Errors
COM_00 = Error(code="COM_00", message="There is something wrong", _status=500)
COM_01 = Error(code="COM_01", message="The field is required", _status=400)
COM_02 = Error(code="COM_02", message="Invalid Data", _status=400)
COM_10 = Error(code="COM_10", message="", _status=400)


# ShoppingCart's Errors
SHP_01 = Error(code="ORD_01", message="Don't exist shoppingCart with this cart_id", _status=404)


def handle(error: Error):
    error_response = {"error": {
        "status": error.status,
        "code": error.code,
        "message": error.message,
        "field": error.field
    }}
    return Response(error_response, status=error.status)
