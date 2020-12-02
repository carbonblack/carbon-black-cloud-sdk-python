#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
LRU cache based on stucchio's py-lru-cache module

original copy at https://github.com/stucchio/Python-LRU-cache licensed under MIT
"""

try:
    from collections import OrderedDict
except ImportError:
    # Python 2.6 compatibility
    from ordereddict import OrderedDict

from itertools import islice
import time
import threading
import weakref


def lru_cache_function(max_size=1024, expiration=15 * 60):
    """
    Least recently used cache function

    >>> @lru_cache_function(3, 1)
    ... def f(x):
    ...    print "Calling f(" + str(x) + ")"
    ...    return x
    >>> f(3)
    Calling f(3)
    3
    >>> f(3)
    3
    """

    def wrapper(func):
        return LRUCachedFunction(func, LRUCacheDict(max_size, expiration))

    return wrapper


def _lock_decorator(func):
    """
    Lock Decorator

    If the LRUCacheDict is concurrent, then we should lock in order to avoid
    conflicts with threading, or the ThreadTrigger.
    """

    def withlock(self, *args, **kwargs):
        if self.concurrent:
            with self._rlock:
                return func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    withlock.__name__ == func.__name__
    return withlock


class LRUCacheDict(object):
    """
    A dictionary-like object, supporting LRU caching semantics.

    >>> d = LRUCacheDict(max_size=3, expiration=3)
    >>> d['foo'] = 'bar'
    >>> d['foo']
    'bar'
    >>> import time
    >>> time.sleep(4) # 4 seconds > 3 second cache expiry of d
    >>> d['foo']
    Traceback (most recent call last):
        ...
    KeyError: 'foo'
    >>> d['a'] = 'A'
    >>> d['b'] = 'B'
    >>> d['c'] = 'C'
    >>> d['d'] = 'D'
    >>> d['a'] # Should return value error, since we exceeded the max cache size
    Traceback (most recent call last):
        ...
    KeyError: 'a'

    By default, this cache will only expire items whenever you poke it - all methods on
    this class will result in a cleanup. If the thread_clear option is specified, a background
    thread will clean it up every thread_clear_min_check seconds.

    If this class must be used in a multithreaded environment, the option concurrent should be
    set to true. Note that the cache will always be concurrent if a background cleanup thread
    is used.
    """

    def __init__(self, max_size=1024, expiration=15 * 60, thread_clear=False, concurrent=True):
        """
        Initialize the LRUCacheDict object.

        Args:
            max_size (int): Maximum number of elements in the cache.
            expiration (int): Number of seconds an item can be in the cache before it expires.
            thread_clear (bool): True if we want to use a background thread to keep the cache clear.
            concurrent (bool): True to make access to the cache thread-safe.
        """
        self.max_size = max_size
        self.expiration = expiration

        self.__values = {}
        self.__expire_times = OrderedDict()
        self.__access_times = OrderedDict()
        self.thread_clear = thread_clear
        self.concurrent = concurrent or thread_clear
        if self.concurrent:
            self._rlock = threading.RLock()
        if thread_clear:
            t = self.EmptyCacheThread(self)
            t.start()

    class EmptyCacheThread(threading.Thread):
        """Background thread that expires elements out of the cache."""
        daemon = True

        def __init__(self, cache, peek_duration=60):
            """
            Initialize the EmptyCacheThread.

            Args:
                cache (LRUCacheDict): The cache to be monitored.
                peek_duration (int): The delay between "sweeps" of the cache.
            """
            me = self

            def kill_self(o):
                me

            self.ref = weakref.ref(cache)
            self.peek_duration = peek_duration
            super(LRUCacheDict.EmptyCacheThread, self).__init__()

        def run(self):
            """Execute the background cleanup."""
            while self.ref():
                c = self.ref()
                if c:
                    next_expire = c.cleanup()
                    if (next_expire is None):
                        time.sleep(self.peek_duration)
                    else:
                        time.sleep(next_expire + 1)
                c = None

    @_lock_decorator
    def size(self):
        """Returns the number of values in the dictionary."""
        return len(self.__values)

    @_lock_decorator
    def clear(self):
        """
        Clears the dict.

        >>> d = LRUCacheDict(max_size=3, expiration=1)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> d.clear()
        >>> d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        self.__values.clear()
        self.__expire_times.clear()
        self.__access_times.clear()

    def __contains__(self, key):
        """
        Tests if a key is in the dictionary.

        Args:
            key (Any): The key to be looked up.

        Returns:
            bool: True if the key is in the dictionary, False if not.
        """
        return key in self

    @_lock_decorator
    def has_key(self, key):
        """
        Determines if a key exists in the cache dictionary.

        This method should almost NEVER be used. The reason is that between the time
        has_key is called, and the key is accessed, the key might vanish.

        You should ALWAYS use a try: ... except KeyError: ... block.

        >>> d = LRUCacheDict(max_size=3, expiration=1)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> import time
        >>> if d.has_key('foo'):
        ...    time.sleep(2) #Oops, the key 'foo' is gone!
        ...    d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        return key in self.__values

    @_lock_decorator
    def __setitem__(self, key, value):
        """
        Store an item into the dictionary.

        Args:
            key (Any): The key of the item to store.
            value (Any): The item to be stored.
        """
        t = int(time.time())
        self.__delete__(key)
        self.__values[key] = value
        self.__access_times[key] = t
        self.__expire_times[key] = t + self.expiration
        self.cleanup()

    @_lock_decorator
    def __getitem__(self, key):
        """
        Return an item stored in the dictionary.

        Args:
            key (Any): The key of the item to retrieve.

        Returns:
            Any: The item from the dictionary.
        """
        t = int(time.time())
        del self.__access_times[key]
        self.__access_times[key] = t
        self.cleanup()
        return self.__values[key]

    @_lock_decorator
    def __delete__(self, key):
        """
        Delete an item from the dictionary.

        Args:
            key (Any): The key of the item to delete.
        """
        if key in self.__values:
            del self.__values[key]
            del self.__expire_times[key]
            del self.__access_times[key]

    @_lock_decorator
    def cleanup(self):
        """
        Clean up the cache dictionary, deleting items as required.

        Returns:
            int: The next expire time for an object in the cache. May be None.
        """
        marked_for_deletion = set()

        if self.expiration is None:
            return None
        t = int(time.time())

        # Delete expired
        next_expire = None
        for k, v in iter(self.__expire_times.items()):
            if v < t:
                marked_for_deletion.add(k)
            else:
                next_expire = v
                break

        for k in marked_for_deletion:
            self.__delete__(k)

        marked_for_deletion = set()

        # If we have more than self.max_size items, delete the oldest
        if len(self.__values) > self.max_size:
            number_to_delete = len(self.__values) - self.max_size
            marked_for_deletion = [k for k in islice(self.__access_times, number_to_delete)]
            for k in marked_for_deletion:
                self.__delete__(k)

        if not (next_expire is None):
            return next_expire - t
        else:
            return None


class LRUCachedFunction(object):
    """
    A memoized function, backed by an LRU cache.

    >>> def f(x):
    ...    print "Calling f(" + str(x) + ")"
    ...    return x
    >>> f = LRUCachedFunction(f, LRUCacheDict(max_size=3, expiration=3) )
    >>> f(3)
    Calling f(3)
    3
    >>> f(3)
    3
    >>> import time
    >>> time.sleep(4) #Cache should now be empty, since expiration time is 3.
    >>> f(3)
    Calling f(3)
    3
    >>> f(4)
    Calling f(4)
    4
    >>> f(5)
    Calling f(5)
    5
    >>> f(3) #Still in cache, so no print statement. At this point, 4 is the least recently used.
    3
    >>> f(6)
    Calling f(6)
    6
    >>> f(4) #No longer in cache - 4 is the least recently used, and there are at least 3 others
    items in cache [3,4,5,6].
    Calling f(4)
    4

    """

    def __init__(self, function, cache=None):
        """
        Initialize the LRUCachedFunction object.

        Args:
            function (func): The function to be used to create new items in the cache.
            cache (LRUCacheDict): The internal cache structure.
        """
        if cache:
            self.cache = cache
        else:
            self.cache = LRUCacheDict()
        self.function = function
        self.__name__ = self.function.__name__

    def __call__(self, *args, **kwargs):
        """
        Retrieve an item from the cache, creating it if necessary.

        Args:
            *args (list): Arguments for the function to initialize the cache item.
            **kwargs (dict): Arguments for the function to initialize the cache item.

        Returns:
            Any: The object in the cache, which may have been created.
        """
        key = repr((args, kwargs)) + "#" + self.__name__
        # In principle a python repr(...) should not return any # characters.
        try:
            return self.cache[key]
        except KeyError:
            value = self.function(*args, **kwargs)
            self.cache[key] = value
            return value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
