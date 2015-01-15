# Disables the CSRF token check

class DisableCSRF(object):
    @staticmethod
    def process_request(request):
        setattr(request, '_dont_enforce_csrf_checks', True)
