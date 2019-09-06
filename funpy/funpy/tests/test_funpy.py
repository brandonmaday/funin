import funpy as fp

# Identities
def test_identity():
    assert fp.identity (10) == 10
    assert fp.identity ("cat") == "cat"
    assert fp.identity (32.2) != 32

def test_always():
    assert fp.always (10) () == 10
    assert fp.always (10) (9) == 10
    assert fp.always (10) (9, 11) == 10

def test_complement():
    fn = lambda x: x == 1
    assert fp.complement (fn) (1) == False
    assert fp.complement (fn) (2) == True

def test_constants():
    assert fp.T() == True
    assert fp.T(1) == True
    assert fp.T(1,2) == True
    assert fp.F() == False
    assert fp.F(1) == False
    assert fp.F(1,2) == False
    assert fp.isNone (None) == True
    assert fp.isNone ("cat") == False
    assert fp.notNone (None) == False
    assert fp.notNone ("cat") == True

def test_flip():
    fn = lambda a: lambda b: f"{a}{b}"
    assert fp.flip (fn) ("b") ("a") == "ab"

# higher order functions
def test_map():
    assert fp.map (lambda x: x+1) ([1,2,3]) == [2,3,4]

def test_filter():
    assert fp.filter (lambda x: x!=2) ([1,2,3]) == [1,3,]

def test_reduce():
    assert fp.reduce (lambda a, b: a + b) (0) ([1,2,3]) == 6

# Composition
def test_compose():
    addOne = lambda x: x+1
    multFive = lambda x: x*5
    assert fp.compose (multFive, addOne) (1) == 10
    assert fp.pipe (addOne, multFive) (1) == 10

# Conditions
def test_conditional():
    isOne = lambda x: x == 1
    addOne = lambda x: x + 1
    assert fp.ifElse (isOne, addOne, lambda x: x) (1) == 2
    assert fp.ifElse (isOne, addOne, lambda x: x+2) (5) == 7
    assert fp.when (isOne, addOne) (1) == 2
    assert fp.unless (isOne, addOne) (1) == 1
    assert fp.when (isOne, addOne) (5) == 5
    assert fp.unless (isOne, addOne) (5) == 6

def test_both():
    assert fp.both (lambda a: a==1) (lambda a: a==2) (2) == False
    assert fp.both (lambda a: a==2) (lambda a: a==2) (2) == True
    assert fp.both (lambda a: a==1) (lambda a: a==2) (2) == False

def test_eitherOr():
    assert fp.eitherOr (lambda a: a==1) (lambda a: a==2) (2) == True
    assert fp.eitherOr (lambda a: a==2) (lambda a: a==2) (2) == True
    assert fp.eitherOr (lambda a: a==2) (lambda a: a==1) (2) == True
    assert fp.eitherOr (lambda a: a==2) (lambda a: a==3) (1) == False

def test_lt():
    assert fp.lt (10) (5) == True
    assert fp.lt (10) (10) == False
    assert fp.lt (10) (15) == False
    
def test_gt():
    assert fp.gt (10) (5) == False
    assert fp.gt (10) (10) == False
    assert fp.gt (10) (15) == True

def test_equals():
    assert fp.equals (10) (5) == False
    assert fp.equals (10) (10) == True
    assert fp.equals (10) (15) == False
    
def test_lte():
    assert fp.lte (10) (5) == True
    assert fp.lte (10) (10) == True
    assert fp.lte (10) (15) == False
    
def test_gte():
    assert fp.gte (10) (5) == False
    assert fp.gte (10) (10) == True
    assert fp.gte (10) (15) == True

def test_isList():
    assert fp.isList ([]) == True
    assert fp.isList (["a", 1, False]) == True
    assert fp.isList ("cat") == False
    assert fp.isList (None) == False
    assert fp.isList (1) == False

def emptyList():
    assert fp.emptyList ([]) == True
    assert fp.emptyList (["a", 123]) == False
    assert fp.emptyList ("cat") == False
    assert fp.emptyList (None) == False

def test_notEmptyList():
    assert fp.notEmptyList ([]) == False
    assert fp.notEmptyList (["a", 123]) == True
    assert fp.notEmptyList ("cat") == False
    assert fp.notEmptyList (None) == False

# Accessors
def test_head():
    assert fp.head ([1,2,3]) == 1
    assert fp.head (["bob",2,3]) == "bob"

def test_last():
    assert fp.last ([1,2,3]) == 3
    assert fp.last (["bob",2,"cat"]) == "cat"

def test_nth():
    assert fp.nth (1) ([1,2,3]) == 2
    assert fp.nth (2) (["bob",2,"cat"]) == "cat"

def test_tail():
    assert fp.tail ([1,2,3]) == [2, 3]
    assert fp.tail (["bob",2,"cat"]) == [2, "cat"]

def test_prop():
    assert fp.prop ("name") ({"name": "bob", "age": 34}) == "bob"
    assert fp.prop ("age") ({"name": "bob", "age": 34}) == 34

def test_path():
    fakeUser = {"name": "brandon", "adr": {"street": "123 Maple"}}
    assert fp.path (["adr", "street"]) (fakeUser) == "123 Maple"
    assert fp.path (["name",]) (fakeUser) == "brandon"

def test_attr():
    class FakeUser():
        planet = "krypton"

        def __init__(self):
            self.name = "clark"

    assert fp.attr ("name") (FakeUser()) == "clark"
    assert fp.attr ("planet") (FakeUser()) == "krypton"

def test_pick():
    t1 = {"name": "brandon", "age": 34, "eyeColor": "green"}
    assert fp.pick (["name", "age"]) (t1) == {"name": "brandon", "age": 34}

# Access and Compare
def test_propEq():
    assert fp.propEq ("name") ("bob") ({"name": "bob"}) == True
    assert fp.propEq ("name") ("john") ({"name": "bob"}) == False

def test_pathEq():
    assert fp.pathEq (["address", "street"]) ("123") (
        {"address": {"street": "123"}}) == True
    assert fp.pathEq (["address", "street"]) ("bob") (
        {"address": {"street": "123"}}) == False

def test_cond():
    conds = [
        [lambda x: x > 30, lambda x: "gt30"],
        [lambda x: x > 20, lambda x: "gt20"],
        [lambda x: x > 10, lambda x: "gt10"],
        [lambda x: True, lambda x: "default"],
    ]
    assert fp.cond (conds) (10) == "default"
    assert fp.cond (conds) (20) == "gt10"
    assert fp.cond (conds) (30) == "gt20"

# Operations
def test_inc():
    assert fp.inc (1) == 2

def test_merge():
    assert fp.merge ({"a": 1, "b": 2, }) ({"c": 3}) == {"a": 1, "b": 2, "c": 3}
    assert fp.merge ({"a": 1, "b": 2, }) ({"b": 3}) == {"a": 1, "b": 3}

def test_trim():
    assert fp.trim ("  ") == ""
    assert fp.trim ("") == ""
    assert fp.trim (" a ") == "a"

def test_assoc():
    assert fp.assoc ("x") (3) ({"name": "brandon", "x": 99}) == {
        "name": "brandon", "x": 3}
    assert fp.assoc ("name") ("dog") ({"name": "brandon", "x": 99}) == {
        "name": "dog", "x": 99}

def test_evolve():
    assert fp.evolve ("x") (lambda x: x+1) ({"name": "brandon", "x": 99}) == {
        "name": "brandon", "x": 100}

def test_evolvePath():
    obj = {"name": "brandon", "age": 34, "address": {
        "street": "123 Example", "zip4": {"zip": 12345, "four": 6789}
    }}
    assert fp.evolvePath (["name"]) (lambda n: f"{n}1") (obj) == {
        "name": "brandon1", "age": 34, "address": {
            "street": "123 Example", "zip4": {"zip": 12345, "four": 6789}
        }
    }
    assert fp.evolvePath (["address", "zip4", "zip"]) (fp.inc) (obj) == {
        "name": "brandon", "age": 34, "address": {
            "street": "123 Example", "zip4": {"zip": 12346, "four": 6789}
        }
    }

def test_assocPath():
    obj = {"name": "brandon", "age": 34, "address": {
        "street": "123 Example", "zip4": {"zip": 12345, "four": 6789}
    }}
    assert fp.assocPath (["name"]) ("bob") (obj) == {
        "name": "bob", "age": 34, "address": {
            "street": "123 Example", "zip4": {"zip": 12345, "four": 6789}
        }
    }
    assert fp.assocPath (["address", "street"]) ("new street") (obj) == {
        "name": "brandon", "age": 34, "address": {
            "street": "new street", "zip4": {"zip": 12345, "four": 6789}
        }
    }
    assert fp.assocPath (["address", "zip4", "zip"]) (99999) (obj) == {
        "name": "brandon", "age": 34, "address": {
            "street": "123 Example", "zip4": {"zip": 99999, "four": 6789}
        }
    }

def test_append():
    a = [1,2]
    b = 3
    c = fp.append (b) (a)
    assert a == [1,2]
    assert c == [1,2,3]

# Monads

def test_result():
    maybe = fp.result (lambda x: x is not None)
    t1 = 10
    t2 = None
    r1 = maybe (t1)
    assert r1["ok"] == True
    assert r1["data"] == 10
    r2 = maybe (t2)
    assert r2["ok"] == False
    assert r2["data"] == None

def test_join():
    maybe = fp.result (lambda x: x is not None)
    t1 = 10
    t2 = None
    r1 = maybe (t1)
    assert fp.join (r1) == 10
    r2 = maybe (t2)
    assert fp.join (r2) == None

def test_flatMap():
    a = [fp.left (1), fp.right (2), fp.left (3)]
    assert fp.flatMap (a) == [1, 2, 3]

def test_mapM():
    maybe = fp.result (lambda x: x is not None)
    mult = lambda a: lambda b: a*b
    a = maybe (10)
    b = fp.mapM (mult (2)) (a)
    assert b["ok"] == True
    assert b["data"] == 20
    c = maybe (None)
    d = fp.mapM (mult (2)) (c)
    assert d["ok"] == False
    assert d["data"] == None

def test_chain():
    maybe = fp.result (lambda x: x is not None)
    mult = lambda a: lambda b: fp.result (fp.T) (a*b)
    a = maybe (10)
    b = fp.chain (mult (2)) (a)
    assert b["ok"] == True
    assert b["data"] == 20
    c = maybe (None)
    d = fp.chain (mult (2)) (c)
    assert d["ok"] == False
    assert d["data"] == None

def test_ap():
    maybe = fp.result (lambda x: x is not None)
    mult = lambda a: lambda b: a*b
    a = maybe (2)
    b = maybe (10)
    c = fp.mapM (mult) (a)
    d = fp.ap (c) (b)
    assert d["ok"] == True
    assert d["data"] == 20
    a = maybe (None)
    b = maybe (10)
    c = fp.mapM (mult) (a)
    d = fp.ap (c) (b)
    assert d["ok"] == False
    assert d["data"] == None 
    a = maybe (2)
    b = maybe (None)
    c = fp.mapM (mult) (a)
    d = fp.ap (c) (b)
    assert d["ok"] == False
    assert d["data"] == None
    a = maybe (None)
    b = maybe (None)
    c = fp.mapM (mult) (a)
    d = fp.ap (c) (b)
    assert d["ok"] == False
    assert d["data"] == None 

def test_liftA2():
    maybe = fp.result (lambda x: x is not None)
    mult = lambda a: lambda b: a*b
    a = fp.liftA2 (mult) (maybe (2)) (maybe (10))
    assert a["ok"] == True
    assert a["data"] == 20
    b = fp.liftA2 (mult) (maybe (None)) (maybe (10))
    assert b["ok"] == False
    assert b["data"] == None 
    c = fp.liftA2 (mult) (maybe (2)) (maybe (None))
    assert c["ok"] == False
    assert c["data"] == None 
    d = fp.liftA2 (mult) (maybe (None)) (maybe (None))
    assert d["ok"] == False
    assert d["data"] == None 

def test_onMaybe():
    t = fp.onMaybe (lambda x: x > 5, lambda x: x - 1, lambda x: x + 1)
    r1 = t (3)
    assert r1["ok"] == False
    assert r1["data"] == 2 
    r2 = t (9)
    assert r2["ok"] == True
    assert r2["data"] == 10

def test_either():
    either = fp.either (fp.always (0), lambda x: x + 1)
    assert either (fp.left (33)) == 0
    assert either (fp.right (33)) == 34

def test_safeProp():
    assert fp.safeProp ("nope") ({"name": "brandon"})["ok"] == False
    r = fp.safeProp ("name") ({"name": "brandon"})
    assert r["ok"] == True
    assert r["data"] == "brandon"

def test_safePath():
    t = {"name": "brandon", "address": {"street": "123 Maple"}}
    r = fp.safePath (["nope", "address", "street"]) (t)
    assert r["ok"] == False
    r = fp.safePath (["address", "street"]) (t)
    assert r["ok"] == True
    assert r["data"] == "123 Maple"
    r = fp.safePath (["address"]) (t)
    assert r["ok"] == True
    assert r["data"] == {"street": "123 Maple"}

def test_safeAttr():
    class FakeUser():
        planet = "krypton"

        def __init__(self):
            self.name = "clark"

    assert fp.pick (["ok", "data"]) (fp.safeAttr ("name") (FakeUser())) == {
        "ok": True, "data": "clark"
    }
    assert fp.pick (["ok", "data"]) (fp.safeAttr ("planet") (FakeUser())) == {
        "ok": True, "data": "krypton"
    }
    assert fp.prop ("ok") (fp.safeAttr ("age") (FakeUser())) == False

def test_validate():
    x = {"name": "bob", "cow": "bell"}
    checks = [
        fp.check ("name", lambda x: x!="bob", "can't be bob"),
        fp.check ("age", lambda x: x > 10, "age needs to be more than 10"),
        fp.check ("cow", lambda x: x == "bell", "more cowbell!"),
    ]
    justTheFacts = fp.pick (["ok", "data"])
    assert justTheFacts (fp.validate (x) (checks)) == {
        "ok": False, "data": ["can't be bob", "age needs to be more than 10"]
    }
    assert justTheFacts (fp.validate ({**x, **{"age": 10}}) (checks)) == {
        "ok": False, "data": ["can't be bob", "age needs to be more than 10"]
    }
    good = {"name": "john", "age": 11, "cow": "bell"}
    assert justTheFacts (fp.validate (good) (checks)) == {
        "ok": True, "data": good
    }
