import pykka
import re
import json
from frontend_utils import add_edge_request, end_request_thread

class Dispatcher(pykka.ThreadingActor):
    def __init__(self, id, prompt_template, workflows, workflow_ids, gpt_connection):
        super().__init__()
        self.name = "Dispatcher"
        self.prompt_format = prompt_template
        self.gpt_connection = gpt_connection
        self.workflows = workflows
        self.workflow_ids = workflow_ids
        self.conversation = ""
        self.communication_queue = []
        self.id = id
        
    def on_receive(self, message):
        print(self.name + " has received the following message: \n" + message)
        prompt = self.prompt_format.substitute({'message': message, 'conversation': self.conversation})
        response = self.gpt_connection.make_request(prompt)
        pattern = r'\{.*?\}'
        orders_str = re.findall(pattern, response)
        if len(orders_str) == 0:
            end_request_thread()
            print("NO ORDERS FROM DISPATCHER, FINISHING THREAD")
            print("-------------------------------------\n")
            return
        orders_str = [orders_str[0]]        # Testing limit to 1
        self.debug_print_orders(orders_str)
        for order_str in orders_str:
            order = json.loads(order_str)
            self.dispatch_command(order)

    def dispatch_command(self, order):
        try:
            print(self.name + " is sending the following message to " + order['assistant_name'] + "\n" + order['message'] + "\n")
            self.conversation = self.conversation + "\n" + "Dispatcher to " + order["assistant_name"] + ": " + order['message']
            # Send message to UI
            add_edge_request(self.id, self.workflow_ids[order['assistant_name']], order['message'])
            resp = self.workflows[order['assistant_name']].ask(order['message'])
            if resp != "Invalid Response":
                self.conversation = self.conversation + "\n" + order["assistant_name"] + " to Dispatcher: " + resp
                print("*** ", "Full Conversation Log:" + self.conversation, "\n***\n")
                self.on_receive(resp)
        except:
            pass

    def debug_print_orders(self, orders_str):
        counter = 1
        print("Orders from Dispatcher: ")
        for order_str in orders_str:
            print(str(counter) + ". " + order_str)
            counter += 1
