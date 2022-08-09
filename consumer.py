from RPA.Robocorp.WorkItems import WorkItems, State, Error
from random import randint

WORKITEMS = WorkItems()


def create_new_status_dict():
    return {
        "action1": False,
        "action2": False,
        "action3": False,
    }


def handle_item():
    variables = WORKITEMS.get_work_item_variables()
    all_pass = False
    # on first consumer run the status information is not (in this example)
    # part of the work item variables - structure is initialized if not present
    if "status" not in variables.keys():
        variables["status"] = create_new_status_dict()
    else:
        # status structure is present - check if all steps are completed
        all_pass = all(variables["status"].values())

    if not all_pass:
        # not all steps are completed - process item
        process_item(variables)

    all_pass = all(variables["status"].values())
    # save status information into the work item
    WORKITEMS.save_work_item()
    if all_pass:
        # all actions are completed - release work item
        WORKITEMS.release_input_work_item(State.DONE)
    else:
        # not all actions are completed - mark work item as failed
        failures = [
            key for key in variables["status"].keys() if not variables["status"][key]
        ]
        error_msg = f"{variables['Name']} - {variables['Item']}: business errors: {','.join(failures)}"
        WORKITEMS.release_input_work_item(
            State.FAILED, Error.BUSINESS, message=error_msg
        )


def process_item(variables):
    print("Processing item")
    _business_block("action1", variables)
    _business_block("action2", variables)
    _business_block("action3", variables)


def _business_block(action_name, variables):
    if variables["status"][action_name]:
        print(f"{action_name} ALREADY completed")
        return
    # simulating success / error with business logic
    variables["status"][action_name] = False if randint(1, 4) == 4 else True
    if variables["status"][action_name]:
        print(f"{action_name} COMPLETED")
    else:
        print(f"{action_name} still NOT completed")


def main():
    try:
        WORKITEMS.get_input_work_item()
        WORKITEMS.for_each_input_work_item(handle_item)
    except Exception as err:
        WORKITEMS.release_input_work_item(
            state=State.FAILED,
            exception_type=Error.APPLICATION,
            message="I failed",
        )
    pass


if __name__ == "__main__":
    main()
