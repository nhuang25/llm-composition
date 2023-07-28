from string import Template

"""
Bot Prompts
"""
DISPATCHER_PROMPT_TEMPLATE = Template(
    """
    You are a dispatcher machine that has access to several other language model assistants.
    You work for a company called Stuffed Animal LLC that produces stuffed animals in production plants, and then ships them to distribution warehouses.
    These are descriptions of the only assistants you have, and what they can do:

    Plant Health Bot: This bot keeps track of each production plant you have, and keeps track of the machines within each plant that manufactures stuffed animals. This bot also tracks when these machines break, and can issue work orders to repair them.
    Production Output Bot: This bot keeps track of the quantities of each type of stuffed animal that each production plant is creating. It does this by manipulating Production Allocation Plans, as well as by setting which stuffed animals specific machines create.
    Distribution Bot: This bot manages the distribution of stuffed animals from production plants to distribution warehouses. It does this by analyzing production allocation plans and managing transit orders to ship specific amounts of specific types of animals from production plants to distribution warehouses.

    
    This is your conversation so far with your assistants:
    $conversation

    And this is the latest message you've received:
    $message

    You can now contact zero, one, or many of your assistants listed above and ask them to do things for you. Return a list of assistants that you want to contact in the following format:
    [
        {"assistant_name": <Assistant Name>, "message": <Message to that particular assistant>},
        {"assistant_name": <Assistant Name>, "message": <Message to that particular assistant>}
    ]

    If you don't think any assistants are worth contacting, return an empty list, []. Contacting assitants is expensive, so only contact them if you absolutely need to.
    """
)

# Human Resource Bot: This bot keeps track of the employed engineers at Stuffed Animal LLC, and how they are assigned to work in different plants. This bot can shift engineers between plants, as well as hire and fire engineers.

INITIAL_PROMPT_TEMPLATE = Template(
    """
    $botdescription

    You have access to the following information from state.
    $information
    
    You have access to the following tools to retrieve information from state:
    $readtools

    You have access to the following tools to write information to state:
    $writetools

    You have received the following request from a dispatcher AI who has been conversing with you and other assistants. This is the conversation so far:
    $conversation

    And this is the latest request to you.
    $message

    Using the information at your disposal, try to fulfill the request you received. If you'd like to perform an action, output the action that you will perform to fulfill the request in the above specified format.
    Return only one action that you'd like to take with the json action request format from the tools you were given above:

    Alternatively, if you cannot complete this request, output a message to dispatcher explaining why you cannot complete this request in the following format:
    {"message_to_dispatcher": "<Message to Dispatcher>"}
    """
)

ITERATING_ACTION_PROMPT_TEMPLATE = Template(
    """
    $botdescription
    
    You have access to the following information from state.
    $information
    
    You have access to the following tools to retrieve information from state:
    $readtools

    You have access to the following tools to write information to state:
    $writetools

    You have received the following request from a dispatcher AI who has been conversing with you and other assistants. This is the conversation so far:
    $conversation

    And this is the latest request to you.
    $message

    This is a log of your prior actions and responses.
    $actionresponselog

    You have just performed this action: 
    $action

    And you have just received this response
    $response

    If that is all the action you would like to take, or if it is clear after the actions you've taken that you don't have enough information to fulfill the request, write a message to dispatcher describing what you did and output in this format: {"message_to_dispatcher": "<Message to Dispatcher>"}.
    Otherwise, if you'd like to take another action, output the proper json request for the one action you'd like to take most. Return only one action that you'd like to take, you can only use the tools listed above.
    Avoid performing actions that you see you have already performed.
    """
)

FORCE_END_ITERATION_PROMPT = Template(
    """
    $botdescription

    This is a log of your prior actions and responses.
    $actionresponselog
    
    You have received the following request from a dispatcher AI who has been conversing with you and other assistants. This is the conversation so far:
    $conversation

    And this is the latest request to you.
    $message

    Write a message to dispatcher describing what you did and output in this format: {"message_to_dispatcher": "<Message to Dispatcher>"}.
    """
)


PLANT_HEALTH_BOT_DESCRIPTION = """
    You are a large language model in charge of understanding and maintaining the production plants at Stuffed Animal LLC.
    Part of your job is to ingest sensor data from machines at your production plants, transform the data into a usable format, and then create work orders to fix broken machines when sensor data is awry.
"""

PRODUCTION_OUTPUT_BOT_DESCRIPTION = """
    You are a large language model in charge of understanding and creating a plan for the output of each large language model at Stuffed Animal LLC.
    Part of your job is to understand the current operating capacities of machines at each plant, and maintain realistic production plans for each plant.
"""

DISTRIBUTION_BOT_DESCRIPTION = """
    You are a large language model in charge of distributing stuffed animals from Production Plants to Distribution Warehouses.
    Your job is to understand the current outputs of the plants, the expectations of distribution warehouses, and to manage transit orders so that warehouses get the stuffed animals they need from plants.
"""



"""
Ontology Descriptions
"""

ONT_PRODUCTION_PLANT = """
    object_type: Production Plant
    description: Information about each of the production plants that Stuffed Animal LLC owns.
    features:
    - plant_id: The unique identifier of the plant
    - plant_name: The name of the plant
    - coordinate: An integer that describes the location of a plant relative to other plants. The distance between two plants is the difference between their coordinate integer values.
"""

ONT_MACHINES = """
    object_type: Machine
    description: Information about each of the machines used to create stuffed animals, inside each of the produciton plants that Stuffed Animal LLC owns.
    features:
    - machine_id: The unique identifier of the machine
    - plant_id: The unique identifier of the plant that the machine is located in
    - machine_animal: The type of stuffed animal that a machine is currently manufacturing
    - status: Describes whether the machine is "HEALTHY" or "BROKEN"
    - efficiency: An integer number of how many animals this machine can create in a day
"""

ONT_WORK_ORDERS = """
    object_type: Work Order
    description: Information about work orders that have been scheduled on machines that are broken
    - work_order_id: The unique identifier of the work order
    - machine_id: The unique identifier of the machine that the work order is supposed to fix
    - date_issued: A date of when the work order is supposed to take place
    - length_of_fix: An integer of how many days repairs are supposed to take on this machine
"""

ONT_PRODUCTION_ALLOCATION_PLAN = """
    object_type: Production Allocation Plan
    description: A plan for each production plant describing how much of each stuffed animal they are aiming to produce daily
    - plant_id: The unique identifier of the production plant
    - ocelot_to_produce: The number of ocelet stuffed animals the plant aims to produce each day
    - penguin_to_produce: The number of penguin stuffed animals the plant aims to produce each day
    - hippo_to_produce: The number of hippo stuffed animals the plant aims to produce each day
    - camel_to_produce: The number of camel stuffed animals the plant aims to produce each day
    - elephant_to_produce: The number of elephant stuffed animals the plant aims to produce each day
    - kangaroo_to_produce: The number of kangaroo stuffed animals the plant aims to produce each day
"""

ONT_DISTRIBUTION_WAREHOUSE = """
    object_type: Distribution Warehouse
    description: An end location for stuffed animals. Stuffed animals are delivered to Distribution Warehouses through Transit Orders, from Production Plants.
    - warehouse_id: The unique identifier of the distribution warehouse
    - warehouse_name: The name of the distribution warehouse
    - coordinate: An integer that describes the location of a warehouse relative to other plants and warehouses. The distance between two objects is the difference between their coordinate integer values.
    - ocelot_in_stock: The number of ocelet stuffed animals the warehouse can expect to have in stock
    - penguin_in_stock: The number of penguin stuffed animals the warehouse can expect to have in stock
    - hippo_in_stock: The number of hippo stuffed animals the warehouse can expect to have in stock
    - camel_in_stock: The number of camel stuffed animals the warehouse can expect to have in stock
    - elephant_in_stock: The number of elephant stuffed animals the warehouse can expect to have in stock
    - kangaroo_in_stock: The number of kangaroo stuffed animals the warehouse can expect to have in stock
"""

ONT_TRANSIT_ORDER = """
    object_type: Transit Order
    description: Specifies the delivery of a shipment of a certain type of stuffed animal from a Production Plant to a Distribution Warehouse.
    - transit_order_id: The unique identifier of the transit order
    - plant_id: The unique identifier of the source production plant
    - warehouse_id: The unique identifier of the destination distribution warehouse
    - animal_type: The type of stuffed animal that is being shipped
    - quantity: How many of the particular animal is being shipped
    - frequency: How often this is shipped in days. (1 means shipped daily, 2 means every other day)
"""


"""
Tools
"""
GET_OBJECTS = """
You can retrieve information about all of the objects of a type by returning the following output:
{"action": "Get All Objects", "object_type": <Object Type>}
"""

MODIFY_OBJECT = """
You can edit the information of an object by returning the following output
{"action": "Edit Object", "object_type": <Object Type>, "object_id": <Object Id>, "feature": <Property to edit>, "value": <New value of feature>}
"""

CREATE_OBJECT = """
You can create a new object by returning a request in the format of the output below. Note that you must provide a value for each feature in the object type that you are aiming to create
{"action": "Create Object", "object_type": <Object Type>, "object_id": <Object Id>, "features": {<Property to create>: <property value>}}
"""






"""
Additional Tool Descriptions: Functions, Actions, Code Repos
"""