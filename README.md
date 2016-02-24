# Donchian_Channel
Evaluate results of Donchian Channel EA

---------------------------------------------------------------------------------------------------------------------

1. Run Init_pickle_Data.py
    - opens csv files output by MetaTrader
    - reads in and does some initial processing
    - dumps them out to a pickle file to make future reading faster

2. Run Add_Stats.py
    - opens pickled files and adds rolling mean, std, and var for each indicator value and Close price of history
    - re-pickles to file ".._wStats.pickle"

3. Run Merge_Data.py
	- Merges History and/or order data with indicator data
	- pickes to file ".._M_Indicator.pickle"

4.  Eval_Corr.py 
	- determine which orders where profit/loss
	- look for strong correlations between profits and weak corelations to loss

GENERAL FILE INFO:
- Functions.py - to contain common used functions across files
- tester_check.ipynb - used to check and devlop Check_PL.py

NEXT STEPS ----
- go back to MT and remove () from indicator data, its a pain to type and not needed
- look ahead in data determine which ones would be profit/loss

---------------------------------------------------------------------------------------------------------------------
DEPRECATED THOUGHTS

-not working, for some reason not getting same results out of MT that was before so trends look different (note for future eval need to have better documentation of runs with all conditions, including spread, etc, be better about saving reports)

2.  Run Add_Trends.py
    - opens pickled data files
    - adds trends based on pre-defined ranges from viewing order data
3. Run BreakSR.py
    - opens ..wStats
    - merged indicator with history
    - determines when support/resistance line is broken
    - pickles history_M_Indicator.pickle

4. Check_PL.py
	- "should" search through price history data (history_M_Indicator.pickle) and find where the price [bar-1] breaks the support or resistance line
	- then will look forward to determine if BUY & SELL will end in a profit or a loss
	- plan is from here to determien if there is some correlation between PL's and some of the indicator data to determien when to open order and what type of order it should before
need to look into module to chart order data and maybe run an MA to set/help determine trends

old 3. Was looking to use Compute_Indicators.py & Indicators.py to add indicators in python, but decided against it.  - may not compute exactly the same as in MT4, will ultimately be time consuming and due to first reason not ultimately worth it

-- decided not to do, use matplot and panda to eval this instead.  redo Donchian Channel in MT to report indicator data when support resistance line is broken if I know every time it s broken, can pandas determine if profit or loss


no longer relevant - order data not in indicator data.  make df of orders from indicator data, will have ind data and stats at time of order open merge with order data frame, want ind, stats at order open, order close info, profit, etc

?? do I need to have balance graph (may make some charts make more sense) can pull from MT report, no wo order data
can not do

---------------------------------------------------------------------------------------------------------------------