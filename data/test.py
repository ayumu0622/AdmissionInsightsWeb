from updated_app import *
from gcp import *

school = "UC Berkeley"
year_time = 2022
major_list = list(get_the_all_major(school)["Major_name"])
viz_instance = Manipulate(school, year_time, major_list, None, False)
viz_instance.sql_method()