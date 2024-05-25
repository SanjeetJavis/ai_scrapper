
from scrapper import controller
import pandas as pd

# Subset of websites you want to search
run_name = 'last_24_wild_life_conflict'
sites = [
    'timesofindia.indiatimes.com', "bhaskar.com", "news24online.com", "sikkimtimes.com", "deccanchronicle.com"
]
# Keywords you want to search for
THEME = 'conflict between wildlife and human beings'
keywords = ['elephant', 'tiger', 'conflict']
questions = [
    "humans_injured(Numeric): How many humans were injured ?"
    "humans_killed(Numeric): How many humans were killed ?",
    "wildlife_involved(List): what kind of wildlife was involved in the conflict ?",
    "wildlife_injured(Numeric): How many of the wildlife were injured ?",
    "wildlife_killed(Numeric): How many of the wildlife were killed ?",
    "conflict_location(String): what was the location of the conflict ?",
    "is_single_event(Boolean): is the article about a single event ?",
    "conflict_summary(String): Summarise the conflict within 20 words"
]


run_name = 'last_24_wild_life_conflict'
sites = [
    'timesofindia.indiatimes.com', "bhaskar.com", "news24online.com", "sikkimtimes.com", "deccanchronicle.com"
]
# Keywords you want to search for
THEME = 'conflict between wildlife and human beings'
keywords = ['elephant', 'tiger', 'conflict']
questions = [
    "humans_injured(Numeric): How many humans were injured ?"
    "humans_killed(Numeric): How many humans were killed ?",
    "wildlife_involved(List): what kind of wildlife was involved in the conflict ?",
    "wildlife_injured(Numeric): How many of the wildlife were injured ?",
    "wildlife_killed(Numeric): How many of the wildlife were killed ?",
    "conflict_location(String): what was the location of the conflict ?",
    "is_single_event(Boolean): is the article about a single event ?",
    "conflict_summary(String): Summarise the conflict within 20 words"
]
#
#
# run_name = 'last_24_rain'
# sites = [
#     'timesofindia.indiatimes.com', "bhaskar.com", "news24online.com", "sikkimtimes.com", "deccanchronicle.com"
# ]
# THEME = 'rainfall'
# keywords = ['rain']
# questions = [
#     "rain_location(Numeric): where did it rain ?"
#     "rain_time(Numeric): how long did it rain for (in hours), if not mentioned give NA ?"
#     "temperature_after_rain(Numeric): what was the temparature after rain ?"
# ]


# # run_name = 'ea_coverage_in_last_2_years_india'
# # sites = [
# #     'timesofindia.indiatimes.com', "bhaskar.com"
# # ]
# # # Keywords you want to search for
# # THEME = ''
# # keywords = ['google']
# # questions = [
# #       "sentiment_towards_google (String) :what is the sentiment towards google in this article ?",
# #        "2_Sentence_summary (Strimg)"
#
# ]




output = controller(sites, keywords, THEME, questions)

output = pd.DataFrame(output)
output.to_csv(f'{run_name}.csv', index=False)