```c
MPI_Init(&argc,&argv);
MPI_Comm_rank(MPI_COMM_WORLD,&rank);
MPI_Comm_size(MPI_COMM_WORLD,&size);
MPI_Abort(MPI_COMM_WORLD,1);
MPI_Send(&msg,count,MPI_INT,partner,tag,MPI_COMM_WORLD);
MPI_Recv(&msg,count,MPI_INT,partner,tag,MPI_COMM_WORLD,MPI_STATUS_IGNORE);

// Special Functions
MPI_Scatter(sendbuf,sendcount,MPI_FLOAT,recvbuf,recvcount,MPI_FLOAT,source,MPI_COMM_WORLD);
MPI_Gather(sendbuf,sendcount,MPI_FLOAT,(Where to store in source),(Number of elements each process is sending),MPI_FLOAT,source,MPI_COMM_WORLD);
MPI_Bcast(&buf, 1, MPI_INT, root, MPI_COMM_WORLD);
MPI_Reduce((Variable to take data from in each process),(Where to store in source),(How many variables will Reduce be getting),MPI_INT,MPI_SUM,source,MPI_COMM_WORLD);
```

# CLOCK SYNC

* Broadcast Right Min and Hour (Time in Server)
* Calculate and Send Difference from other clocks
* Server calculates average difference in other clocks and sets its time accordingly and sends the difference to other clocks.
    send = (diff1+diff2)/3
    ...Change Time in Server
    diff1 = send - diff1
    diff2 = send - diff2
* Send the difference to the respective clocks
* Set time in the other clocks

# Leader Election
* Set a uid for every process (uid = (rand() * (rank+1) * size)%100)
* Calculate the next and previous for every process
* Send your uid to the successor.(next)
* While TRUE:
*   Recv from prev (any tag)
*   if TAG == 201
        Send the received message to the next
        break
    else:
        round = st.MPI_TAG
        if (recv == uid)
            Declare urself as leader
            send 201 as tag
            break
        else if (recv > uid):
            Send received message to next with incremented tag (round + 1)
