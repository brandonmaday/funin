const {F} = require('./funjs.js')

test("identity", () => {
    expect(F.identity (10)).toBe(10);
    expect(F.identity ("cat")).toBe("cat");
    expect(F.identity (32.2)).not.toBe(32);
});

test("always", () => {
    expect(F.always (10) ()).toBe(10);
    expect(F.always (10) (9)).toBe(10);
    expect(F.always (10) ([9, 11])).toBe(10);
});

test("complement", () => {
    fn = x => x == 1
    expect(F.complement (fn) (1)).toBe(false);
    expect(F.complement (fn) (2)).toBe(true);
});

test("always", () => {
    let a = {};
    expect(F.T()).toBe(true);
    expect(F.T(1)).toBe(true);
    expect(F.T(1,2)).toBe(true);
    expect(F.F()).toBe(false);
    expect(F.F(1)).toBe(false);
    expect(F.F(1,2)).toBe(false);
    expect(F.isNone (null)).toBe(true);
    expect(F.isNone (a.b)).toBe(true);
    expect(F.isNone ("cat")).toBe(false);
    expect(F.notNone (null)).toBe(false);
    expect(F.notNone (a.b)).toBe(false);
    expect(F.notNone ("cat")).toBe(true);
});

test("flip", () => {
    const fn = a => b => `${a}${b}`;
    expect(F.flip (fn) ("b") ("a")).toBe("ab");
});

test("map", () => {
    expect(F.map (x => x+1) ([1,2,3])).toEqual([2,3,4]);
});

test("filter", () => {
    expect(F.filter (x => x!=2) ([1,2,3])).toEqual([1,3]);
});

test("reduce", () => {
    expect(F.reduce ((a, b) => a + b) (0) ([1,2,3])).toEqual(6);
    expect(F.reduce ((a, b) => a + b) (1) ([1,2,3])).toEqual(7);
});

test("compose", () => {
    const addOne = x => x + 1;
    const multFive = x => x * 5;
    expect(F.compose (multFive, addOne) (1)).toEqual(10);
    expect(F.pipe (addOne, multFive) (1)).toEqual(10);
});

test("conditional", () => {
    const isOne = x => x == 1;
    const addOne = x => x + 1;
    expect(F.ifElse (isOne, addOne, x => x) (1)).toEqual(2);
    expect(F.ifElse (isOne, addOne, x => x+2) (5)).toEqual(7);
    expect(F.when (isOne, addOne) (1)).toEqual(2);
    expect(F.unless (isOne, addOne) (1)).toEqual(1);
    expect(F.when (isOne, addOne) (5)).toEqual(5);
    expect(F.unless (isOne, addOne) (5)).toEqual(6);
});

test("both", () => {
    expect(F.both (a => a==1) (a => a==2) (2)).toEqual(false);
    expect(F.both (a => a==2) (a => a==2) (2)).toEqual(true);
    expect(F.both (a => a==2) (a => a==1) (2)).toEqual(false);
});

test("eitherOr", () => {
    expect(F.eitherOr (a => a==1) (a => a==2) (2)).toEqual(true);
    expect(F.eitherOr (a => a==2) (a => a==2) (2)).toEqual(true);
    expect(F.eitherOr (a => a==2) (a => a==1) (2)).toEqual(true);
    expect(F.eitherOr (a => a==2) (a => a==3) (1)).toEqual(false);
});

test("lt", () => {
    expect(F.lt (10) (5)).toEqual(true);
    expect(F.lt (10) (10)).toEqual(false);
    expect(F.lt (10) (15)).toEqual(false);
});

test("gt", () => {
    expect(F.gt (10) (5)).toEqual(false);
    expect(F.gt (10) (10)).toEqual(false);
    expect(F.gt (10) (15)).toEqual(true);
});

test("equals", () => {
    expect(F.equals (10) (5)).toEqual(false);
    expect(F.equals (10) (10)).toEqual(true);
    expect(F.equals (10) (15)).toEqual(false);
});

test("lte", () => {
    expect(F.lte (10) (5)).toEqual(true);
    expect(F.lte (10) (10)).toEqual(true);
    expect(F.lte (10) (15)).toEqual(false);
});

test("gte", () => {
    expect(F.gte (10) (5)).toEqual(false);
    expect(F.gte (10) (10)).toEqual(true);
    expect(F.gte (10) (15)).toEqual(true);
});

test("notEmptyList", () => {
    expect(F.notEmptyList ([])).toEqual(false);
    expect(F.notEmptyList (["a", 123])).toEqual(true);
    expect(F.notEmptyList ("cat")).toEqual(true);
});

test("emptyList", () => {
    expect(F.emptyList ([])).toEqual(true);
    expect(F.emptyList (["a", 123])).toEqual(false);
    expect(F.emptyList ("cat")).toEqual(false);
});

test("head", () => {
    expect(F.head ([1,2,3])).toEqual(1);
    expect(F.head (["bob", 123])).toEqual("bob");
});

test("last", () => {
    expect(F.last ([1,2,3])).toEqual(3);
    expect(F.last (["bob", 123, "cat"])).toEqual("cat");
});

test("nth", () => {
    expect(F.nth (1) ([1,2,3])).toEqual(2);
    expect(F.nth (2) (["bob", 123, "cat"])).toEqual("cat");
});

test("tail", () => {
    expect(F.tail ([1,2,3])).toEqual([2, 3]);
    expect(F.tail (["bob", 123, "cat"])).toEqual([123, "cat"]);
});

test("prop", () => {
    expect(F.prop ("name") ({name: "bob", age: 34})).toEqual("bob");
    expect(F.prop ("age") ({name: "bob", age: 34})).toEqual(34);
});

test("path", () => {
    const fakeUser = {name: "brandon", adr: {street: "123 Maple"}};
    expect(F.path (["adr", "street"]) (fakeUser)).toEqual("123 Maple");
    expect(F.path (["name",]) (fakeUser)).toEqual("brandon");
});

test("pick", () => {
    t1 = {name: "brandon", age: 34, eyeColor: "green"};
    expect(F.pick (["name", "age"]) (t1)).toEqual({name: "brandon", age: 34});
});

test("propEq", () => {
    expect(F.propEq ("name") ("bob") ({name: "bob"})).toEqual(true);
    expect(F.propEq ("name") ("john") ({name: "bob"})).toEqual(false);
});

test("pathEq", () => {
    const t = {"address": {"street": "123"}}
    expect(F.pathEq (["address", "street"]) ("123") (t)).toEqual(true);
    expect(F.pathEq (["address", "street"]) ("bob") (t)).toEqual(false);
});

test("cond", () => {
    const conds = [
        [x => x > 30, x => "gt30"],
        [x => x > 20, x => "gt20"],
        [x => x > 10, x => "gt10"],
        [x => true, x => "default"],
    ];
    const t = {"address": {"street": "123"}}
    expect(F.cond (conds) (10)).toEqual("default");
    expect(F.cond (conds) (20)).toEqual("gt10");
    expect(F.cond (conds) (30)).toEqual("gt20");
});

test("inc", () => {
    expect(F.inc (1)).toEqual(2);
});

test("merge", () => {
    const t = {a: 1, b: 2}
    expect(F.merge (t) ({c: 3})).toEqual({a: 1, b:2, c:3});
    expect(F.merge (t) ({b: 3})).toEqual({a: 1, b:3});
    expect(t).toEqual({a: 1, b:2});
});

test("trim", () => {
    expect(F.trim ("  ")).toEqual("");
    expect(F.trim ("")).toEqual("");
    expect(F.trim (" a ")).toEqual("a");
});

test("assoc", () => {
    const t = {name: "brandon", x: 99};
    expect(F.assoc ("x") (3) (t)).toEqual({name: "brandon", x: 3});
    expect(F.assoc ("age") (34) (t)).toEqual({name: "brandon", x: 99, age: 34});
});

test("evolve", () => {
    const t = {name: "brandon", x: 99};
    expect(F.evolve ("x") (x => x+1) (t)).toEqual({name: "brandon", x: 100});
});

test("evolvePath", () => {
    const t = {name: "brandon", age: 34, address: {
        street: "123 Example", zip4: {zip: 12345, four: 6789}
    }};
    expect(F.evolvePath (["name"]) (n => `${n}1`) (t)).toEqual({
        name: "brandon1", age: 34, address: {
            street: "123 Example", zip4: {zip: 12345, four: 6789}
        }
    });
    expect(F.evolvePath (["address", "zip4", "zip"]) (F.inc) (t)).toEqual({
        name: "brandon", age: 34, address: {
            street: "123 Example", zip4: {zip: 12346, four: 6789}
        }
    });
});

test("assocPath", () => {
    const t = {name: "brandon", age: 34, address: {
        street: "123 Example", zip4: {zip: 12345, four: 6789}
    }};
    expect(F.assocPath (["name"]) ("bob") (t)).toEqual({
        name: "bob", age: 34, address: {
            street: "123 Example", zip4: {zip: 12345, four: 6789}
        }
    });
    expect(F.assocPath (["address", "street"]) ("new street") (t)).toEqual({
        name: "brandon", age: 34, address: {
            street: "new street", zip4: {zip: 12345, four: 6789}
        }
    });
    expect(F.assocPath (["address", "zip4", "zip"]) (99999) (t)).toEqual({
        name: "brandon", age: 34, address: {
            street: "123 Example", zip4: {zip: 99999, four: 6789}
        }
    });
});

test("append", () => {
    let a = [1,2]
    expect(F.append (3) (a)).toEqual([1,2,3]);
    expect(a).toEqual([1,2]);
});

test("result", () => {
    const maybe = F.result (x => x != null);
    const r1 = maybe (10);
    expect(r1.ok).toEqual(true);
    expect(r1.data).toEqual(10);
    const r2 = maybe (null);
    expect(F.resultOk (r2)).toEqual(false);
    expect(r2.data).toEqual(null);
});

test("join", () => {
    const maybe = F.result (x => x != null);
    const r1 = maybe (10);
    expect(F.join (r1)).toEqual(10);
    const r2 = maybe (null);
    expect(F.join (r2)).toEqual(null);
});

test("flatMap", () => {
    const maybe = F.result (x => x != null);
    const a = [maybe (1), maybe (2), maybe (3)];
    expect(F.flatMap (a)).toEqual([1, 2, 3]);
});

test("mapM", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => a*b;
    const a = maybe (10);
    const b = F.mapM (mult (2)) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(20);
    const c = maybe (null);
    const d = F.mapM (mult (2)) (c)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
});

test("mapMLeft", () => {
    const maybe = F.result (x => x != null)
    makeBob = a => "bob"
    a = maybe (10)
    b = F.mapMLeft (makeBob) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(10);
    const c = maybe (null);
    const d = F.mapMLeft (makeBob) (c);
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual("bob");
});

test("chain", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => F.result (F.T) (a*b);
    const a = maybe (10);
    const b = F.chain (mult (2)) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(20);
    const c = maybe (null);
    const d = F.chain (mult (2)) (c)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
});

test("chainLeft", () => {
    const maybe = F.result (x => x != null);
    makeBob = a => ({ok: true, data: "bob"})
    a = maybe (10)
    b = F.chainLeft (makeBob) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(10);
    c = maybe (null)
    d = F.chainLeft (makeBob) (c)
    expect(d.ok).toEqual(true);
    expect(d.data).toEqual("bob");
});

test("ap", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => (a*b);
    let a = maybe (2);
    let b = maybe (10);
    let c = F.mapM (mult) (a)
    let d = F.ap (c) (b)
    expect(d.ok).toEqual(true);
    expect(d.data).toEqual(20);
    a = maybe (null);
    b = maybe (10);
    c = F.mapM (mult) (a)
    d = F.ap (c) (b)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
    a = maybe (2);
    b = maybe (null);
    c = F.mapM (mult) (a)
    d = F.ap (c) (b)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
    a = maybe (null);
    b = maybe (null);
    c = F.mapM (mult) (a)
    d = F.ap (c) (b)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
});

test("liftA2", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => (a*b);
    let a = F.liftA2 (mult) (maybe (2)) (maybe (10));
    expect(a.ok).toEqual(true);
    expect(a.data).toEqual(20);
    a = F.liftA2 (mult) (maybe (null)) (maybe (10));
    expect(a.ok).toEqual(false);
    expect(a.data).toEqual(null);
    a = F.liftA2 (mult) (maybe (2)) (maybe (null));
    expect(a.ok).toEqual(false);
    expect(a.data).toEqual(null);
    a = F.liftA2 (mult) (maybe (null)) (maybe (null));
    expect(a.ok).toEqual(false);
    expect(a.data).toEqual(null);
});

test("either", () => {
    const either = F.either (F.always (0), x => x + 1);
    expect(either (F.left (33))).toEqual(0);
    expect(either (F.right (33))).toEqual(34);
});

test("onMaybe", () => {
    const t = F.onMaybe (x => x > 5, x => x - 1, x => x + 1);
    const r1 = t(3)
    expect(r1.ok).toEqual(false);
    expect(r1.data).toEqual(2);
    const r2 = t(9)
    expect(r2.ok).toEqual(true);
    expect(r2.data).toEqual(10);
});

test("safeProp", () => {
    expect(F.safeProp ("nope") ({name: "bob", age: 34}).ok).toEqual(false);
    expect(F.safeProp ("name") ({name: "bob", age: 34}).ok).toEqual(true);
    expect(F.safeProp ("name") ({name: "bob", age: 34}).data).toEqual("bob");
});

test("safePath", () => {
    const t = {name: "brandon", address: {street: "123 Maple"}}
    let r = F.safePath (["nope", "address", "street"]) (t)
    expect(r.ok).toEqual(false);
    r = F.safePath (["address", "street"]) (t)
    expect(r.ok).toEqual(true);
    expect(r.data).toEqual("123 Maple");
    r = F.safePath (["address"]) (t)
    expect(r.ok).toEqual(true);
    expect(r.data).toEqual({street: "123 Maple"});
});

test("validate", () => {
    const x = {name: "bob", cow: "bell"};
    const checks = [
        F.check ("name", x => x!="bob", "can't be bob"),
        F.check ("age", x => x > 10, "age needs to be more than 10"),
        F.check ("cow", x => x=="bell", "more cowbell!"),
    ];
    const justTheFacts = F.pick (["ok", "data"]);
    expect(justTheFacts (F.validate (x) (checks))).toEqual({
        ok: false, data: ["can't be bob", "age needs to be more than 10"]
    });
    expect(justTheFacts (F.validate ({...x, ...{age: 10}}) (checks))).toEqual({
        ok: false, data: ["can't be bob", "age needs to be more than 10"]
    });
    const good = {name: "john", age: 11, cow: "bell"};
    expect(justTheFacts (F.validate (good) (checks))).toEqual({
        ok: true, data: good
    });
});
