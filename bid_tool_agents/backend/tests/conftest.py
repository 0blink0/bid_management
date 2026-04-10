"""
tests/conftest.py
"""
import pytest
import sys
import os

# 确保项目根目录在path中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
