from RPA.Excel.Files import Files
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Tables import Tables

WORKITEMS = WorkItems()
EXCEL = Files()


def main():
    WORKITEMS.get_input_work_item()
    filepath = WORKITEMS.get_work_item_file("orders.xlsx", "./output/orders.xlsx")
    EXCEL.open_workbook(filepath)
    table_data = EXCEL.read_worksheet_as_table(header=True)
    for row in table_data:
        item_data = {"Name": row["Name"], "Zip": row["Zip"], "Item": row["Item"]}
        WORKITEMS.create_output_work_item(variables=item_data, save=True)


if __name__ == "__main__":
    main()
