from RPA.Excel.Files import Files
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Tables import Tables

WORKITEMS = WorkItems()


def create_new_status_dict():
    return {
        "step1": False,
        "step2": False,
        "step3": False,
    }


def update_workitem(status_dict):
    WORKITEMS.set_work_item_variable("Status", status_dict)
    WORKITEMS.save_work_item()


def handle_item():
    status_dict = create_new_status_dict()
    variables = WORKITEMS.get_work_item_variables()
    all_pass = (
        False if "Status" not in variables.keys() else all(variables["Status"].values())
    )
    if all_pass:

        print("Work item has been successfully executed")
    else:
        print("Work item needs to be processed")
        process_item(variables, status_dict)

    print(variables)
    update_workitem(status_dict)


def process_item(variables, status_dict):
    print("Processing item")
    step1(variables, status_dict)
    step2(variables, status_dict)
    step3(variables, status_dict)


def step1(variables, status_dict):
    status_dict["step1"] = True


def step2(variables, status_dict):
    status_dict["step2"] = True


def step3(variables, status_dict):
    status_dict["step3"] = True


def main():
    try:
        WORKITEMS.for_each_input_work_item(handle_item)
    except Exception as err:
        WORKITEMS.release_input_work_item(
            state="failed", exception_type="application", message="I failed"
        )
    pass


if __name__ == "__main__":
    main()
