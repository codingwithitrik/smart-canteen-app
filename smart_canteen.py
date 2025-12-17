import time
import threading
from collections import deque

class MenuItem:
    def __init__(self, name, price, prep_time):
        self.name = name
        self.price = price
        self.prep_time = prep_time  # in seconds for simulation

class Order:
    def __init__(self, student_id, items, is_advance=True):
        self.student_id = student_id
        self.items = items  # list of MenuItem
        self.is_advance = is_advance
        self.total_price = sum(item.price for item in items)
        self.estimated_prep_time = sum(item.prep_time for item in items)
        self.status = "Queued"

class SmartCanteen:
    def __init__(self):
        self.menu = [
            MenuItem("Burger", 5.0, 5),
            MenuItem("Pizza Slice", 4.0, 4),
            MenuItem("Coffee", 2.0, 2),
            MenuItem("Sandwich", 3.5, 3),
        ]
        self.queue = deque()  # Queue for orders
        self.processing = False

    def display_menu(self):
        print("\n--- Canteen Menu ---")
        for i, item in enumerate(self.menu, 1):
            print(f"{i}. {item.name} - ${item.price} (Prep: {item.prep_time}s)")

    def place_order(self, student_id, item_indices, is_advance=True):
        items = [self.menu[i-1] for i in item_indices if 0 < i <= len(self.menu)]
        if not items:
            print("Invalid items selected.")
            return
        order = Order(student_id, items, is_advance)
        self.queue.append(order)
        print(f"Order placed for {student_id}. Total: ${order.total_price}. Estimated prep: {order.estimated_prep_time}s.")
        if not self.processing:
            self.start_processing()

    def start_processing(self):
        if self.queue:
            self.processing = True
            threading.Thread(target=self.process_queue).start()

    def process_queue(self):
        while self.queue:
            order = self.queue.popleft()
            print(f"\nProcessing order for {order.student_id}...")
            time.sleep(order.estimated_prep_time)
            order.status = "Ready"
            print(f"Order for {order.student_id} is ready! Total: ${order.total_price}")
        self.processing = False

    def view_queue(self):
        if not self.queue:
            print("Queue is empty.")
            return
        print("\n--- Current Queue ---")
        total_wait = 0
        for i, order in enumerate(self.queue, 1):
            wait_time = total_wait + order.estimated_prep_time
            print(f"{i}. {order.student_id} - {len(order.items)} items - Est. wait: {wait_time}s - Status: {order.status}")
            total_wait += order.estimated_prep_time

def main():
    canteen = SmartCanteen()
    while True:
        print("\n--- Smart Canteen System ---")
        print("1. View Menu")
        print("2. Place Advance Order")
        print("3. Place On-the-Spot Order")
        print("4. View Queue")
        print("5. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            canteen.display_menu()
        elif choice == "2":
            student_id = input("Enter student ID: ")
            canteen.display_menu()
            indices = list(map(int, input("Enter item numbers (comma-separated): ").split(",")))
            canteen.place_order(student_id, indices, is_advance=True)
        elif choice == "3":
            student_id = input("Enter student ID: ")
            canteen.display_menu()
            indices = list(map(int, input("Enter item numbers (comma-separated): ").split(",")))
            canteen.place_order(student_id, indices, is_advance=False)
        elif choice == "4":
            canteen.view_queue()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
