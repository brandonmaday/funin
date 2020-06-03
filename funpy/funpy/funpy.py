from typing import NamedTuple, Any, Callable, List, Union, Dict
from functools import reduce as _reduce

# TYPES

Unary = Callable[[Any], Any]

class Result(NamedTuple):
    """ The only Monad you'll ever need """
    ok: bool
    data: Any

Mappable = Union[List[Any], Result]

# HIGHER ORDER FUNCTIONS

def curry(fn):
    """ Cache function arguments """
    cache = []
    arity = fn.__code__.co_argcount
    def wrap(*args):
        """ Checks if enough args and runs function """
        new_cache = [*cache, *args]
        if len(new_cache) >= arity:
            return fn(*new_cache)
        return lambda *more: wrap(*new_cache, *more)
    return wrap

@curry
def flip(fn: Callable[[Any,Any], Any], a1: Any, a2: Any) -> Any:
    return fn(a2, a1)

@curry
def filter(fn: Callable[[Any], bool], arr: List[Any]) -> List[Any]:
    return [a for a in arr if fn(a)]

@curry
def reduce(fn: Callable[[Any, Any], Any], default: Any, arr: List[Any]) -> Any:
    return _reduce(fn, arr, default)

def compose(*fns: Callable) -> Callable [[Any], Any]:
    return reduce(
        lambda f, g: lambda x: f(g(x)),
        lambda x: x,
        fns
    )

# IDENTITY

def identity(a: Any) -> Any:
    return a

@curry
def always(a: Any, *ignore: Any) -> Any:
    return a

# MONADS

def left(a: Any) -> Result:
    """ A failed result """
    return Result(False, a)

def right(a: Any) -> Result:
    """ A good result """
    return Result(True, a)


@curry
def map_list(fn: Unary, arr: List[Any]) -> List[Any]:
    return [fn(a) for a in arr]

@curry
def map_result(fn: Unary, result: Result) -> Result:
    if result.ok == True:
        return right(fn(result.data))
    return result

@curry
def map(fn: Unary, mappable: Mappable) -> Mappable:
    if isinstance(mappable, list):
        return map_list(fn, mappable)
    return map_result(fn, mappable)

def chain(fn: Unary, result: Result) -> Any:
    if result.ok == True:
        return fn(result.data)
    return result

@curry
def ap(fnInResult: Result, paramInResult: Result) -> Result:
    """ A way to apply Results to a curried function """
    if fnInResult.ok == False:
        return fnInResult
    return map(fnInResult.data, paramInResult)

@curry
def liftA2(fn: Callable[[Any, Any], Any], r1: Result, r2: Result) -> Result:
    """ Map and Ap glued together """
    return ap(map(fn, r1), r2)

@curry
def either(ifBad: Unary, ifGood: Unary, result: Result) -> Any:
    if result.ok == False:
        return ifBad(result.data)
    return ifGood(result.data)

@curry
def or_else(fn: Unary, result: Result) -> Any:
    if result.ok == False:
        return fn(result.data)
    return result.data

# CREATORS

@curry
def merge(d1: Dict[Any,Any], d2: Dict[Any,Any]) -> Dict[Any,Any]:
    return {**d1, **d2}

@curry
def assoc(key: Any, val: Any, d: Dict[Any,Any]) -> Dict[Any,Any]:
    return merge(d, {key: val})

# SAFE ACCESSORS

@curry
def prop(key: Any, d: Dict[Any,Any]) -> Result:
    try:
        return right(d[key])
    except KeyError:
        return left(key)

@curry
def tail(l: List[Any]) -> List[Any]:
    return l[1:]

@curry
def nth(i: int, l: List[Any]) -> Result:
    try:
        return right(l[i])
    except IndexError:
        return left(i)

head = nth(0)
last = nth(-1)

# SAFE ACCESS TO CREATE

@curry
def evolve(key: Any, fn: Unary, d: Dict[Any, Any]) -> Result:
    return map(flip(assoc(key), d), map(fn, prop(key, d)))

# TAIL RECURSION

def tail_r(fn, *args, **kwargs):
    """
    Caches arguments from being applied to a function that calls itself
    Returns a function that can be checked for 'callable' which takes no arguments
    """
    return lambda: fn(*args, **kwargs)

def bounce(fn, *args, **kwargs):
    """
    Applys initial arguments to a function that could return a tail_r function
    Keeps calling tail_r functions until a non callable is returned
    Prevents stack overflow
    """
    result = fn(*args, **kwargs)
    while(callable(result)):
        result = result()
    return result
