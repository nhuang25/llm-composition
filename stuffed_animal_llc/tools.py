

class ToolRunner:
    def __init__(self):
        self.object_to_file_map = {
            "Production Plant": "./ontology/production_plants.txt",
            "Machine": "./ontology/machines.txt",
            "Work Order": "./ontology/work_orders.txt",
            "Production Allocation Plan": "./ontology/production_output.txt",
            "Distribution Warehouse": "./ontology/warehouses.txt",
            "Transit Order": "./ontology/transit_orders.txt"
        }

    def act(self, action_json):
        action = action_json['action']
        if action == 'Edit Object':
            return "Modified Object Successfully"
        elif action == "Get All Objects":
            try:
                relevant_object = action_json['object_type']
                file_path = self.object_to_file_map[relevant_object]
                with open(file_path, "r") as file:
                    content = file.read()
                    return content
            except Exception as e:
                print("Error Retrieving all objects: ", e)
                return ""
        elif action == 'Create Object':
            return "Created Object Successfully"
        else:
            return ""