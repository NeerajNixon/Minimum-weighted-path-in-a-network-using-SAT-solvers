Abhishek M 200070003
Neeraj Nixon 20d070056

Execution details :

1) Run the python_main.py file
2) Input format for the GUI :
	
	1st box = No. of nodes
	2nd box = Connections in the topology and their corresponding  weights
		  (example given below)
	3rd box = The endpoints for which we have to find the least weighted path

--------------------------------------------------------------------------------------------------------------------

	Example for input for 2nd box :
	A connection in the topology is defined as an edge from a from_node to a to_node and a corresponding weight
	assigned to it
	
	Therefore, Connection representation = (from_node, to_node, weight) == lets take (1,4,1) (1,7,1) (1,9,1)
	Then for this the input format for the 2nd box will be = 1 4 1 1 7 1 1 9 1

	Note: 
	Good testcases are given in the testcases.txt file

--------------------------------------------------------------------------------------------------------------------

3) After giving the input in the GUI and pressing "Submit", we show the topology that the user has just provided
4) Closing the input GUI tab will generate the least weighted path between the given 2 nodes.


     ----------------------------------------------------------------------------
     |  IMPORTANT NOTE :							|
     |  WITHOUT CLOSING THE GUI TAB, THE REQUIRED OUTPUT WILL NOT BE GENERATED  |
     ----------------------------------------------------------------------------