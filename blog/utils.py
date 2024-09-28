from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'errors': response.data,  # Retain original errors
            'status_code': response.status_code,  # Add status code
            'message': 'There was an error processing your request.'  # Custom message
        }

    return response
