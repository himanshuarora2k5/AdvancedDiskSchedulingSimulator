def fcfs(reqs, startHead):
    """
    Simulate FCFS disk scheduling algo.
    Args:
        reqs (list): List of disk reqs.
        startHead (int): Initial head pos.
    Returns:
        dict: Contains the service order, total head movement, avg seek time, and thpt.
    """
    totalHead = startHead
    headMovement = 0
    order = []
    for r in reqs:
        move = abs(r - totalHead)
        headMovement += move
        order.append(r)
        totalHead = r
    avgSeek = headMovement / len(reqs) if reqs else 0
    
    # Throughput calc
    time = headMovement  
    thpt = len(reqs) / time if time else 0
    
    return {
        "order": order,
        "head Movement": headMovement,
        "average Seek": avgSeek,
        "throughput": thpt
    }

def sstf(reqs, startHead):
    """
    simulate SSTF disk scheduling algo.
    args:
        reqs (list): List of disk reqs.
        startHead (int): Initial head pos.
    Returns:
        dict: Contains the service order, total head movement, avg seek time, and throughput.
    """
    totalHead = startHead
    headMovement = 0
    order = []
    leftReqs = reqs.copy()

    while leftReqs:
        # Find closest req
        closeReq = min(leftReqs, key=lambda x: abs(x - totalHead))
        move = abs(closeReq - totalHead)
        headMovement += move
        order.append(closeReq)
        totalHead = closeReq
        leftReqs.remove(closeReq)

    avgSeek = headMovement / len(reqs) if reqs else 0
    time = headMovement  
    thpt = len(reqs) / time if time else 0
    
    return {
        "order": order,
        "head Movement": headMovement,
        "average Seek": avgSeek,
        "throughput": thpt
    }

def scan(reqs, startHead, diskSize=200):
    """
    simulate SCAN disk scheduling algo.
    Args:
        reqs (list): List of disk reqs.
        startHead (int): Initial head pos.
        diskSize (int): Max disk track num.
    Returns:
        dict: Contains the service order, total head movement, avg seek time, and throughput.
    """
    # split reqs into left right
    left = [r for r in reqs if r < startHead]
    right = [r for r in reqs if r >= startHead]

    left.sort(reverse=True)  # Sort left requests in descending order
    right.sort()             # Sort right requests in ascending order

    order = []
    headMovement = 0
    totalHead = startHead

    # Move right first
    for r in right:
        headMovement += abs(r - totalHead)
        order.append(r)
        totalHead = r

    # Move to end of disk if not already there
    if totalHead != diskSize - 1:
        headMovement += abs(diskSize - 1 - totalHead)
        order.append(diskSize - 1)
        totalHead = diskSize - 1

    # Move left
    for r in left:
        headMovement += abs(totalHead - r)
        order.append(r)
        totalHead = r

    avgSeek = headMovement / len(reqs) if reqs else 0
    time = headMovement  
    thpt = len(reqs) / time if time else 0
    
    return {
        "order": order,
        "head Movement": headMovement,
        "average Seek": avgSeek,
        "throughput": thpt
    }

def c_scan(reqs, startHead, diskSize=200):
    """
    Simulate C-SCAN scheduling algo.
    Args:
        reqs (list): list of disk reqs.
        startHead (int): Initial head pos.
        diskSize (int): max disk track num.
    Returns:
        dict: Contains the service orde , total head movement,
              avg. seek time, and throughput.
    """
    # split reqs into right left
    right = sorted([r for r in reqs if r >= startHead])
    left = sorted([r for r in reqs if r < startHead])

    order = []
    headMovement = 0
    totalHead = startHead

    # right
    for r in right:
        headMovement += abs(r - totalHead)
        order.append(r)
        totalHead = r

    # Move to End
    if totalHead != diskSize - 1:
        headMovement += abs(diskSize - 1 - totalHead)
        order.append(diskSize - 1)
        totalHead = diskSize - 1

    # jump to start
    headMovement += (diskSize - 1)
    order.append(0)
    totalHead = 0

    # Left
    for r in left:
        headMovement += abs(r - totalHead)
        order.append(r)
        totalHead = r

    avgSeek = headMovement / len(reqs) if reqs else 0
    time = headMovement  
    thpt = len(reqs) / time if time else 0

    return {
        "order": order,
        "head Movement": headMovement,
        "average Seek": avgSeek,
        "throughput": thpt
    }



# if __name__ == "__main__":
#     # FCFS Test
#     reqs = [45, 20, 65]
#     startHead = 50
#     print("FCFS:", fcfs(reqs, startHead))
    
#     # SSTF Test
#     print("SSTF:", sstf(reqs, startHead))
    
#     # SCAN Test
#     reqs = [45, 20, 65, 10, 150]
#     print("SCAN:", scan(reqs, startHead))
    
#     # C-SCAN Test
#     print("C-SCAN:", c_scan(reqs, startHead))
