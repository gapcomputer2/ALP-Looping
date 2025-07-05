"""Custom exceptions for the Adaptive Learning Process."""

class AdaptiveLearningError(Exception):
    """Base exception for Adaptive Learning Process errors."""
    pass

class TerminationConditionError(AdaptiveLearningError):
    """Exception raised when there are issues evaluating termination conditions."""
    def __init__(self, message: str, condition_type: str = None):
        """
        Initialize the TerminationConditionError.

        Args:
            message (str): Description of the error.
            condition_type (str, optional): Type of termination condition that failed.
        """
        self.condition_type = condition_type
        super().__init__(f"Termination condition error: {message}")

class InvalidTerminationConfigError(TerminationConditionError):
    """Exception raised when termination condition configuration is invalid."""
    pass

class TerminationConditionTimeoutError(TerminationConditionError):
    """Exception raised when termination condition evaluation times out."""
    pass