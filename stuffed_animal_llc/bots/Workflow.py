import pykka
import re
import regex
import json

from frontend_utils import add_edge_request, action_request


class Workflow(pykka.ThreadingActor):
    """
    Sets up all of our prompt template variables
    """
    def __init__(
            self,
            name,
            id,
            dispatcher_id,
            bot_description,
            initial_prompt_template,
            iteration_prompt_template,
            force_end_prompt_template,
            information,
            readtools,
            writetools,
            gpt_connection,
            tool_runner
        ):
        super().__init__()
        self.name = name
        self.id = id
        self.dispatcher_id = dispatcher_id
        self.bot_description = bot_description
        self.initial_prompt_template = initial_prompt_template
        self.iteration_template = iteration_prompt_template
        self.force_end_prompt_template = force_end_prompt_template
        self.gpt_connection = gpt_connection
        self.tool_runner = tool_runner
        self.conversation = ""
        self.total_attempts = 5

        self.readtools = ""
        read_tool_counter = 1
        for tool in readtools:
            self.readtools += (str(read_tool_counter) + ': ' + tool + '\n')
            read_tool_counter += 1

        self.writetools = ""
        write_tool_counter = 1
        for tool in writetools:
            self.readtools += (str(write_tool_counter) + ': ' + tool + '\n')
            write_tool_counter += 1

        self.information = ""
        information_counter = 1
        for info in information:
            self.information += (str(information_counter) + ': ' + info + '\n')
            information_counter += 1

    
    """
    Triggers when we receive a message from Dispatcher
    We iteratively attempt to address Dispatcher's request with the tools at our disposal
    """
    def on_receive(self, message):
        # Add Dispatcher's communication to our ongoing conversation state
        print(self.name + " has received the following message: \n" + message)
        self.conversation = self.conversation + "\n" + "Dispatcher to " + self.name+ ": " + message

        # Assemble first time prompt
        prompt = self.initial_prompt_template.substitute(
            {
                'botdescription': self.bot_description,
                'information': self.information,
                'readtools': self.readtools,
                'writetools': self.writetools,
                'conversation': self.conversation,
                'message': message
            }
        )

        # Create a log for our actions and responses from our Tools
        action_response_log = ""

        # While an exit condition isn't met, iteratively try to complete the request
        exit = False
        iteration = 0
        return_message = ""
        while(exit == False):
            iteration += 1
            print("* ", self.name, " Iteration #", iteration, " *")
            # Make requests to GPT with prompt - Fault Tolerance allows for multiple tries
            attempt_number = 0
            while attempt_number < self.total_attempts:
                attempt_number += 1
                try:
                    # Make GPT Request with current prompt
                    response = self.gpt_connection.make_request(prompt)
                    # Parse out JSON from response
                    pattern = r'\{((?:[^{}]+|(?R))*)\}'
                    match = regex.search(pattern, response)
                    # Attempt to load JSON
                    response_json = json.loads(match.group(0))
                    # If 'action' is in JSON, then attempt to complete that action
                    if "action" in response_json:
                        # Attempt to complete the suggested action
                        tool_running_response = self.tool_runner.act(response_json)
                        # Update prompt if action successful
                        prompt = self.iteration_template.substitute(
                            {
                                'botdescription': self.bot_description,
                                'information': self.information,
                                'readtools': self.readtools,
                                'writetools': self.writetools,
                                'conversation': self.conversation,
                                'message': message,
                                'actionresponselog': action_response_log,
                                'action': response_json,
                                'response': tool_running_response
                            }
                        )
                        # Add action and response to the action log, print our successful action
                        action_description = self.name + " performed the following action: \n" + str(response_json) + "\n"
                        response_description = "And then received response " + tool_running_response + "\n"
                        print(action_description)
                        action_request(self.id, str(response_json))

                        # If the context length is too long, we cannot append 
                        if len(prompt) > 26000:
                            print("Context getting too long, time to end questioning")
                            # Set prompt equal to our endgame summarization prompt
                            prompt = self.force_end_prompt_template.substitute(
                                {
                                    'botdescription': self.bot_description,
                                    'conversation': self.conversation,
                                    'message': message,
                                    'actionresponselog': action_response_log,
                                }
                            )
                        # If we still have room in our context, append the action and response to the action log
                        else:
                            action_response_log += (action_description + response_description)
                        # Now that this has succeeded, break out of our Fault Tolerance loop
                        print("DEBUG: Iteration #" + str(iteration) + " Attempt " + str(attempt_number) + ": Succeeded - Now performing the next Action Iteration\n")
                        break
                    # Otherwise, if 'message_to_dispatcher' is in the GPT response, set our return message and exit the while loop
                    elif "message_to_dispatcher" in response_json:
                        print(self.name + " is sending the following message to the Dispatcher: \n" + response_json['message_to_dispatcher'] + "\n")
                        return_message = f"Hi, this is {self.name}. {response_json['message_to_dispatcher']}"
                        exit=True
                        # Now that this has succeeded, break out of our Fault Tolerance loop
                        print("DEBUG: Iteration #" + str(iteration) + " Attempt " + str(attempt_number) + ": Succeeded - Now responding to Dispatcher\n")
                        break
                    # Else, we did not enter either if statement despite parsing the json properly
                    else:
                        print("DEBUG: Iteration #" + str(iteration) + " Attempt " + str(attempt_number) + ": Failed - Parsed response but no valid keys\n")
                        print("This was the most recent response: ", str(response))
                        continue
                except Exception as e:
                    print("DEBUG: Iteration #" + str(iteration) + " Attempt " + str(attempt_number) + ": Failed\n")
                    print("There was an error from ", self.name, "\nError: ", e)
                    print("This was the most recent response: ", str(response))
                    continue

            # If we make it N attempts without a successful flow, then we exit
            if attempt_number == self.total_attempts:
                return_message = "Invalid Response"
                print("ERROR: All " + str(self.total_attempts) + " attempts failed for this request \n")
                exit=True
        
        self.conversation = self.conversation + "\n" +  self.name +" to Dispatcher: " + return_message
        # Send message to UI
        add_edge_request(self.id, self.dispatcher_id, return_message)
        return return_message
