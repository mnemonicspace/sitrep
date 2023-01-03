import pytest
from app.device_compile import palo_compile, cisco_compile

def test_palo():
    assert palo_compile()