"""Tests for TerminationConditionHandler."""

import pytest
import time
import logging

from src.adaptive_learning.termination_handler import TerminationConditionHandler
from src.adaptive_learning.exceptions import (
    InvalidTerminationConfigError,
    TerminationConditionTimeoutError,
    TerminationConditionError
)

def test_successful_condition():
    """Test successful termination condition evaluation."""
    handler = TerminationConditionHandler()
    result = handler.evaluate_condition(lambda: True, condition_name="test_condition")
    assert result is True

def test_failed_condition():
    """Test termination condition that returns False."""
    handler = TerminationConditionHandler()
    result = handler.evaluate_condition(lambda: False, condition_name="test_condition")
    assert result is False

def test_invalid_condition():
    """Test handling of non-callable condition."""
    handler = TerminationConditionHandler()
    with pytest.raises(InvalidTerminationConfigError):
        handler.evaluate_condition("not a callable", condition_name="invalid_condition")

def test_condition_with_error():
    """Test handling of exception in condition."""
    handler = TerminationConditionHandler()
    
    def error_condition():
        raise ValueError("Simulated condition error")
    
    with pytest.raises(TerminationConditionError):
        handler.evaluate_condition(error_condition, condition_name="error_condition")

def test_condition_timeout():
    """Test timeout handling for long-running condition."""
    handler = TerminationConditionHandler()
    
    def slow_condition():
        time.sleep(6)  # Longer than default timeout
        return True
    
    with pytest.raises(TerminationConditionTimeoutError):
        handler.evaluate_condition(slow_condition, timeout=2.0, condition_name="slow_condition")

def test_custom_logger():
    """Test termination handler with a custom logger."""
    custom_logger = logging.getLogger("test_logger")
    custom_logger.setLevel(logging.DEBUG)
    
    handler = TerminationConditionHandler(logger=custom_logger)
    result = handler.evaluate_condition(lambda: True, condition_name="logged_condition")
    assert result is True