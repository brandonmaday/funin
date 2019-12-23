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

test("truefalse", () => {
    let a = {};
    expect(F.T()).toBe(true);
    expect(F.T(1)).toBe(true);
    expect(F.T(1,2)).toBe(true);
    expect(F.F()).toBe(false);
    expect(F.F(1)).toBe(false);
    expect(F.F(1,2)).toBe(false);
});

test("result", () => {
    const maybe = F.result (x => x != null);
    const r1 = maybe (10);
    expect(r1.ok).toEqual(true);
    expect(r1.data).toEqual(10);
    const r2 = maybe (null);
    expect(r2.ok).toEqual(false);
    expect(r2.data).toEqual(null);
});

test("join", () => {
    const maybe = F.result (x => x != null);
    const r1 = maybe (10);
    expect(F.join (r1)).toEqual(10);
    const r2 = maybe (null);
    expect(F.join (r2)).toEqual(null);
});

test("either", () => {
    const either = F.either (F.always (0), x => x + 1);
    expect(either (F.left (33))).toEqual(0);
    expect(either (F.right (33))).toEqual(34);
});

test ("orElse", () => {
    const res = F.result (a => (a==2) ? true : false);
    expect (F.orElse (x => "hi") (res (2))).toEqual (2);
    expect (F.orElse (x => "hi") (res (4))).toEqual ("hi");
});

test("flip", () => {
    const fn = a => b => `${a}${b}`;
    expect(F.flip (fn) ("b") ("a")).toBe("ab");
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
});

test("mapList", () => {
    expect(F._mapList (x => x+1) ([1,2,3])).toEqual([2,3,4]);
});

test("mapResult", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => a*b;
    const a = maybe (10);
    const b = F._mapResult (mult (2)) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(20);
    const c = maybe (null);
    const d = F._mapResult (mult (2)) (c)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
});

test("map", () => {
    expect(F.map (x => x+1) ([1,2,3])).toEqual([2,3,4]);
    const maybe = F.result (x => x != null);
    const mult = a => b => a*b;
    const a = maybe (10);
    const b = F.map (mult (2)) (a)
    expect(b.ok).toEqual(true);
    expect(b.data).toEqual(20);
    const c = maybe (null);
    const d = F.map (mult (2)) (c)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
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

test("ap", () => {
    const maybe = F.result (x => x != null);
    const mult = a => b => (a*b);
    let a = maybe (2);
    let b = maybe (10);
    let c = F.map (mult) (a)
    let d = F.ap (c) (b)
    expect(d.ok).toEqual(true);
    expect(d.data).toEqual(20);
    a = maybe (null);
    b = maybe (10);
    c = F.map (mult) (a)
    d = F.ap (c) (b)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
    a = maybe (2);
    b = maybe (null);
    c = F.map (mult) (a)
    d = F.ap (c) (b)
    expect(d.ok).toEqual(false);
    expect(d.data).toEqual(null);
    a = maybe (null);
    b = maybe (null);
    c = F.map (mult) (a)
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

test("merge", () => {
    const t = {a: 1, b: 2}
    expect(F.merge (t) ({c: 3})).toEqual({a: 1, b:2, c:3});
    expect(F.merge (t) ({b: 3})).toEqual({a: 1, b:3});
    expect(t).toEqual({a: 1, b:2});
});

test("assoc", () => {
    const t = {name: "brandon", x: 99};
    expect(F.assoc ("x") (3) (t)).toEqual({name: "brandon", x: 3});
    expect(F.assoc ("age") (34) (t)).toEqual({name: "brandon", x: 99, age: 34});
});

test("prop", () => {
    expect(F.prop ("nope") ({name: "bob", age: 34}).ok).toEqual(false);
    expect(F.prop ("name") ({name: "bob", age: 34}).ok).toEqual(true);
    expect(F.prop ("name") ({name: "bob", age: 34}).data).toEqual("bob");
});

test("tail", () => {
    expect(F.tail ([1,2,3])).toEqual([2, 3]);
    expect(F.tail (["bob", 123, "cat"])).toEqual([123, "cat"]);
});

test("nth", () => {
    expect(F.nth (1) ([1,2,3])).toEqual({ok: true, data: 2});
    expect(F.nth (2) (["bob", 123, "cat"])).toEqual({ok: true, data: "cat"});
    expect(F.nth (20) ([1,2])).toEqual({ok: false, data: 20});
});

test("head", () => {
    expect(F.head ([1,2,3])).toEqual({ok: true, data: 1});
    expect(F.head (["bob", 123])).toEqual({ok: true, data: "bob"});
    expect(F.head ([])).toEqual({ok: false, data: 0});
});

test("last", () => {
    expect(F.last ([1,2,3])).toEqual({ok: true, data: 3});
    expect(F.last ([])).toEqual({ok: false, data: -1});
});

test("evolve", () => {
    const t = {name: "brandon", x: 99};
    expect(F.evolve ("x") (x => x+1) (t)).toEqual({
        ok: true, data: {name: "brandon", x: 100}
    });
    expect(F.evolve ("y") (x => x+1) (t)).toEqual({
        ok: false, data: "y"
    });
});

test("equals", () => {
    expect(F.equals (10) (5)).toEqual(false);
    expect(F.equals (10) (10)).toEqual(true);
    expect(F.equals (10) (15)).toEqual(false);
});

test ("asyncCompose", async () => {
    const sleep = a => new Promise (res => setTimeout(_ => res (a), 500));
    const ans = await F.asyncCompose (a => a + 10, sleep) (10)
    expect (ans).toBe (20);
});
