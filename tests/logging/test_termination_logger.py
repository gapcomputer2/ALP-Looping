import os
import json
import pytest
from datetime import datetime
from src.logging.termination_logger import TerminationLogger

def test_termination_logger_creation():
    """Test creating a TerminationLogger instance."""
    logger = TerminationLogger()
    assert os.path.exists(logger.log_dir)
    logger.close()

def test_termination_logging():
    """Test logging a termination event."""
    logger = TerminationLogger()
    
    # Log a termination event
    logger.log_termination(
        reason='Max iterations reached', 
        iteration_count=100,
        performance_metrics={'accuracy': 0.95, 'loss': 0.05},
        additional_info={'model_name': 'test_model'}
    )
    
    # Close the logger to ensure logs are written
    logger.close()
    
    # Check the latest log file
    log_files = os.listdir(logger.log_dir)
    assert len(log_files) > 0
    
    # Read the most recent log file
    latest_log = max([os.path.join(logger.log_dir, f) for f in log_files], key=os.path.getctime)
    
    with open(latest_log, 'r') as f:
        log_entry = json.loads(f.readline())
    
    assert log_entry['reason'] == 'Max iterations reached'
    assert log_entry['iteration_count'] == 100
    assert log_entry['performance_metrics'] == {'accuracy': 0.95, 'loss': 0.05}
    assert log_entry['additional_info'] == {'model_name': 'test_model'}

def test_termination_logger_error_handling():
    """Test error handling in termination logging."""
    logger = TerminationLogger()
    
    # Try logging with un-serializable object (should not raise exception)
    class UnserializableClass:
        pass
    
    logger.log_termination(
        reason='Error scenario', 
        iteration_count=50,
        additional_info={'bad_object': UnserializableClass()}
    )
    
    logger.close()
    
    # If no exception is raised, test passes
    assert True