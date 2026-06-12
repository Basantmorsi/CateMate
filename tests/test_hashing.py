from CateMate.utils.hashing import hash_password, verify_password


def test_hash_and_verify_round_trip():
    h = hash_password("password123")
    assert h.startswith("$2b$")
    assert verify_password("password123", h) is True
    assert verify_password("wrong", h) is False


def test_verify_does_not_crash_on_malformed_hash():
    # Legacy/seed/corrupt values that aren't valid bcrypt hashes must fail
    # gracefully (return False) rather than raising and 500-ing the login.
    for bad in ["hashed_pw", "", "not-a-hash", "$2b$broken"]:
        assert verify_password("anything", bad) is False


def test_hashes_are_salted_and_unique():
    # Same password hashed twice should differ (random salt) but both verify.
    a = hash_password("samepass")
    b = hash_password("samepass")
    assert a != b
    assert verify_password("samepass", a)
    assert verify_password("samepass", b)
