API_TEST_CASES = [
    ("valid", 200),
    ("expired", 401),
    ("invalid_auth_type", 401),
    ("no_token", 401),
    ("no_auth", 401),
]
