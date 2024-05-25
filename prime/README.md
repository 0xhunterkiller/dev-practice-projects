# Prime - Terminal based Task Driven Work Management

## Config
  - $PRIME_ROOT Root Directory of all your task directories
  - $PRIME_COMPLETED Directory to put all your completed tasks (default $PRIME_ROOT/completed)

## Logical Objects

## Args
- prime
  - create
    - task_name
    - deadline (timeleft)
        ```
          Can be of the form t-x
            - x is the unit of time in consideration. [can be w,d,m,h or s]
            - t is the number of units of the x specified.
            Example :
              2-w -> 2 Weeks | 5-d -> 5 Days | 3-h -> 3 Hours | 10-m -> 10 Minutes | 15-s -> 15 Seconds

          Or a date of the format -> yyyy-mm-dd
        ```
    - priority (default 0) (can be 0,1,2 or 3)
  
  - read
    - (default - show all tasks (sort by deadlines))
    - filter
      - task_name
      - deadline
      - priority
      - count (show only top $count number of tasks)

  - update (user can select from read mode/enter task-name)
    - identifier (task-name)
    - new task_name
    - new deadline
    - new priority
  - delete
    - task_name
    - done (default false)
    - archive (default true)