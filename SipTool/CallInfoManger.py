from SipTool.MessageParser import SipMessage


class CallInfoManger:
    def __init__(self):
        self.dict = {}
        self.all_call_id = set()

    def get_call(self, cur_message: SipMessage):
        call_id = cur_message.headers.CallID.call_id
        if call_id not in self.all_call_id:
            self.all_call_id.add(call_id)
        else:
            self.dict[call_id].put(cur_message)
        return self.dict[call_id]