import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
import os

class TerminationLogger:
    """
    A specialized logger for capturing ALP loop termination events.
    
    This logger provides detailed logging of why and when an ALP loop terminates,
    capturing iteration count, performance metrics, and other relevant details.
    """
    
    def __init__(self, log_dir: str = 'logs/termination'):
        """
        Initialize the TerminationLogger.
        
        Args:
            log_dir (str, optional): Directory to store termination logs. 
                                     Defaults to 'logs/termination'.
        """
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        self.log_dir = log_dir
        self.logger = logging.getLogger('termination_logger')
        self.logger.setLevel(logging.INFO)
        
        # File handler for JSON logs
        log_file = os.path.join(log_dir, f'termination_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        self.file_handler = logging.FileHandler(log_file)
        self.logger.addHandler(self.file_handler)
    
    def log_termination(
        self, 
        reason: str, 
        iteration_count: int, 
        performance_metrics: Optional[Dict[str, Any]] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log detailed information about loop termination.
        
        Args:
            reason (str): Reason for loop termination
            iteration_count (int): Number of iterations completed
            performance_metrics (dict, optional): Performance metrics at termination
            additional_info (dict, optional): Any extra contextual information
        """
        termination_event = {
            'timestamp': datetime.now().isoformat(),
            'reason': reason,
            'iteration_count': iteration_count,
            'performance_metrics': performance_metrics or {},
            'additional_info': additional_info or {}
        }
        
        # Log as JSON for structured logging
        try:
            log_entry = json.dumps(termination_event)
            self.logger.info(log_entry)
        except Exception as e:
            # Fallback logging if JSON serialization fails
            self.logger.error(f"Failed to log termination event: {e}")
    
    def close(self):
        """
        Close file handlers to ensure all logs are written.
        """
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)