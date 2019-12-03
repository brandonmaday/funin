import funpy as F

add = lambda a: lambda b: a + b

def test_identity ():
    assert F.identity (1) == 1

def test_always ():
    assert F.always (1) (2) == 1

def test_result ():
    assert F.result (lambda a: a==1) (1) == {"ok": True, "data": 1}
    assert F.result (lambda a: a==1) (2) == {"ok": False, "data": 2}

def test_join ():
    assert F.join ({"ok": True, "data": 1}) == 1
    assert F.join ({"ok": False, "data": 1}) == 1

def test_either ():
    assert F.either (add (1), add (2)) ({"ok": True, "data": 1}) == 3
    assert F.either (add (1), add (2)) ({"ok": False, "data": 1}) == 2

def test_flip ():
    fn = lambda a: lambda b: f"{a} {b}"
    assert F.flip (fn) ("1") ("2") == "2 1"

def test_filter ():
    assert F.filter (lambda a: a % 2 == 0) ([1,2,3,4]) == [2,4]

def test_reduce ():
    def mult (acc, i):
        acc [i [0]] = i [1]
        return acc

    arr = [["a", 1], ["b", 2], ["c", 3]]
    assert F.reduce (mult) ({}) (arr) == {"a": 1, "b": 2, "c": 3}

def test_compose ():
    addOne = add (1)
    multFive = lambda a: a * 5
    assert F.compose (addOne, multFive, addOne) (1) == 11

def test_mapList ():
    assert F._mapList (add (1)) ([1,2,3]) == [2,3,4]

def test_mapResult ():
    res = {"ok": True, "data": 1}
    badRes = {"ok": False, "data": 1}
    assert F._mapResult (add (1)) (res) == {"ok": True, "data": 2}
    assert F._mapResult (add (1)) (badRes) == {"ok": False, "data": 1}

def test_map ():
    res = {"ok": True, "data": 1}
    badRes = {"ok": False, "data": 1}
    assert F.map (add (1)) ([1,2,3]) == [2,3,4]
    assert F.map (add (1)) (res) == {"ok": True, "data": 2}
    assert F.map (add (1)) (badRes) == {"ok": False, "data": 1}

def test_chain ():
    res = {"ok": True, "data": 1}
    badRes = {"ok": False, "data": 1}
    toGood = lambda a: {"ok": True, "data": add (1) (a)}
    toBad = lambda a: {"ok": False, "data": add (2) (a)}
    assert F.chain (toGood) (badRes) == badRes
    assert F.chain (toBad) (res) == {"ok": False, "data": 3}
    assert F.chain (toGood) (res) == {"ok": True, "data": 2}

def test_ap ():
    goodA = F.right (1)
    goodB = F.right (2)
    badA = F.left (1)
    badB = F.left (2)
    assert F.ap (F.map (add) (goodA)) (goodB) == {"ok": True, "data": 3}
    assert F.ap (F.map (add) (badA)) (goodB) == {"ok": False, "data": 1}
    assert F.ap (F.map (add) (goodA)) (badB) == {"ok": False, "data": 2}
    assert F.ap (F.map (add) (badA)) (badB) == {"ok": False, "data": 1}

def test_liftA2 ():
    goodA = F.right (1)
    goodB = F.right (2)
    badA = F.left (1)
    badB = F.left (2)
    safeAdd = F.liftA2 (add)
    assert safeAdd (goodA) (goodB) == {"ok": True, "data": 3}
    assert safeAdd (badA) (goodB) == {"ok": False, "data": 1}
    assert safeAdd (goodA) (badB) == {"ok": False, "data": 2}
    assert safeAdd (badA) (badB) == {"ok": False, "data": 1}

def test_merge ():
    a = {"a": 1, "b": 2}
    b = {"b": 3, "c": 4}
    assert F.merge (a) (b) == {"a": 1, "b": 3, "c": 4}

def test_assoc ():
    a = {"a": 1, "b": 2}
    assert F.assoc ("b") (3) (a) == {"a": 1, "b": 3}
    assert F.assoc ("c") (4) (a) == {"a": 1, "b": 2, "c": 4}

def test_tail ():
    assert F.tail ([]) == []
    assert F.tail ([1,2,3]) == [2,3]

def test_nth ():
    assert F.nth (1) ([1, 2, 3]) == {"ok": True, "data": 2}
    assert F.nth (10) ([1, 2, 3]) == {"ok": False, "data": 10}

def test_head ():
    assert F.head ([1, 2, 3]) == {"ok": True, "data": 1}
    assert F.head ([]) == {"ok": False, "data": 0}

def test_last ():
    assert F.last ([1, 2, 3]) == {"ok": True, "data": 3}
    assert F.last ([]) == {"ok": False, "data": -1}

def test_prop ():
    a = {"a": 1, "b": 2}
    assert F.prop ("a") (a) == {"ok": True, "data": 1}
    assert F.prop ("c") (a) == {"ok": False, "data": "c"}

def test_evolve ():
    a = {"a": 1, "b": 2}
    assert F.evolve ("a") (add (1)) (a) == {"ok": True, "data": {"a": 2, "b": 2}}
    assert F.evolve ("c") (add (1)) (a) == {"ok": False, "data": "c"}

def test_trampoline ():
    def countdown (i):
        if i == 0:
            return 0
        else:
            return F.tailR (countdown) (i-1)

    def countup (start, end):
        loop = F.tailR (countup)
        if start >= end:
            return end
        return loop (start + 1, end)

    assert F.bounce (countdown) (19900) == 0
    assert F.bounce (countup) (0, 190000) == 190000

