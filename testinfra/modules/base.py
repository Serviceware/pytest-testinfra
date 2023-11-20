# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TYPE_CHECKING, Callable

import testinfra.modules


def register_module(name: str) -> Callable[[type["Module"]], type["Module"]]:
    """registers the module under the given name

    Once it is registered, you can call the module as "host.NAME".

    Example:

    >>> @register_module("my_module")
    ... class MyModule(Module):
    ...     def __init__(self, param):
    ...         self.param = param
    >>> def my_test(host):
    ...     foo = host.my_module("param")
    """

    def wrapper(clz: type["Module"]) -> type["Module"]:
        testinfra.modules.modules[name] = "{}:{}".format(
            clz.__module__,
            clz.__name__,
        )
        return clz

    return wrapper


class Module:
    if TYPE_CHECKING:
        import testinfra.host

        _host: testinfra.host.Host

    @classmethod
    def get_module(cls, _host: "testinfra.host.Host") -> type["Module"]:
        klass = cls.get_module_class(_host)
        return type(
            klass.__name__,
            (klass,),
            {"_host": _host},
        )

    @classmethod
    def get_module_class(cls, host):
        return cls

    @classmethod
    def run(cls, *args, **kwargs):
        return cls._host.run(*args, **kwargs)

    @classmethod
    def run_test(cls, *args, **kwargs):
        return cls._host.run_test(*args, **kwargs)

    @classmethod
    def run_expect(cls, *args, **kwargs):
        return cls._host.run_expect(*args, **kwargs)

    @classmethod
    def check_output(cls, *args, **kwargs):
        return cls._host.check_output(*args, **kwargs)

    @classmethod
    def find_command(cls, *args, **kwargs):
        return cls._host.find_command(*args, **kwargs)


class InstanceModule(Module):
    @classmethod
    def get_module(cls, _host):
        klass = super().get_module(_host)
        return klass()
