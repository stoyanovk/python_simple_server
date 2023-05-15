from lib.get_pagination import get_pagination, Button


def test_pagination():
    # Test case 1
    result = get_pagination(page=1, total=10, limit=2)
    expected = [
        Button(number=1, is_active=True),
        Button(number=2),
        Button(dots=True),
        Button(number=5),
    ]
    assert result == expected

    # Test case 2
    result = get_pagination(page=2, total=10, limit=2)
    expected = [
        Button(number=1),
        Button(number=2, is_active=True),
        Button(number=3),
        Button(dots=True),
        Button(number=5),
    ]
    assert result == expected

    # Test case 3
    result = get_pagination(page=3, total=10, limit=2)
    expected = [
        Button(number=1),
        Button(number=2),
        Button(number=3, is_active=True),
        Button(number=4),
        Button(number=5),
    ]
    assert result == expected

    # Test case 4
    result = get_pagination(page=5, total=10, limit=2)
    expected = [
        Button(number=1),
        Button(dots=True),
        Button(number=4),
        Button(number=5, is_active=True),
    ]
    assert result == expected

    # Test case 5
    result = get_pagination(page=1, total=1, limit=2)
    expected = []
    assert result == expected


test_pagination()
