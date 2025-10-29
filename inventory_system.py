"""
Inventory Management System

This module provides functions to manage inventory stock data including
adding, removing, loading, saving, and reporting on inventory items.
"""
import json
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory with the specified quantity.

    Args:
        item (str): Name of the item to add
        qty (int): Quantity to add (must be non-negative)
        logs (list): Optional list to log operations

    Returns:
        bool: True if successful, False otherwise
    """
    if logs is None:
        logs = []

    # Input validation
    if not isinstance(item, str):
        logging.error("Item name must be a string")
        return False

    if not isinstance(qty, int):
        logging.error("Quantity must be an integer")
        return False

    if not item:
        logging.warning("Empty item name provided")
        return False

    if qty < 0:
        logging.warning("Negative quantity %d provided for %s", qty, item)

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info("%s: Added %d of %s", datetime.now(), qty, item)
    return True


def remove_item(item, qty):
    """
    Remove a specified quantity of an item from the inventory.

    Args:
        item (str): Name of the item to remove
        qty (int): Quantity to remove

    Returns:
        bool: True if successful, False if item not found
    """
    if not isinstance(item, str):
        logging.error("Item name must be a string")
        return False

    if not isinstance(qty, int) or qty < 0:
        logging.error("Quantity must be a non-negative integer")
        return False

    try:
        if item not in stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(
                "Item '%s' removed from inventory (quantity <= 0)",
                item
            )
        return True
    except KeyError as e:
        logging.error("Error removing item: %s", e)
        return False


def get_qty(item):
    """
    Get the current quantity of an item in inventory.

    Args:
        item (str): Name of the item

    Returns:
        int: Quantity of the item, or 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        dict: Loaded stock data
    """
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Data loaded from %s", file)
        return stock_data
    except FileNotFoundError:
        logging.warning(
            "File %s not found, starting with empty inventory",
            file
        )
        stock_data = {}
        return stock_data
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON from %s: %s", file, e)
        return {}


def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logging.info("Data saved to %s", file)
        return True
    except IOError as e:
        logging.error("Error saving data to %s: %s", file, e)
        return False


def print_data():
    """
    Print a report of all items in the inventory.
    """
    print("Items Report")
    print("-" * 30)
    if not stock_data:
        print("No items in inventory")
    else:
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")
    print("-" * 30)


def check_low_items(threshold=5):
    """
    Check for items with quantity below a threshold.

    Args:
        threshold (int): Minimum quantity threshold

    Returns:
        list: List of items below the threshold
    """
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """
    Main function to demonstrate inventory system functionality.
    """
    logging.info("Starting inventory system")

    # Valid operations
    add_item("apple", 10)
    add_item("banana", 5)

    # This will log a warning for negative quantity but still add
    add_item("orange", -2)

    # This will fail validation and log errors
    add_item(123, "ten")  # invalid types - will be caught by validation

    remove_item("apple", 3)
    remove_item("orange", 1)  # This may work despite negative initial stock

    # Try to remove non-existent item
    remove_item("grape", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()
    load_data()
    print_data()

    # Removed dangerous eval() - replaced with safe alternative
    print('Safe print without eval')

    logging.info("Inventory system completed")


if __name__ == "__main__":
    main()
