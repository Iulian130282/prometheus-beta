import datetime
import os
import json
from typing import Any, Union, Dict

def log_data_with_timestamp(data: Any, log_file: str = 'logs/data_log.json') -> bool:
    """
    Log data with a timestamp to a JSON file.
    
    Args:
        data (Any): The data to be logged. Can be of any JSON-serializable type.
        log_file (str, optional): Path to the log file. Defaults to 'logs/data_log.json'.
    
    Returns:
        bool: True if logging was successful, False otherwise.
    
    Raises:
        TypeError: If data cannot be JSON serialized
        IOError: If there are issues writing to the log file
    """
    try:
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Create log entry with timestamp
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'data': data
        }
        
        # Determine file mode - append if exists, write if not
        file_mode = 'a' if os.path.exists(log_file) else 'w'
        
        # Write log entry
        with open(log_file, file_mode) as f:
            json.dump(log_entry, f)
            f.write('\n')  # Ensure each entry is on a new line
        
        return True
    
    except TypeError:
        # Catch JSON serialization errors
        return False
    except IOError:
        # Catch file writing errors
        return False