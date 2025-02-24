import os
import json
import pytest
import datetime
from src.timestamp_logger import log_data_with_timestamp

def test_log_basic_data(tmp_path):
    """Test logging a basic string"""
    log_file = str(tmp_path / 'log.json')
    result = log_data_with_timestamp('test message', log_file)
    
    assert result is True
    
    # Verify log file contents
    with open(log_file, 'r') as f:
        log_entry = json.loads(f.readline().strip())
        assert log_entry['data'] == 'test message'
        assert 'timestamp' in log_entry

def test_log_complex_data(tmp_path):
    """Test logging a dictionary"""
    log_file = str(tmp_path / 'log.json')
    test_dict = {'key': 'value', 'number': 42}
    
    result = log_data_with_timestamp(test_dict, log_file)
    
    assert result is True
    
    # Verify log file contents
    with open(log_file, 'r') as f:
        log_entry = json.loads(f.readline().strip())
        assert log_entry['data'] == test_dict

def test_log_append_mode(tmp_path):
    """Test that logs are appended, not overwritten"""
    log_file = str(tmp_path / 'log.json')
    
    # Log first entry
    log_data_with_timestamp('first message', log_file)
    log_data_with_timestamp('second message', log_file)
    
    # Read log file
    with open(log_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2
        
        first_entry = json.loads(lines[0].strip())
        second_entry = json.loads(lines[1].strip())
        
        assert first_entry['data'] == 'first message'
        assert second_entry['data'] == 'second message'

def test_log_non_serializable_data(tmp_path):
    """Test logging non-JSON serializable data"""
    log_file = str(tmp_path / 'log.json')
    
    # Custom class that's not JSON serializable
    class NonSerializable:
        pass
    
    result = log_data_with_timestamp(NonSerializable(), log_file)
    
    # Should return False for non-serializable data
    assert result is False

def test_default_log_path(tmp_path):
    """Test default log path creation"""
    # Temporarily change current working directory
    original_cwd = os.getcwd()
    os.chdir(str(tmp_path))
    
    try:
        # Use default log path
        result = log_data_with_timestamp('test')
        
        # Check if default log exists in logs directory
        default_log_path = os.path.join('logs', 'data_log.json')
        assert os.path.exists(default_log_path)
        assert result is True
    finally:
        # Restore original working directory
        os.chdir(original_cwd)