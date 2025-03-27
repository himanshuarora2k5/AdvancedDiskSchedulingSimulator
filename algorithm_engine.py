def fcfs(disk_requests, initial_head):
    """
    Simulate First-Come-First-Serve disk scheduling algorithm.
    Args:
    disk_requests (list): List of disk requests
    initial_head (int): Initial head position
    Returns:
    total_head_movement (dict): Total head movement and sequence of head movements
    """

    current_head = initial_head
    total_head_movement = 0
    schedule = []
    for request in disk_requests:
        movement = abs(request - current_head)
        total_head_movement += movement
        schedule.append(request)
        current_head = request
    if len(disk_requests) > 0:
        average_seek = total_head_movement / len(disk_requests)
    else:
        average_seek = 0
    return {
        "schedule": schedule,
        "total_head_movement": total_head_movement,
        "average_seek": average_seek
    }
#standalone test
if __name__ == "__main__":
    #example input
    disk_requests = [45, 20, 65]
    initial_head = 50
    result = fcfs(disk_requests, initial_head)
    print("Service Order: ", result["schedule"])
    print("Total Head Movement: ", result["total_head_movement"])
    print("Average Seek Time: ", result["average_seek"])