import sleekxmpp
import time
from . sleektest import *


class TestEvents(SleekTest):

    def setUp(self):
        self.streamStart()

    def tearDown(self):
        self.streamClose()

    def testEventHappening(self):
        """Test handler working"""
        happened = []

        def handletestevent(event):
            happened.append(True)

        self.xmpp.add_event_handler("test_event", handletestevent)
        self.xmpp.event("test_event")
        self.xmpp.event("test_event")

        # Give the event queue time to process.
        time.sleep(0.1)

        msg = "Event was not triggered the correct number of times: %s"
        self.failUnless(happened == [True, True], msg)

    def testDelEvent(self):
        """Test handler working, then deleted and not triggered"""
        happened = []

        def handletestevent(event):
            happened.append(True)

        self.xmpp.add_event_handler("test_event", handletestevent)
        self.xmpp.event("test_event", {})

        self.xmpp.del_event_handler("test_event", handletestevent)

        # Should not trigger because it was deleted
        self.xmpp.event("test_event", {})

        # Give the event queue time to process.
        time.sleep(0.1)

        msg = "Event was not triggered the correct number of times: %s"
        self.failUnless(happened == [True], msg % happened)

    def testDisposableEvent(self):
        """Test disposable handler working, then not being triggered again."""
        happened = []

        def handletestevent(event):
            happened.append(True)

        self.xmpp.add_event_handler("test_event", handletestevent,
                                    disposable=True)
        self.xmpp.event("test_event", {})

        # Should not trigger because it was deleted
        self.xmpp.event("test_event", {})

        # Give the event queue time to process.
        time.sleep(0.1)

        msg = "Event was not triggered the correct number of times: %s"
        self.failUnless(happened == [True], msg % happened)


suite = unittest.TestLoader().loadTestsFromTestCase(TestEvents)
