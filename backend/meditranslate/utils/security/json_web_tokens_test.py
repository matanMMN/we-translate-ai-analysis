import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from json_web_tokens import create_jwt_token, decode_jwt_token, decode_expired_jwt_token, JWTAlgorithm, JWTDecodeError, JWTExpiredError


@pytest.fixture
def setup_data():
    """Setup test data as a fixture"""
    return {
        "secret_key": "test_secret",
        "data": {"user_id": 123, "role": "admin"},
        "expire_minutes": 5,
        "algorithm": JWTAlgorithm.HS256
    }


def test_create_jwt_token(setup_data):
    """Test the creation of JWT token"""
    token = create_jwt_token(setup_data['secret_key'], setup_data['data'], setup_data['expire_minutes'], algorithm=setup_data['algorithm'])
    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"


def test_decode_jwt_token_valid(setup_data):
    """Test decoding a valid JWT token"""
    token = create_jwt_token(setup_data['secret_key'], setup_data['data'], setup_data['expire_minutes'], algorithm=setup_data['algorithm'])
    decoded_data = decode_jwt_token(setup_data['secret_key'], token, algorithms=[setup_data['algorithm']])
    assert 'data' in decoded_data, "Decoded data should contain 'data'"
    assert decoded_data['data']['user_id'] == 123, "User ID should be 123"
    assert decoded_data['data']['role'] == 'admin', "Role should be 'admin'"


def test_decode_jwt_token_expired(setup_data):
    """Test decoding an expired JWT token"""
    expired_token = create_jwt_token(setup_data['secret_key'], setup_data['data'], expire_minutes=-1, algorithm=setup_data['algorithm'])
    with pytest.raises(JWTExpiredError):
        decode_jwt_token(setup_data['secret_key'], expired_token, algorithms=[setup_data['algorithm']])


def test_decode_jwt_token_invalid_secret(setup_data):
    """Test decoding JWT token with an invalid secret key"""
    token = create_jwt_token(setup_data['secret_key'], setup_data['data'], setup_data['expire_minutes'], algorithm=setup_data['algorithm'])
    with pytest.raises(JWTDecodeError):
        decode_jwt_token("wrong_secret", token, algorithms=[setup_data['algorithm']])


def test_decode_expired_jwt_token(setup_data):
    """Test decoding an expired JWT token without checking expiration"""
    expired_token = create_jwt_token(setup_data['secret_key'], setup_data['data'], expire_minutes=-1, algorithm=setup_data['algorithm'])
    decoded_data = decode_expired_jwt_token(setup_data['secret_key'], expired_token, algorithms=[setup_data['algorithm']])
    assert 'data' in decoded_data, "Decoded data should contain 'data'"
    assert decoded_data['data']['user_id'] == 123, "User ID should be 123"
    assert decoded_data['data']['role'] == 'admin', "Role should be 'admin'"


def test_decode_expired_jwt_token_invalid_secret(setup_data):
    """Test decoding an expired JWT token with an invalid secret key"""
    expired_token = create_jwt_token(setup_data['secret_key'], setup_data['data'], expire_minutes=-1, algorithm=setup_data['algorithm'])
    with pytest.raises(JWTDecodeError):
        decode_expired_jwt_token("wrong_secret", expired_token, algorithms=[setup_data['algorithm']])
