from typing import TypedDict, Any, Callable, Union


# TYPES


class Result (TypedDict):
    ok: bool
    data: Any

Unary = Callable [[Any], Any]

Mapable = Union [list, Result]


# IDENTITIES


def identity (a: Any) -> Any:
    return a

def always (a: Any) -> Unary:
    def wrap (b: Any) -> Any:
        return a
    return wrap

F = always (False)
T = always (True)


# MONADS


def result (fn: Callable [[Any], bool]) -> Callable [[Any], Result]:
    def wrap (a: Any) -> Result:
        return {"ok": fn (a), "data": a}
    return wrap

def join (res: Result) -> Any:
    return res ["data"]

left = result (F)
right = result (T)

def either (badFn: Unary, goodFn: Unary) -> Callable [[Result], Any]:
    def wrap (res: Result) -> Any:
        data = join (res)
        return badFn (data) if res ["ok"] == False else goodFn (data)
    return wrap


# HIGHER ORDER FUNCTIONS


flip = lambda fn: lambda a: lambda b: fn (b) (a)

def filter (fn: [[Any], bool]) -> Callable [[list], list]:
    def wrap (arr: list) -> list:
        return [a for a in arr if fn (a)]
    return wrap

from functools import reduce as _reduce
def reduce (fn: Callable [[Any, Any], Any]) -> Callable [
    [Any], Callable [[list], Any]
]:
    def init (a: Any) -> Callable [[list], Any]:
        def wrap (arr: list) -> Any:
            return _reduce (fn, arr, a)
        return wrap
    return init

def _compose2 (f: Unary, g: Unary) -> Unary:
    def wrap (x: Any) -> Any:
        return f (g (x))
    return wrap

def compose (*fns) -> Unary:
    def wrap (a: Any) -> Any:
        return reduce (_compose2) (identity) (fns) (a)
    return wrap

def _mapList (fn: Unary) -> Callable [[list], list]:
    def wrap (arr: list) -> list:
        return [fn (a) for a in arr]
    return wrap

def _mapResult (fn: Unary) -> Callable [[Result], Result]:
    def wrap (res: Result) -> Result:
        return either (left, compose (right, fn)) (res)
    return wrap

def map (fn: Unary) -> Callable [[Mapable], Mapable]:
    def wrap (mapable: Mapable) -> Mapable:
        mapFn = _mapList if isinstance (mapable, list) else _mapResult
        return mapFn (fn) (mapable)
    return wrap

def chain (fn: Callable [[Any], Result]) -> Callable [[Result], Result]:
    def wrap (res: Result) -> Result:
        return either (left, fn) (res)
    return wrap

def ap (fnInResult: Result) -> Callable [[Result], Result]:
    def wrap (param2InResult: Result) -> Result:
        if fnInResult ["ok"] == False:
            return fnInResult
        fn = join (fnInResult)
        return map (fn) (param2InResult)
    return wrap

def liftA2 (
    fn: Callable [[Any, Any], Any]
) -> Callable [[Result], Callable [[Result], Result]]:
    def wrapA (resultA: Result) -> Callable [[Result], Result]:
        def wrapB (resultB: Result) -> Result:
            a = map (fn) (resultA)
            return ap (a) (resultB)
        return wrapB
    return wrapA


# CREATORS


def merge (a: dict) -> Callable [[dict], dict]:
    def wrap (b: dict) -> dict:
        return {**a, **b}
    return wrap

def assoc (key: Any) -> Callable [[Any], Callable [[dict], dict]]:
    def wrap (val: Any) -> Callable [[dict], dict]:
        return flip (merge) ({key: val})
    return wrap


# SAFE ACCESSORS


def prop (key: Any) -> Callable [[dict], Result]:
    def wrap (obj: dict) -> Result:
        try:
            return right (obj [key])
        except KeyError:
            return left (key)
    return wrap

def tail (arr: list) -> list:
    return arr [1:]

def nth (idx: int) -> Callable [[list], Result]:
    def wrap (arr: list) -> Result:
        try:
            return right (arr [idx])
        except IndexError:
            return left (idx)
    return wrap

head = nth (0)

last = nth (-1)


# SAFE ACCESS TO CREATE


def evolve (key: Any) -> Callable [[Unary], Callable [[dict], dict]]:
    update = flip (assoc (key))
    def withFn (fn: Unary) -> Callable [[dict], dict]:
        def wrap (obj: dict) -> dict:
            return compose (map (update (obj)), map (fn), prop (key)) (obj)
        return wrap
    return withFn


# TAIL RECURSION


def tailR (fn):
    def wrap (*args, **kwargs):
        return lambda: fn (*args, **kwargs)
    return wrap

def bounce (fn):
    def wrap (*args, **kwargs):
        result = fn (*args, **kwargs)
        while (callable (result)):
            result = result ()
        return result
    return wrap


# TRANSDUCERS

