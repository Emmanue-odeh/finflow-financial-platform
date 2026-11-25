from app.security.passwords import hash_password, verify_password

def test_password_is_hashed():
    password = "FinFlowTest123!"

    hashed_password = hash_password(password)

    assert hashed_password != password

def test_correct_password_is_accepted():
    password = "FinFlowTest123!"

    hashed_password = hash_password(password)

    assert verify_password(hashed_password, password) is True

def test_incorrect_password_is_rejected():
    password = "FinFlowTest123!"

    hashed_password = hash_password(password)

    assert verify_password(
        hashed_password,
        "WrongPassword123!"
    ) is False