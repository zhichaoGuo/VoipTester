from SipTool.MessageParser import parser_buf
from test.DemoBuffer import REV


class TestInvite:
    _invite = [REV.audio.Invite,
               REV.video.Invite,
               REV.audio.Hold,
               REV.video.Hold,
               REV.audio.Resume,
               REV.video.Resume]

    def test_hold(self):
        hope = [False, False, True, True, False, False]
        for i in range(len(self._invite)):
            sip_message = parser_buf(self._invite[i])
            assert sip_message.is_hold() is hope[i]

    def test_resume(self):
        hope = [False, False, False, False, True, True]
        for i in range(len(self._invite)):
            sip_message = parser_buf(self._invite[i])
            assert sip_message.is_resume() is hope[i]


if __name__ == '__main__':
    test = TestInvite()
    test.test_hold()
    test.test_resume()
