# movie-theater-seating-python-sqlite3

## Introduction 

Movie Theater Seating project allocates seats in a movie theater to incoming requests in an efficient way which maximizes theater profit as well as gives closely located seats made in a single request. 
In the current support it is capable of taking seat reservation request input from a text file and writes the seat reservation details to an output file. The seat configurations and other information related to the movie theater are fetched from a sqlite database. 
After allocation, the reserved seats are updated against he reservation IDs in the database. However the design is flexible to take inputs and dispatch outputs to any source with code extension.

## Usage 

Goto the directory containing movie-theater-seating project and run the commands below. 
This generates a reservation output file for seat reservation requests passed via the input file.

```
cd movie-theater-seating/ 
```

```
python allocator.py <database> <inputfile> <outputfile>
```

## Parameters 

```
database : Name of the database the service should connect to.
inputfile : Input file holding the request identifier and seats requested data in format [RXXXX][#number].
outputfile : File path where the reservation output is saved in format [REQ_ID][Seat Identifiers].
```

## Sample 

```
mts suchethapanduranga$ python allocator.py movie_seating.db sample-input.txt sample-output.txt
```

## Assumptions

1. Table structure of 'reservations' will remain as is, i.e. reservationID--seat. 
2. The theater comprises of only one class of seats. 
3. Seat allocation is done on first come first serve basis. 
4. All seats are assumed to be empty during the start of program.

## Code Structure 

1. The code has been seggregated into appropriate classes based on the OOP norms.
2. Numpy array has been used to store the seat allocation information (i.e. Seat number and row number).
3. Data structure such as lists and arrays have been used to store the values as per the requirement of the program.

## Discussion

This project demonstrates the use of data structures, classes, unit testing and using database in python programming. 
However, the task can be achieved using only lists or dictionaries data structure 
but upon research, it was evident that the most efficient approach is to use a sparse matrix using numpy. 
Sparse matrices are efficient, fast to process or perform calculation and easy to store because of binary values.

Moreover, from the point of data structures, this problem can also be solved using graph networks by applying greedy algorithms or greedy approach. 
That will allocate the seats to passenger in a group together using minimal traversal and by finding out number of empty seats connected to a particular vertex (i.e. finding subgrapgh of empty seats). 
Weights can be assigned to the edges between empty node and occupied node which can help to find empty seats in a walk. 
