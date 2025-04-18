def get_input():
    """
    This function is for getting user input for disk requests and the starting head position.
    It gives back:
        - disk_reqs (list): A list of disk requests
        - start_head (int): The starting position of the head
    """
    while True:
        try:
            # Prompt user to enter disk requests
            reqs_raw = input("Enter the disk requests (comma-separated): ")
            reqs_list = [int(x.strip()) for x in reqs_raw.split(',')]
            
            # Prompt user to enter head position
            head_start = int(input("Enter the starting head position: "))
            
            # Check if all inputs are positive
            if any(r < 0 for r in reqs_list) or head_start < 0:
                print("Error: Only positive numbers are allowed. Please try again.")
                continue
            
            # Return 
            return reqs_list, head_start
        
        except ValueError:
            #invalid input
            print("Invalid input. Please enter numbers only, separated by commas.")

# Test
# if __name__ == "__main__":
#     requests, head = get_input()
#     print(requests, head)
