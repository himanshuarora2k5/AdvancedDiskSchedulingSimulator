def get_input():
    """
    Get disk requests and initial head position from user input.
    Returns:
    disk_requests (list): List of disk requests
    initial_head (int): Initial head position
    """
    while True:
        try:
            #get disk requests
            raw_requests = input("Enter disk requests (comma-seperated): ")
            disk_requests = [int(x) for x in raw_requests.split(',')]
            
            #get initial head position
            initial_head = int(input("Enter initial head position: "))
            
            #check for invalid input
            if any(x < 0 for x in disk_requests) or initial_head < 0:
                print("Invalid input. Please enter positive integers.")
                continue
            
            #return valid input
            return disk_requests, initial_head
        
        #handle invalid input
        except ValueError:
            print("Invalid input. Please enter valid integers seperated by commas.")

#standalone test
if __name__ == "__main__":
    disk_requests, initial_head = get_input()
    print(disk_requests, initial_head)
    