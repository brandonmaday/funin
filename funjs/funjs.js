var F = {};
/*
 TYPES 

Result = {
  ok: bool
  data: Any
}

Unary = (a) -> a

Mapable = Union [Array, Result]
*/


// IDENTITIES


// identity : a -> a
F.identity = x => x;

// always : a -> * -> a
F.always = a => (...b) => a;

// T : a -> * -> Boolean
F.T = F.always (true);

// F : a -> * -> Boolean
F.F = F.always (false);


// MONADS


// result : (a -> Boolean) -> a -> Result
F.result = fn => data => ({ok: fn (data), data});

// join : Result -> a
F.join = a => a.data;

// left : a -> Result
F.left = F.result (F.F);

// right : a -> Result
F.right = F.result (F.T);

// either : (Unary, Unary) -> Result -> a
F.either = (badFn, goodFn) => res => {
    data = F.join (res);
    return (res.ok == false) ? badFn (data) : goodFn (data);
}

// orElse : (Unary) -> Result -> a
F.orElse = fn => F.either (fn, F.identity);


// HIGHER ORDER FUNCTIONS


// flip : (a -> b -> c) -> b -> a -> c
F.flip = fn => b => a => fn (a) (b);

// filter : (a -> Boolean) -> [a] -> [a]
F.filter = fn => arr => arr.filter(fn);

// reduce :: (a -> b -> a) -> a -> [b] -> a
F.reduce = fn => init => arr => arr.reduce(fn, init);

// compose : ((y -> z) ... (a -> b)) -> a -> z
F.compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

// _mapList : (a -> b) -> [a] -> [b]
F._mapList = fn => arr => arr.map(fn);

// _mapResult : (a -> b) -> Result a -> Result b
F._mapResult = fn => F.either (F.left, F.compose (F.right, fn));

// map : Unary -> Mapable -> Mapable
F.map = fn => mapable => {
    const mapFn = (Array.isArray(mapable)) ? F._mapList : F._mapResult;
    return mapFn (fn) (mapable);
}

// chain : (a -> Result) -> Result -> Result
F.chain = fn => F.either (F.left, fn);

// ap : Result [a -> b] -> Result [a] -> Result [c]
F.ap = fnInResult => param2InResult => {
    if (fnInResult.ok == false) { return fnInResult; }
    const fn = F.join (fnInResult);
    return F.map (fn) (param2InResult);
}

// liftA2 : (a -> b -> c) -> Result [a] -> Result [b] -> Result [c]
F.liftA2 = fn => r1 => r2 => F.ap (F.map (fn) (r1)) (r2);


// CREATORS


// merge : {a} -> {b} -> {ab}
F.merge = f => g => ({...f, ...g});

// assoc : a -> b -> {c} -> {c}
F.assoc = key => val => obj => {
    x = {};
    x[key] = val;
    return F.merge (obj) (x);
};


// SAFE ACCESSORS


// prop : a -> {b} -> Result
F.prop = k => o => {
    const v = o [k];
    return (v === undefined) ? F.left (k) : F.right (v);
}

// tail : [a] -> [a]
F.tail = arr => arr.slice(1);

// nth :: a -> [b] -> Result
F.nth = idx => arr => F.prop (idx) (arr);

// head : [a] -> a
F.head = F.nth (0);

// last : [a] -> a
F.last = arr => F.nth (arr.length-1) (arr);


// SAFE ACCESS TO CREATE


// evolve : a -> (b -> c) -> {d} -> Result
F.evolve = k => fn => o => {
    return F.compose (
        F.map (F.flip (F.assoc (k)) (o)),
        F.map (fn),
        F.prop (k)
    ) (o);
}


// TAIL RECURSION


// COMPARISIONS


// equals : a -> b -> Boolean
F.equals = a => b => (b === a) ? true : false;


// TRANSDUCERS


// AJAX


// asyncCompose : ((y -> z) ... (a -> b)) -> a -> z
F.asyncCompose = (...fns) => x =>
    fns.reduceRight((v, f) => Promise.resolve(v).then(f), x);

// jaxCfg : a -> b -> {ab}
F.jaxCfg = method => data => ({
    method,
    body: JSON.stringify(data),
    cache: "no-cache",
    headers: new Headers({"content-type": "application/json"}),
    credentials: "same-origin",
});

// jaxResult : ResponseResult [Json [Result]] -> Result
F.jaxResult = F.either (
    F.asyncCompose (F.left, r => r.statusText),
    r => r.json().catch(_ => F.left ("JSON Error")),
);

// jax : a -> b -> c -> Result
F.jax = method => uri => F.asyncCompose (
    F.jaxResult,
    data => fetch(uri, F.jaxCfg (method) (data))
)

// jaxNoData : a -> b -> Result
F.jaxNoData = method => uri => F.jax (method) (uri) (undefined);

// jaxGet : a -> Result
F.jaxGet = F.jaxNoData ("GET");

// jaxDelete : a -> Result
F.jaxDelete = F.jaxNoData ("DELETE");

// jaxPost : a -> Result
F.jaxPost = F.jax ("POST");

// jaxPut : a -> Result
F.jaxPut = F.jax ("PUT");


// BOOTSTRAP FOR NODE


try { exports.F = F; } catch {}
