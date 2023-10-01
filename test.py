from app import Manipulate, get_the_all_major
# school = "UC Berkeley"
# year_time = ["2021", "2022"]
# major_list = list(get_the_all_major(school)["Major_name"])
# stat_list = ["Major_name", "Yield_rate"]
# vizz_instance = Manipulate(school, year_time, major_list, stat_list, False)
# vizz_instance.sql_method()
# a = vizz_instance.data
# print(a)

statistic_option = ["Admit_GPA_range","Admit_rate","Enroll_GPA_range","Yield_rate","Admits","Applicants","Enrolls"]

school = "UC Berkeley"
option = "Check the table data"

if option == "Check the table data":
   # year_time = [[str(i) for i in range(2012, 2022)][0]]
   year_time = [i for i in range(2012, 2023)]
   major_list = list(get_the_all_major(school)["Major_name"])
   viz_instance = Manipulate(school, year_time, major_list, statistic_option, False)
   viz_instance.sql_method()
   a = viz_instance.data
   print(a)