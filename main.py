import struct
import datetime
import os

# Define the InventoryRecord class to hold record data
class InventoryRecord:
    def __init__(self, description, quantity, wholesale_cost, sale_price, date_added):
        self.description = description
        self.quantity = quantity
        self.wholesale_cost = wholesale_cost
        self.sale_price = sale_price
        self.date_added = date_added

    # Define the size of the record in bytes
    @staticmethod
    def size():
        return struct.calcsize("50s i d d 10s")  # Assuming 50 bytes for description, 4 bytes for int, 8 bytes for double, and 10 bytes for date

    # Pack the record data into bytes
    def pack(self):
        return struct.pack("50s i d d 10s",
                           self.description.encode("utf-8"),
                           self.quantity,
                           self.wholesale_cost,
                           self.sale_price,
                           self.date_added.encode("utf-8"))

    # Unpack bytes into record data
    @staticmethod
    def unpack(data):
        description, quantity, wholesale_cost, sale_price, date_added = struct.unpack("50s i d d 10s", data)
        return InventoryRecord(description.decode("utf-8").strip(), quantity, wholesale_cost, sale_price, date_added.decode("utf-8"))

# Function to add a new record
def add_new_record():
    description = input("Enter item description: ")
    quantity = int(input("Enter quantity on hand: "))
    wholesale_cost = float(input("Enter wholesale cost: "))
    sale_price = float(input("Enter sale price: "))
    date_added = datetime.datetime.now().strftime("%Y-%m-%d")  # Get current date
    record = InventoryRecord(description, quantity, wholesale_cost, sale_price, date_added)
    with open("inventory.dat", "ab") as file:
        file.write(record.pack())

# Function to display a record
def display_record():
    record_number = int(input("Enter record number to display: "))
    with open("inventory.dat", "rb") as file:
        # Calculate seek position
        seek_position = (record_number - 1) * InventoryRecord.size()
        file.seek(seek_position)
        # Read and display record
        record_data = file.read(InventoryRecord.size())
        record = InventoryRecord.unpack(record_data)
        print("Description:", record.description)
        print("Quantity on hand:", record.quantity)
        print("Wholesale cost:", record.wholesale_cost)
        print("Sale price:", record.sale_price)
        print("Date added:", record.date_added)

# Function to change a record
def change_record():
    record_number = int(input("Enter record number to change: "))
    with open("inventory.dat", "rb+") as file:
        # Calculate seek position
        seek_position = (record_number - 1) * InventoryRecord.size()
        file.seek(seek_position)
        # Read existing record
        record_data = file.read(InventoryRecord.size())
        record = InventoryRecord.unpack(record_data)
        # Prompt user for new data
        record.description = input("Enter new item description: ")
        record.quantity = int(input("Enter new quantity on hand: "))
        record.wholesale_cost = float(input("Enter new wholesale cost: "))
        record.sale_price = float(input("Enter new sale price: "))
        # Write updated record
        file.seek(seek_position)
        file.write(record.pack())

# Main function
def main():
    # Check if file exists
    if not os.path.exists("inventory.dat"):
        open("inventory.dat", "wb").close()  # Create the file if it doesn't exist

    while True:
        # Display menu
        print("\nMenu:")
        print("1. Add new record")
        print("2. Display record")
        print("3. Change record")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_new_record()
        elif choice == "2":
            display_record()
        elif choice == "3":
            change_record()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()