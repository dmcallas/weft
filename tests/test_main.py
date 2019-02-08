from main import some_fn

def test_point_mul():
    x = 1
    y = 2
    assert 3 == some_fn(x, y)

    assert 1 == some_fn(1, -2)

