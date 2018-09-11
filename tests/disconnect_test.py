import signal
import os

import unittest2

import testlib
import mitogen.master
import mitogen.parent
import mitogen.utils


def ping():
    return True


def kill_self():
    os.kill(os.getpid(), signal.SIGKILL)


class DisconnectionTest(testlib.RouterMixin, testlib.TestCase):
    def test_during_call(self):
        child = self.router.fork()
        self.assertRaises(mitogen.core.ChannelError,
            lambda: child.call(kill_self))

    def test_during_call_grandchild(self):
        child = self.router.fork()
        child2 = self.router.fork(via=child)
        self.assertRaises(mitogen.core.ChannelError,
            lambda: child2.call(kill_self))
        self.assertRaises(mitogen.core.ChannelError,
            lambda: child2.call(ping))

    def test_after_disconnect(self):
        child = self.router.fork()
        self.assertRaises(mitogen.core.ChannelError,
            lambda: child.call(kill_self))
        self.assertRaises(mitogen.core.ChannelError,
            lambda: child.call(ping))


if __name__ == '__main__':
    unittest2.main()
