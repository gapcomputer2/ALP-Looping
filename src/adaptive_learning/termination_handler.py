"""Termination condition evaluation with robust error handling."""

import logging
import threading
from typing import Callable, Any, Optional
import time

from .exceptions import (
    TerminationConditionError,
    InvalidTerminationConfigError,
    TerminationConditionTimeoutError
)

class TerminationConditionHandler:
    """
    Manages evaluation of termination conditions with comprehensive error handling.
    
    Handles different types of termination conditions, validates inputs,
    and provides detailed error information.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the TerminationConditionHandler.

        Args:
            logger (Optional[logging.Logger]): Logger for tracking termination events.
                If not provided, a default logger will be created.
        """
        self.logger = logger or logging.getLogger(__name__)

    def evaluate_condition(
        self, 
        condition: Callable[[], bool], 
        timeout: float = 5.0, 
        condition_name: Optional[str] = None
    ) -> bool:
        """
        Evaluate a termination condition with error handling and timeout.

        Args:
            condition (Callable[[], bool]): Function that returns a boolean.
            timeout (float, optional): Maximum time allowed for condition evaluation. Defaults to 5 seconds.
            condition_name (Optional[str], optional): Name of the condition for logging.

        Returns:
            bool: Result of the condition evaluation.

        Raises:
            InvalidTerminationConfigError: If the condition is not callable.
            TerminationConditionTimeoutError: If condition evaluation exceeds timeout.
            TerminationConditionError: For other unexpected errors during evaluation.
        """
        # Validate condition
        if not callable(condition):
            raise InvalidTerminationConfigError(
                f"Termination condition must be callable. Got {type(condition)}", 
                condition_type=condition_name
            )

        # Thread-safe condition result and error storage
        result = [None]
        error = [None]

        def run_condition():
            try:
                result[0] = condition()
            except Exception as e:
                error[0] = e

        # Run condition in a separate thread with timeout
        thread = threading.Thread(target=run_condition)
        thread.start()
        thread.join(timeout=timeout)

        # Check for timeout or thread completion
        if thread.is_alive():
            self.logger.warning(f"Termination condition '{condition_name or 'unnamed'}' timed out")
            raise TerminationConditionTimeoutError(
                f"Condition evaluation timed out after {timeout} seconds", 
                condition_type=condition_name
            )

        # Check for any errors in the condition
        if error[0] is not None:
            self.logger.error(f"Error in termination condition: {error[0]}")
            raise TerminationConditionError(
                f"Unexpected error: {error[0]}", 
                condition_type=condition_name
            )

        # Log and return result
        self.logger.debug(
            f"Termination condition '{condition_name or 'unnamed'}' evaluated: {result[0]}"
        )
        return result[0]