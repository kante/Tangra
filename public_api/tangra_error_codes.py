
class TangraErrorCodes:
    """Defines all the error codes returned by a FailureResponse
    """
    
    # Returned for bad username or password combinations.
    INVALID_CREDENTIALS = "Invalid username or passord."
    
    # Returned when requesting a stage/stage completion for a participant who has finished all stages.
    INVALID_STAGE_REQUEST = "Participant has finished all stages."
    
    def __init__(self):
        """Doesn't really need to do something this is a purely static class right now."""
        pass