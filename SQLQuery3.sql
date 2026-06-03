Select Gender , Count(Gender) as Totalcount , 
count(Gender) * 100.0 / (Select count(*) from Customer_Data) as Percentage
from Customer_Data
Group by Gender



Select Contract , Count(Contract) as Totalcount , 
count(Contract) * 100.0 / (Select count(*) from Customer_Data) as Percentage
from Customer_Data
Group by Contract

Select State , Count(State) as Totalcount , 
count(State) * 100.0 / (Select count(*) from Customer_Data) as Percentage
from Customer_Data
Group by State
order by Percentage desc