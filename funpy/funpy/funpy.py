# Identities
""" identity :: a -> a """
identity = lambda x: x

""" always :: a -> * -> a """
always = lambda a: lambda *b: a

""" defer :: (a -> b) -> a -> * -> b """
defer = lambda fn: lambda val: lambda *x: fn(val)

""" complement :: (a -> Boolean) -> a -> Boolean """
complement = lambda fn: lambda a: not fn(a)

""" T :: a -> * -> Boolean """
T = always(True)

""" F :: a -> * -> Boolean """
F = always(False)

""" isNone :: a -> Boolean """
isNone = lambda a: a is None

""" notNone :: a -> boolean """
notNone = complement (isNone)

""" flip :: (a -> b -> c) -> b -> a -> c """
flip = lambda fn: lambda b: lambda a: fn (a) (b)

# higher order functions
""" map :: (a -> b) -> [a] -> [b] """
map = lambda fn: lambda arr: [fn(a) for a in arr]

""" filter :: (a -> Boolean) -> [a] -> [a] """
filter = lambda fn: lambda arr: [a for a in arr if fn(a)]

""" reduce :: (a -> b -> a) -> a -> [b] -> a"""
from functools import reduce as _reduce
reduce = lambda fn: lambda init: lambda arr: _reduce(fn, arr, init)

# Composition
""" compose2 :: ((b -> c), (a -> b)) -> a -> c """
compose2 = lambda f, g: lambda x: f(g(x))

initCompose = reduce (compose2) (identity)

""" compose :: ((y -> z) ... (a -> b)) -> a -> z """
compose = lambda *fns: initCompose (fns)

""" pipe :: ((a -> b) ... (y -> z)) -> a -> z """
pipe = lambda *fns: initCompose (fns[::-1])

# Conditions
""" ifElse :: ((a -> Boolean), (a -> b), (a -> c)) -> a -> b | c """
ifElse = lambda pred, ok, notOk: lambda a: ok(a) if pred(a) else notOk(a)

""" when :: ((a -> Boolean), (a -> b)) -> a -> b | a """
when = lambda pred, ok: ifElse(pred, ok, identity)

""" unless :: ((a -> Boolean), (a -> b)) -> a -> a | b """
unless = lambda pred, notOk: ifElse(pred, identity, notOk)

""" both :: (a -> Boolean) -> (a -> Boolean) -> a -> Boolean """
both = lambda fn1: lambda fn2: lambda a: fn1(a) and fn2(a)

""" eitherOr :: (a -> Boolean) -> (a -> Boolean) -> a -> Boolean """
eitherOr = lambda fn1: lambda fn2: lambda a: fn1(a) or fn2(a)

""" lt :: a -> b -> Boolean """
lt = lambda a: lambda b: b < a

""" gt :: a -> b -> Boolean """
gt = lambda a: lambda b: b > a

""" equals :: a -> b -> Boolean """
equals = lambda a: lambda b: a == b

""" lte :: a -> b -> Boolean """
lte = lambda a: eitherOr (equals (a)) (lt (a))

""" gte :: a -> b -> Boolean """
gte = lambda a: eitherOr (equals (a)) (gt (a))

""" isList :: [a] -> Boolean """
isList = compose(equals (list), type)

""" notEmptyList :: [a] -> Boolean """
notEmptyList = both (isList) (compose(gt (0), len))

""" emptyList :: [a] -> Boolean """
emptyList = both (isList) (compose(equals (0), len))

# Accessors
""" head :: [a] -> a """
head = lambda arr: arr[0]

""" last :: [a] -> a """
last = lambda arr: arr[-1]

""" nth :: a -> [b] -> b """
nth = lambda idx: lambda arr: arr[idx]

""" tail :: [a] -> [a] """
tail = lambda arr: arr[1:]

""" prop :: a -> {b} -> b[a] """
prop = lambda a: lambda b: b[a]

""" path :: [a] -> {b} -> b[a[0]]...[a[-1]] """
path = lambda keys: lambda obj: reduce (lambda a, b: prop (b) (a)) (obj) (keys)

""" attr :: a -> b -> b.a """
attr = lambda name: lambda cls: getattr(cls, name)

""" pick :: [a] -> {b} -> {b} """
pick = lambda keys: lambda obj: {k: v for k, v in obj.items() if k in keys}

# Access and Compare
""" propEq :: a -> b -> {c} -> Boolean """
propEq = lambda key: lambda val: compose(equals (val), prop (key))

""" pathEq :: [a] -> b -> {c} -> Boolean """
pathEq = lambda keys: lambda val: compose(equals (val), path (keys))

""" cond :: [[(a -> Boolean), (a -> b)]] -> a -> b """
cond = lambda conds: lambda x: ifElse(
    compose(head, head)(conds),
    compose(last, head)(conds),
    cond(tail(conds))
)(x)

# Operations
""" inc :: a -> b """
inc = lambda x: x + 1

""" merge :: {a} -> {b} -> {ab} """
merge = lambda f: lambda g: {**f, **g}

""" trim :: a -> b """
trim = lambda x: x.strip()

""" assoc :: a -> b -> {c} -> {c} """
assoc = lambda key: lambda val: lambda obj: merge (obj) ({key: val})

""" evolve :: a -> (b -> c) -> {d} -> {dc} """
evolve = lambda k: lambda f: lambda o: assoc (k) (f(prop (k) (o))) (o)

""" evolvePath :: [a] -> (b -> c) -> {d} -> {dc} """
evolvePath = lambda keys: lambda fn: lambda obj: compose(
    lambda v: assoc (head (keys)) (v) (obj),
    ifElse(
        compose(lte (1), len),
        compose(fn, flip (prop) (obj), head),
        compose(evolvePath (tail (keys)) (fn), flip (prop) (obj), head)
    )
)(keys)

""" assocPath :: [a] -> b -> {c} -> {c} """
assocPath = lambda keys: lambda val: evolvePath (keys) (always (val))

""" append :: a -> [a] -> [a] """
append = lambda item: lambda arr: arr + [item]

# Monads (Generic)
""" result :: (a -> Boolean) -> a -> m a """
result = lambda fn: lambda data: {"ok": fn (data), "data": data}

""" left :: a -> m a """
left = result (F)

""" right :: a -> m a """
right = result (T)

""" resultOk :: m a -> Boolean """
resultOk = propEq ("ok") (True)

""" join :: m a -> a """
join = prop ("data")

""" flatMap :: [m a] -> [a] """
flatMap = map (join)

""" mapM :: (a -> b) -> m a -> m b """
""" mapM :: (a -> b -> c) -> m a -> m (b -> c) """
mapM = lambda fn: lambda m: when(
    resultOk,
    compose (flip (assoc ("data")) (m), fn, join)
)(m)

""" chain :: (a -> m b) -> m a -> m b """
chain = lambda fn: when(resultOk, compose(join, mapM (fn)))

""" ap :: m (a -> b) -> m a -> m b """
ap = lambda mFn: lambda m: when(
    resultOk,
    compose(flip (mapM) (m), join)
)(mFn)

""" liftA2 :: (a -> b -> c) -> m a -> m b -> m c """
liftA2 = lambda fn: lambda ma: lambda mb: compose(
    flip (ap) (mb),
    mapM (fn)
)(ma)

# Monads (Maybe)
""" onMaybe :: ((a -> Boolean), (a -> b), (a -> c)) -> a -> m b|c """
onMaybe = lambda pred, bad, good: compose(
    either (compose(left, bad), compose(right, good)),
    result (pred)
)

# Monads (Either)
""" either :: ((a -> c), (b -> c)) -> m a|b -> c """
either = lambda notOk, ok: lambda m: compose(
    ifElse(always (resultOk (m)), ok, notOk), join
)(m)

# Monads (Validaion)
""" check :: a -> (b -> Boolean) -> c -> abc """
check = lambda p, fn, msg: {"p": p, "fn": fn, "msg": msg}

""" safeProp :: a -> b -> Either None|b[a] """
safeProp = lambda k: lambda o: right (prop (k) (o)) if k in o else left (None)

""" safePath :: [a] -> {b} -> m {b} """
safePath = lambda keys: lambda obj: reduce (
    lambda obj, key: chain (safeProp (key)) (obj)
) (right(obj)) (keys)

""" safeAttr :: a -> b -> m b.a """
safeAttr = lambda name: lambda cls: result (lambda x: x is not None) (
    getattr(cls, name, None))

""" validate :: a -> [b] -> m a """
validate = lambda data: pipe(
    reduce (
        lambda results, check: pipe(
            safeProp (prop ("p") (check)),
            chain (result (prop ("fn") (check))),
            either (compose(left, always (prop ("msg") (check))), right),
            flip (append) (results)
        )(data)
    )([]),
    filter (complement(resultOk)),
    flatMap,
    ifElse(emptyList, compose(right, always (data)), left)
)
