from .petstore_api import OK_STATUS_CODE, NOT_FOUND_STATUS_CODE


def assert_status_code_is_ok(status_code: int):
    assert_status_code(status_code, OK_STATUS_CODE)


def assert_status_code_is_not_found(status_code: int):
    assert_status_code(status_code, NOT_FOUND_STATUS_CODE)


def assert_status_code(status_code: int, expected_status_code: int):
    assert (
        status_code == expected_status_code
    ), f"Expected API response status code {expected_status_code}, got {status_code}"


def assert_fields_match(data, expected_data, fields):
    def get_nested_value(data, path):
        if isinstance(path, list):
            value = data
            for key in path:
                if not isinstance(value, dict):
                    raise ValueError(
                        f"Cannot access key '{key}' in non-dict structure: {value}"
                    )
                value = value.get(key)
            return value
        return data.get(path)

    for field in fields:
        actual_value = get_nested_value(data, field)
        expected_value = get_nested_value(expected_data, field)
        assert (
            actual_value == expected_value
        ), f"Field {field} mismatch: expected {expected_value}, got {actual_value}"
