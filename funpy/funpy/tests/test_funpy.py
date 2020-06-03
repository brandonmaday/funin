from backend import funpy as F

def test_curry():
    @F.curry
    def add(a,b):
        return a + b

    assert add(1,2) == 3
    assert add(1)(2) == 3

def test_flip():
    assert F.flip(lambda a, b: a + b, "b", "a") == "ab"

def test_filter():
    assert F.filter(lambda a: a != 2, [1,2,3]) == [1,3,]

def test_reduce():
    assert F.reduce(
        lambda a, b: {**a, **b},
        {},
        [{"a": 1, "b": 2}, {"b": 3, "c": 4}]
    ) == {"a": 1, "b": 3, "c": 4}

def test_compose():
    assert F.compose(
        lambda a: a * 5,
        lambda a: a + 1
    )(1) == 10

def test_identity():
    assert F.identity(1) == 1

def test_always():
    assert F.always(1, 2) == 1
    assert F.always(1, 2, 3) == 1

def test_left():
    assert F.left(1) == F.Result(False, 1)

def test_right():
    assert F.right(1) == F.Result(True, 1)

def test_map_list():
    assert F.map_list(lambda a: a + 1, [1,2,3]) == [2,3,4]

def test_map_result():
    assert F.map_result(lambda a: a + 1, F.left(1)) == F.left(1)
    assert F.map_result(lambda a: a + 1, F.right(1)) == F.right(2)

def test_map():
    assert F.map(lambda a: a + 1, [1,2,3]) == [2,3,4]
    assert F.map(lambda a: a + 1, F.left(1)) == F.left(1)
    assert F.map(lambda a: a + 1, F.right(1)) == F.right(2)

def test_chain():
    assert F.chain(lambda a: a + 1, F.left(1)) == F.left(1)
    assert F.chain(lambda a: a + 1, F.right(1)) == 2
    assert F.chain(lambda a: F.right(a + 1), F.right(1)) == F.right(2)

def test_ap():
    @F.curry
    def add(a,b):
        return a + b

    assert F.ap(F.map(add, F.right(1)), F.right(2)) == F.right(3)
    assert F.ap(F.map(add, F.left(1)), F.right(2)) == F.left(1)
    assert F.ap(F.map(add, F.right(1)), F.left(2)) == F.left(2)
    assert F.ap(F.map(add, F.left(1)), F.left(2)) == F.left(1)

def test_liftA2():
    @F.curry
    def add(a,b):
        return a + b

    assert F.liftA2(add, F.right(1), F.right(2)) == F.right(3)
    assert F.liftA2(add, F.left(1), F.right(2)) == F.left(1)
    assert F.liftA2(add, F.right(1), F.left(2)) == F.left(2)
    assert F.liftA2(add, F.left(1), F.left(2)) == F.left(1)

def test_either():
    assert F.either(lambda a: a + 1, lambda a: a + 2, F.left(1)) == 2
    assert F.either(lambda a: a + 1, lambda a: a + 2, F.right(1)) == 3

def test_or_else():
    assert F.or_else(lambda a: a + 1, F.left(1)) == 2
    assert F.or_else(lambda a: a + 1, F.right(1)) == 1

def test_mut():
    x = F.right(9)
    z = x.data
    z = 33
    assert x == F.right(9)

def test_merge():
    assert F.merge({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {
        "a": 1, "b": 3, "c": 4
    }

def test_assoc():
    assert F.assoc("b", 3, {"a": 1, "b": 2}) == {"a": 1, "b": 3}
    assert F.assoc("c", 3, {"a": 1, "b": 2}) == {"a": 1, "b": 2, "c": 3}

def test_prop():
    assert F.prop("a")({"a": 3}) == F.right(3)
    assert F.prop("b")({"a": 3}) == F.left("b")

def test_tail():
    assert F.tail([]) == []
    assert F.tail([1,2,3]) == [2,3]

def test_nth():
    assert F.nth(2, [1,2,3]) == F.right(3)
    assert F.nth(8, [1,2,3]) == F.left(8)
    assert F.head([1,2,3]) == F.right(1)
    assert F.last([1,2,3]) == F.right(3)
    assert F.head([]) == F.left(0)
    assert F.last([]) == F.left(-1)

def test_evolve():
    assert F.evolve("a", lambda a: a + 1, {"a": 1}) == F.right({"a": 2})
    assert F.evolve("b", lambda a: a + 1, {"a": 1}) == F.left("b")

def test_trampoline():
    def countdown(i):
        if i <= 0:
            return i
        return F.tail_r(countdown, i-1)

    def countup(start, end):
        if start >= end:
            return end
        return F.tail_r(countup, start + 1, end)

    assert F.bounce(countdown, 19900) == 0
    assert F.bounce(countup, 0, 19900) == 19900
