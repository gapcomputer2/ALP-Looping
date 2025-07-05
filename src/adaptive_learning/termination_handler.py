"""Termination condition evaluation with robust error handling."""

import logging
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

        start_time = time.time()
        try:
            # Use a timeout mechanism
            while time.time() - start_time < timeout:
                try:
                    result = condition()
                    
                    # Log condition evaluation
                    self.logger.debug(
                        f"Termination condition '{condition_name or 'unnamed'}' evaluated: {result}"
                    )
                    
                    return result

                except Exception as inner_error:
                    # Handle unexpected errors in the condition
                    self.logger.warning(
                        f"Error in termination condition '{condition_name or 'unnamed'}': {inner_error}"
                    )
                    raise TerminationConditionError(
                        f"Unexpected error: {inner_error}", 
                        condition_type=condition_name
                    )

            # Timeout occurred
            raise TerminationConditionTimeoutError(
                f"Condition evaluation timed out after {timeout} seconds", 
                condition_type=condition_name
            )

        except Exception as e:
            # Log and re-raise with context
            self.logger.error(f"Termination condition evaluation failed: {e}")
            raise