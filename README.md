# TSP-Deliveries
Package delivery program that addresses the NP-hard Traveling Salesman Problem(TSP). Extracts data from location & package CSV files and 
stores it in chaining hash tables.  Factoring in package-specific deadlines & constraints, creates multiple routes via randomization 
and nearest neighbor algorithm. Selects the shortest route satisfying all delivery constraints, updates delivery status of all packages, 
and outputs the information to the user based on user-input delivery status check-time. Space-time complexity of O(N^2).
