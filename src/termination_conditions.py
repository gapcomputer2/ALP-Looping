from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class TerminationConditionError(Exception):
    """
    Custom exception for errors during termination condition evaluation.
    
    Attributes:
        message (str): Descriptive error message
        context (Optional[Dict[str, Any]]): Additional context about the error
    """
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.context = context or {}
        super().__init__(self.message)


class AbstractTerminationCondition(ABC):
    """
    Abstract base class for defining termination conditions in an adaptive learning process.
    
    Provides a structured approach to evaluating whether a learning process should terminate.
    """
    
    @abstractmethod
    def evaluate(self, **kwargs: Any) -> bool:
        """
        Evaluate the termination condition.
        
        Args:
            **kwargs: Flexible keyword arguments for condition evaluation
        
        Returns:
            bool: Whether the termination condition is met
        
        Raises:
            TerminationConditionError: If an error occurs during evaluation
        """
        try:
            # Placeholder for concrete implementation in subclasses
            pass
        except Exception as e:
            raise TerminationConditionError(
                f"Error evaluating termination condition: {str(e)}",
                context={
                    "exception_type": type(e).__name__,
                    "original_exception": str(e)
                }
            )


class MaxIterationTerminationCondition(AbstractTerminationCondition):
    """
    Termination condition based on maximum number of iterations.
    
    Ensures learning process stops after a predefined number of iterations.
    """
    
    def __init__(self, max_iterations: int):
        """
        Initialize with maximum allowed iterations.
        
        Args:
            max_iterations (int): Maximum number of iterations allowed
        
        Raises:
            ValueError: If max_iterations is not a positive integer
        """
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            raise ValueError("max_iterations must be a positive integer")
        
        self.max_iterations = max_iterations
    
    def evaluate(self, current_iteration: int, **kwargs: Any) -> bool:
        """
        Check if current iteration exceeds maximum allowed iterations.
        
        Args:
            current_iteration (int): Current iteration number
            **kwargs: Additional context (ignored)
        
        Returns:
            bool: True if max iterations reached, False otherwise
        
        Raises:
            TerminationConditionError: If evaluation fails
        """
        try:
            return current_iteration >= self.max_iterations
        except Exception as e:
            raise TerminationConditionError(
                f"Error in max iteration termination condition: {str(e)}",
                context={
                    "current_iteration": current_iteration,
                    "max_iterations": self.max_iterations
                }
            )