import pykka
import re
import json

from gpt_connection import GPT_Connection
from tools import ToolRunner
from frontend_utils import initial_request

from bots.Dispatcher import Dispatcher
from bots.Workflow import Workflow

from prompts import DISPATCHER_PROMPT_TEMPLATE, INITIAL_PROMPT_TEMPLATE, ITERATING_ACTION_PROMPT_TEMPLATE, FORCE_END_ITERATION_PROMPT, \
    PLANT_HEALTH_BOT_DESCRIPTION, PRODUCTION_OUTPUT_BOT_DESCRIPTION, DISTRIBUTION_BOT_DESCRIPTION, \
    ONT_PRODUCTION_PLANT, ONT_MACHINES, ONT_WORK_ORDERS, ONT_PRODUCTION_ALLOCATION_PLAN, ONT_DISTRIBUTION_WAREHOUSE, ONT_TRANSIT_ORDER, \
    GET_OBJECTS, MODIFY_OBJECT, CREATE_OBJECT


from string import Template



"""
Main Execution Code
"""

gpt_connection = GPT_Connection()
tool_runner = ToolRunner()

plant_health_ref = Workflow.start(
    name="Plant Health Bot",
    id=2,
    dispatcher_id=1,
    bot_description=PLANT_HEALTH_BOT_DESCRIPTION,
    initial_prompt_template=INITIAL_PROMPT_TEMPLATE,
    iteration_prompt_template=ITERATING_ACTION_PROMPT_TEMPLATE,
    force_end_prompt_template=FORCE_END_ITERATION_PROMPT,
    information=[ONT_PRODUCTION_PLANT, ONT_MACHINES, ONT_WORK_ORDERS],
    readtools=[GET_OBJECTS],
    writetools=[MODIFY_OBJECT, CREATE_OBJECT],
    gpt_connection=gpt_connection,
    tool_runner=tool_runner
)
production_output_ref = Workflow.start(
    name="Production Output Bot",
    id=3,
    dispatcher_id=1,
    bot_description=PRODUCTION_OUTPUT_BOT_DESCRIPTION,
    initial_prompt_template=INITIAL_PROMPT_TEMPLATE,
    iteration_prompt_template=ITERATING_ACTION_PROMPT_TEMPLATE,
    force_end_prompt_template=FORCE_END_ITERATION_PROMPT,
    information=[ONT_PRODUCTION_PLANT, ONT_MACHINES, ONT_PRODUCTION_ALLOCATION_PLAN],
    readtools=[GET_OBJECTS],
    writetools=[MODIFY_OBJECT, CREATE_OBJECT],
    gpt_connection=gpt_connection,
    tool_runner=tool_runner
)
distribution_ref = Workflow.start(
    name="Distribution Bot",
    id=4,
    dispatcher_id=1,
    bot_description=DISTRIBUTION_BOT_DESCRIPTION,
    initial_prompt_template=INITIAL_PROMPT_TEMPLATE,
    iteration_prompt_template=ITERATING_ACTION_PROMPT_TEMPLATE,
    force_end_prompt_template=FORCE_END_ITERATION_PROMPT,
    information=[ONT_PRODUCTION_PLANT, ONT_DISTRIBUTION_WAREHOUSE, ONT_PRODUCTION_ALLOCATION_PLAN, ONT_TRANSIT_ORDER],
    readtools=[GET_OBJECTS],
    writetools=[MODIFY_OBJECT, CREATE_OBJECT],
    gpt_connection=gpt_connection,
    tool_runner=tool_runner
)
workflows = {
    "Plant Health Bot": plant_health_ref,
    "Production Output Bot": production_output_ref,
    "Distribution Bot": distribution_ref
}
workflow_ids = {
    "Plant Health Bot": 2,
    "Production Output Bot": 3,
    "Distribution Bot": 4
}
dispatcher_ref = Dispatcher.start(
    id=1,
    prompt_template=DISPATCHER_PROMPT_TEMPLATE,
    workflows=workflows,
    workflow_ids=workflow_ids,
    gpt_connection=gpt_connection)



initial_ask = "We just got a message that the ocelot making machine has broken at Stuffed Animal Plant 8"
# initial_ask = "Our trucks carrying transit order T0030 got into an accident."
# initial_ask = "Alice has left the company"
initial_request(initial_ask)
dispatcher_ref.ask(initial_ask)

dispatcher_ref.stop()
