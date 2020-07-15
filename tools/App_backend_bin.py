''' This is the main bin for storing backend calculations required for various pages of the macro dash app. The required calculations are based on an open ODBC connection to the SQL database, with access to data table computed by the dash Core module daily '''
import pyodbc
import datetime
import pandas as pd

def bday_pulse(conn_str, **flter):

    ''' Function for retriving and generating pulse score attribution for each business date between the earliest and most recent release date available.
    Input
    -----
    conn_str: ODBC connection str
    Keyword args = **filters - used to subset by
    - country: list of countries (ccys) to retrive, default is all
    - sector: list of sectors to retrive, default is all
    - data_name: list of str for data_name, default is all
    '''

    # Import dependencies
    import pyodbc
    import pandas as pd

    # Define main data table map
    ccy_map = {'country':['Australia', 'United State', 'Eurozone', 'New Zealand', 'United Kingdom', 'Switzerland', 'Canada', 'Japan', 'Norway', 'Sweden', 'Turkey', 'South Africa', 'Mexico', 'Singapore', 'China'], 'currency':['AUD', 'USD', 'EUR', 'NZD', 'GBP', 'CHF', 'CAD', 'JPY', 'NOK', 'SEK', 'TRY', 'ZAR', 'MXN', 'SGD', 'CNH']}
    summary_tbl_map = pd.DataFrame.from_dict(ccy_map)

    ## Test connection & raise exception message if fails
    try:
        conn = pyodbc.connect(conn_str) # Create PYODBC connection for the instance
    except Exception as e:
        print('Error in establishing PYODBC connection: \n' + e)
        return

    ## retrieve data pulse table
    try:
        sql_tbl = pd.read_sql("SELECT * FROM dbo.pulse_score", conn)  # SQL statement to execute. May need to update if DB structure change
    except Exception as e:
        print('Error in reading SQL table. Error message:' + e)
        return

    # Process key argument filters on sql_tbl
    for filter_var in flter:
        if filter_var == 'country':
            sql_tbl = sql_tbl[sql_tbl['country'].isin(flter[filter_var])]
        if filter_var == 'sector':
            sql_tbl = sql_tbl[sql_tbl['sector'].isin(flter[filter_var])]
        if filter_var == 'data_name':
            sql_tbl = sql_tbl[sql_tbl['data_name'].isin(flter[filter_var])]
        if filter_var not in ['country', 'sector', 'data_name']:
            print('Filter variable must be one of country, sector or data_name!')
            return

    # Clean up and aggregate to get business date indicators
    ''' First construct a dataframe of bus_date. Merge this with full data table and forward fill Pulse_cont for country / sector. Finally clean up'''

    ccy_pulse = sql_tbl[['release_date','country','pulse_cont']].groupby(['release_date','country']).sum().reset_index() # Sum by release_date / country combination
    ccy_pulse.rename(columns={'country':'currency', 'pulse_cont':'Pulse'}, inplace=True) # Reanme...

    # Generate a bus_day / full currency df for merging
    bday_ts = pd.bdate_range(start=min(sql_tbl['release_date']), end=max(sql_tbl['release_date']))
    unique_ccy = sql_tbl['country'].unique().tolist()

    # Create a Dataframe of business day / CCY combination
    bday_lst = bday_ts.to_list() * len(unique_ccy)
    ccy_lst = unique_ccy * len(bday_ts)
    ccy_lst.sort() # Need to sort so that each bday_ts is corresponding to one unique currency. Order doens't matter.

    bday_pulse_df = pd.DataFrame(list(zip(bday_lst, ccy_lst)), columns=['business day','currency'])

    bday_pulse_df = bday_pulse_df.merge(ccy_pulse, how='left', left_on=['business day','currency'], right_on=['release_date','currency']) # This would give the full rows of business days, albeit NA value for there not to be a release on that day

    # Now forward-fill Pulse time series for each currency and compute percentile
    bday_pulse_filled = pd.DataFrame()
    for ccy in unique_ccy:

        flt = bday_pulse_df['currency'] == ccy
        ccy_ts = bday_pulse_df[['business day', 'currency', 'Pulse']][flt].sort_values(by='business day', ascending=True).fillna(method='ffill')
        ccy_ts['PCT'] = ccy_ts['Pulse'].rank(pct=True) # Create a percentile rank

        bday_pulse_filled = bday_pulse_filled.append(ccy_ts) # Append

    bday_pulse_filled = bday_pulse_filled.merge(summary_tbl_map, how='left', on='currency') # Now map country onto the df

    # Finally cleaning up to multilevel index - sum shouldn't aggregate anything - can check by looking at shape attr - should be identical
    bday_pulse_final = bday_pulse_filled.groupby(['business day','country', 'currency']).sum()

    return bday_pulse_final

def bday_econ_ts(conn_str, **flter):
    ''' Function for retriving and generating economic data time series for each business date between the earliest and most recent release date available.

    Input
    -----
    conn_str: ODBC connection str
    Keyword args = **filters - used to subset by
    - country: list of countries (ccys) to retrive, default is all
    - sector: list of sectors to retrive, default is all
    - data_name: list of str for data_name, default is all
    Ouput
    -----
    dataframe
    '''

    # Import dependencies
    import pyodbc
    import pandas as pd

    # Define main data table map
    ccy_map = {'country':['Australia', 'United State', 'Eurozone', 'New Zealand', 'United Kingdom', 'Switzerland', 'Canada', 'Japan', 'Norway', 'Sweden', 'Turkey', 'South Africa', 'Mexico', 'Singapore', 'China'], 'currency':['AUD', 'USD', 'EUR', 'NZD', 'GBP', 'CHF', 'CAD', 'JPY', 'NOK', 'SEK', 'TRY', 'ZAR', 'MXN', 'SGD', 'CNH']}
    summary_tbl_map = pd.DataFrame.from_dict(ccy_map)

    ## Test connection & raise exception message if fails
    try:
        conn = pyodbc.connect(conn_str) # Create PYODBC connection for the instance
    except Exception as e:
        print('Error in establishing PYODBC connection: \n' + e)
        return

    ## retrieve data pulse table
    try:
        sql_tbl = pd.read_sql("SELECT * FROM dbo.eco_data", conn)  # SQL statement to execute. May need to update if DB structure change
    except Exception as e:
        print('Error in reading SQL table. Error message:' + e)
        return

    # Process key argument filters on sql_tbl
    for filter_var in flter:
        if filter_var == 'country':
            sql_tbl = sql_tbl[sql_tbl['country'].isin(flter[filter_var])]
        if filter_var == 'sector':
            sql_tbl = sql_tbl[sql_tbl['sector'].isin(flter[filter_var])]
        if filter_var == 'data_name':
            sql_tbl = sql_tbl[sql_tbl['data_name'].isin(flter[filter_var])]
        if filter_var not in ['country', 'sector', 'data_name']:
            print('Filter variable must be one of country, sector or data_name!')
            return

    # Clean up and aggregate to get business date indicators
    ''' First construct a dataframe of bus_date. Merge this with full data table and forward fill pulse_cont for country / sector. Finally clean up'''

    eco_data = sql_tbl[['release_date','effective_date', 'country', 'sector', 'data_name', 'bbg_code', 'value']]
    eco_data.rename(columns={'country':'currency'}, inplace=True) # Reanme.

    # Generate bus_day datetime ts and full currency list
    bday_ts = pd.bdate_range(start=min(sql_tbl['release_date']), end=max(sql_tbl['release_date']))
    unique_ccy = eco_data['currency'].unique().tolist()

    # Calculation logic: First filter for currency, then generate full bday time series (forward filled) for each unique indicator given currency
    bday_eco_filled = pd.DataFrame()
    for ccy in unique_ccy:

        flt = eco_data['currency'] == ccy # First filter for currency
        unique_data = eco_data[flt]['data_name'].unique()
        bday_eco_ccy_df = eco_data[flt] # Work with ccy filtered subset in the loop

        for data in unique_data:

            # Create a Dataframe of business day / CCY / data combination

            #ccy_lst = unique_ccy * len(bday_ts)
            #ccy_lst.sort() # Need to sort so that each bday_ts is corresponding to one unique currency. Order doens't matter.

            bday_lst = bday_ts.to_list()
            bday_eco_df = pd.DataFrame(bday_lst, columns=['business day'])

            bday_eco_df = bday_eco_df.merge(bday_eco_ccy_df[bday_eco_ccy_df['data_name']==data], how='left', left_on=['business day'], right_on=['release_date']) # This would give the full rows of business days, albeit NA value for there not to be a release on that day

            eco_ts = bday_eco_df[['business day', 'effective_date', 'currency', 'sector', 'data_name', 'value']].sort_values(by=['business day','data_name'], ascending=True).fillna(method='ffill')

            bday_eco_filled = bday_eco_filled.append(eco_ts) # Append

    bday_eco_filled = bday_eco_filled.merge(summary_tbl_map, how='left', on='currency') # Now map country onto the df

    # Final production cleaning = order by ccy > sector > name > bday. DropNA if All and reset index
    bday_eco_final = bday_eco_filled.sort_values(by = ['currency', 'sector', 'data_name', 'business day']).dropna(axis=0, how = 'all', subset = ['currency', 'sector', 'data_name', 'value', 'country']).reset_index()

    return bday_eco_final

def main_tbl_data_calc(T, bday_pulse_data):

    ''' Function for calculating the data frame structure for feeding Dash datatable on summary table.
    Input:
    -----
    T = datetime object of the spot date
    bday_pulse_data = data fram of Pulse score and PCT by Business Day, Country and Currency index
    '''

    # Import Dependencies
    import pandas as pd
    from functools import reduce # For reduce function

    # Business date corrections
    T = T + pd.tseries.offsets.BDay(1) + pd.tseries.offsets.BDay(-1)
    T_30 = T + pd.tseries.offsets.BDay(-30)
    T_90 = T + pd.tseries.offsets.BDay(-90)

    # Extract multilevel table for aggregated pulse score
    pulse_T = bday_pulse_data.loc[T]
    pulse_Delta_T_30 = pulse_T- bday_pulse_data.loc[T_30]
    pulse_Delta_T_30.rename(columns={'Pulse':'Delta T-30D'}, inplace=True)
    pulse_Delta_T_90 = pulse_T - bday_pulse_data.loc[T_90]
    pulse_Delta_T_90.rename(columns={'Pulse':'Delta T-90D'}, inplace=True)

    # Finally compile data table for Dash DataTable
    '''
    Dash App format:
    Country | Currency | T | Delta T-30D | Delta T-90D | Historical PCT |
    '''
    # Create main_tble_data by sequentially merging left to right 3 data frames: pulse_t, pulse_Delta_T30, pulse_Delta_T90 keeping only the Delta columns in the later two

    main_tbl_data = reduce(lambda left,right: pd.merge(left, right, on=['Country','Currency'], how='left'), [pulse_T, pulse_Delta_T_30['Delta T-30D'], pulse_Delta_T_90['Delta T-90D']])

    # Format float percentile into PERCENTILE
    main_tbl_data['PCT'] = main_tbl_data['PCT'] * 100
    main_tbl_data['PCT'] = main_tbl_data['PCT'].astype(int) # Conver to int
    main_tbl_data = main_tbl_data.sort_values(by='Country').round(1).reset_index() # Sort Alphabetical, reset and round

    # Adding utf-8 emoji for bias
    ''' Current rule for building bias is to break into 5 categories
    Outright positive: Pulse >= 50
    Positive: Pulse in (0, 50)
    Flat: Spot pulse at zero
    Negative: Spot pulse in (-50, 0)
    Outright Negative: Spot pulse <-50
    '''
    # -*- coding: utf-8 -*-
    # unfortunately VS Code doesn't fully support utf-8, but funny enough this translates alright through dash....
    main_tbl_data['Bias'] = main_tbl_data['Pulse'].apply(lambda x: '⬇️' if x <= -50 else('↙️' if x <0 else ('⬅️' if x ==0 else('↗️' if x <50 else ('⬆️')))))

    # Finally re-arrange main datatable feed for Dash, rename Delta cols
    final_col_order = ['Country','Currency','Pulse','PCT','Bias','Delta T-30D','Delta T-90D']
    main_tbl_data = main_tbl_data[final_col_order]
    main_tbl_data.rename(columns={'Delta T-30D':'Pulse 🛆30D', 'Delta T-90D':'Pulse 🛆90D'}, inplace=True)

    return main_tbl_data

def main_tbl_ctymap(main_tbl_data):

    ''' Function that produces a figure object for choropleth map of the current Pulse level.
    Input
    -----
    main_tbl_data = data parsed to the main dash data table with the correct as of date T '''

    # Import Dependencies
    import pandas as pd
    import plotly.graph_objects as go

    # Define map between Country Name, ISO Alpha-3
    iso_map_exEU = {'Country':
                ['Australia', 'United State', 'New Zealand', 'United Kingdom', 'Switzerland', 'Canada', 'Japan', 'Norway', 'Sweden', 'Turkey', 'South Africa', 'Mexico', 'Singapore', 'China'],
                'ISO_code':
                ['AUS', 'USA', 'NZL', 'GBR', 'CHE', 'CAN', 'JPN', 'NOR', 'SWE', 'TUR', 'ZAF', 'MEX', 'SGP', 'CHN']}

    iso_map_EU = {'Country':
            ['Eurozone'] * 19,  # 19 Eurozone monetary union members
            'ISO_code':
            ['AUT', 'BEL', 'CYP', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA',  'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'PRT', 'SVK', 'SVN', 'ESP']}

    # Left merge vs. latest data table
    iso_map_full = {key:iso_map_exEU[key] + iso_map_EU[key] for key in iso_map_EU}
    iso_map_df = pd.DataFrame.from_dict(iso_map_full)
    country_map = iso_map_df.merge(main_tbl_data[['Country', 'Pulse']], how = 'left', on='Country')

    # Create plotly graph object - need to work on the visualisation parameters later
    fig = go.Figure(data = go.Choropleth(
        locations = country_map['ISO_code'],
        z = country_map['Pulse'],
        text = country_map['Country'],
        colorscale = 'Blues',
        reversescale = True,
        marker_line_color = 'darkgray',
        marker_line_width = 0.5,
        colorbar_title = 'Pulse Score',
        zmax = 100,
        zmin = -100
    ))

    return fig

def cb_tbl_data_calc(ccy:str, start_date, end_date, bday_econ_data):
    ''' placeholder for calculating required data for cb analysis table'''

    import datetime
    import pandas as pd

    # Short function for dealing with conversion
    def dt2qtrformat(date):
        import math
        return 'Q{}-{}'.format(str(math.ceil(date.month/3)), str(date.year-2000))

    # Deal with non-business day input & dates outside of valid range
    start_date = max(start_date + pd.tseries.offsets.BDay(1) + pd.tseries.offsets.BDay(-1), min(bday_econ_data['business day']))
    end_date = min(end_date + pd.tseries.offsets.BDay(1) + pd.tseries.offsets.BDay(-1), max(bday_econ_data['business day']))

    # Add a switch to fix the scenario where input start_date is more than end date
    if start_date >= end_date:
        start_date = end_date # cap start_date at most end_date. Also catches scenarios where two dates are the same (i.e. =)
        out_cols = ['data name', 'sector', datetime.datetime.strftime(end_date, '%d-%h-%y'), 'verdict']
    else:
        out_cols = ['data name', 'sector', datetime.datetime.strftime(end_date, '%d-%h-%y'), datetime.datetime.strftime(start_date, '%d-%h-%y'), 'verdict']

    # Generate currency & date based filters
    flt = (bday_econ_data['currency'] == ccy) & ((bday_econ_data['business day'] == start_date) | (bday_econ_data['business day'] == end_date))
    #bday_econ_data[flt]

    # First map to 'Economic Activities' vs. 'Inflation'
    cb_main_tbl = bday_econ_data[flt][['business day', 'effective_date', 'sector', 'data_name', 'value', 'score_direction', 'freq']].reset_index(drop=True)

    cb_main_tbl['sector'] = cb_main_tbl['sector'].map({'Employment':'Economic Activities','Growth':'Economic Activities', 'Housing':'Economic Activities', 'Survey':'Economic Activities','Inflation':'Inflation'})

    cb_main_tbl['effective_date_fmt'] = [datetime.datetime.strftime(x, '%b-%y') if y == 'Monthly' else dt2qtrformat(x) for x, y in zip(cb_main_tbl['effective_date'], cb_main_tbl['freq'])]

    # Loop for computing table feeding Dash data table
    bull_bear, values_end, values_start, sector, data_name, verdict = [], [], [], [], [], []
    for data in cb_main_tbl['data_name'].unique():

        # Filter and generate Bull / Bear indicators
        flt1 = (cb_main_tbl['business day'] == start_date) & (cb_main_tbl['data_name'] == data)
        flt2 = (cb_main_tbl['business day'] == end_date) & (cb_main_tbl['data_name'] == data)

        # Append for final table to show
        data_name.append(data)
        sector.append(cb_main_tbl['sector'][flt2].item()) # append sector
        values_end.append(cb_main_tbl['value'][flt2].item())
        direction = cb_main_tbl['score_direction'][flt2].item()

        if (cb_main_tbl['value'][flt1].size >0):
            delta = cb_main_tbl['value'][flt2].item() - cb_main_tbl['value'][flt1].item()
            values_start.append(cb_main_tbl['value'][flt1].item())
            if (delta * direction) > 0:
                bull_bear.append(1) # Bullish = 1
                verdict.append('bullish')
            elif (delta * direction) == 0:
                bull_bear.append(0) # Neutral = 0
                verdict.append('neutral')
            else:
                bull_bear.append(-1) # Bearish = -1
                verdict.append('bearish')
        else:
            delta =  'N/A' # N/A delta since no prior reading
            values_start.append('N/A') # N/A prior reading
            bull_bear.append('N/A')
            verdict.append('N/A')

    col_nms = ['data name', 'sector', datetime.datetime.strftime(end_date, '%d-%h-%y'), datetime.datetime.strftime(start_date, '%d-%h-%y'), 'bull_bear', 'verdict'] # This still contains both start and end_date even for duplicate dates.

    main_tbl_df = pd.DataFrame(zip(data_name, sector, values_end, values_start, bull_bear, verdict), columns=col_nms).sort_values(by = ['sector','data name']) # Generate final table sort by sector and data name

    main_tbl_data = main_tbl_df[out_cols].reset_index(drop=True)
    main_tbl_data = main_tbl_data.loc[:, ~main_tbl_data.columns.duplicated()] # Drop duplicate roles - in case of same start/end date selected

    return main_tbl_data, main_tbl_df


def top_mover_tbl(conn_str,period1,period2,N):
    ''' Function is used to generate data for the top_movers table on Currency page '''
    def get_price(tickers,date):
        try:
            return float(prices[(prices['bbg_code']==tickers) & (prices['effective_date']==date)].value)
        except:
            return 1

        ## Test connection & raise exception message if fails
    # try:
    conn = pyodbc.connect(conn_str) # Create PYODBC connection for the instance
    # except Exception as e:
    #     print('Error in establishing PYODBC connection: \n' + e)
    #     return

    end_date=datetime.date.today()-pd.tseries.offsets.BDay(1)
    start_date=end_date-pd.tseries.offsets.BDay(period2)
    ccys=pd.read_csv(r"C:\Git\python-dash-app\app_assets\tracked_security.tXT",header=None,names=['tickers'])
    ccys['end_date']=end_date
    ccys['start_date_near']=end_date-pd.tseries.offsets.BDay(period1)
    ccys['start_date_far']=end_date-pd.tseries.offsets.BDay(period2)
    ccys['ccy1']=ccys['tickers'].str[:3] +'USD Curncy'
    ccys['ccy2']=ccys['tickers'].str[3:] +'USD Curncy'

    sqlstr="SELECT * from dbo.prices where effective_date>=? and effective_date<=?"
    prices=pd.read_sql(sqlstr,conn,params=[start_date,end_date])
    # Looping through each ccy to calculate pct return.
    for index, row in ccys.iterrows():
        ccys.loc[index,'end_date_px']=get_price(ccys.loc[index,'ccy1'],ccys.loc[index,'end_date'])
        ccys.loc[index,'start_date_near_px']=get_price(ccys.loc[index,'ccy1'],ccys.loc[index,'start_date_near'])
        ccys.loc[index,'start_date_far_px']=get_price(ccys.loc[index,'ccy1'],ccys.loc[index,'start_date_far'])

        ccys.loc[index,'end_date_px_ccy2']=get_price(ccys.loc[index,'ccy2'],ccys.loc[index,'end_date'])
        ccys.loc[index,'start_date_near_px_ccy2']=get_price(ccys.loc[index,'ccy2'],ccys.loc[index,'start_date_near'])
        ccys.loc[index,'start_date_far_px_ccy2']=get_price(ccys.loc[index,'ccy2'],ccys.loc[index,'start_date_far'])


    ccys['ticker_px_end']=round(ccys['end_date_px']/ccys['end_date_px_ccy2'],4)
    ccys['ticker_px_start_near']=ccys['start_date_near_px']/ccys['start_date_near_px_ccy2']
    ccys['ticker_px_start_far']=ccys['start_date_far_px']/ccys['start_date_far_px_ccy2']

    ccys['st_px_chng']=round((ccys['ticker_px_end']/ccys['ticker_px_start_near']-1),4)
    ccys['lt_px_chng']=round((ccys['ticker_px_end']/ccys['ticker_px_start_far']-1),4)
    S=ccys[['tickers','ticker_px_end','st_px_chng','lt_px_chng']]

    S.columns=['ticker','price','st_chng','lt_chng']
    S=S.reindex(S.st_chng.abs().sort_values(ascending=False).index)
    S = S.reset_index(drop=True)

    return S.iloc[0:N]

def get_prices(raw_data,ccy1,ccy2):

    price=raw_data[(raw_data['bbg_code']==ccy1+'USD Curncy') | (raw_data['bbg_code']==ccy2+'USD Curncy')]
    price.set_index('effective_date',inplace =True)
    price.index.rename('business day',inplace=True)
    price.sort_index(inplace=True)

    price_1=price[price['bbg_code']==ccy1+'USD Curncy']
    price_2=price[price['bbg_code']==ccy2+'USD Curncy']
    price_chart=pd.concat([price_1, price_2], axis=1).fillna(method='ffill')
    if ccy2=='USD':
        price_chart['rate']=price_chart.iloc[:,2]
    elif ccy1=='USD':
        price_chart['rate']=1/price_chart.iloc[:,5]
    else:
        price_chart['rate']=price_chart.iloc[:,2]/price_chart.iloc[:,5]

    return price_chart[['rate']]

def pulse_graph(raw_pulse,price,ccy1,ccy2,m_a,last_n):

    '''Create dataframe for pulse_main_graph object
       -ccy1 & ccy2 are three letter ccy codes for countries,
       -m_a is the moving average period of net pulse,
       -last_n is how many rows of the df to show in chart '''

    if not isinstance(m_a,int):
        m_a=20

    spot_price=get_prices(price,ccy1,ccy2)

    ccy1_pulse=raw_pulse.iloc[raw_pulse.index.get_level_values('currency') == ccy1]
    ccy2_pulse=raw_pulse.iloc[raw_pulse.index.get_level_values('currency') == ccy2]

    graph_df=pd.merge(ccy1_pulse,ccy2_pulse, how='left',on='business day',suffixes=('_ccy1', '_ccy2'))
    graph_df['Pulse_net']=graph_df['Pulse_ccy1']-graph_df['Pulse_ccy2']
    graph_df['average']=graph_df['Pulse_net'].rolling(m_a).mean()

    graph_df=pd.merge(graph_df,spot_price,how='left',on='business day')

    graph_df_final=graph_df.tail(last_n)

    return graph_df_final

def data_dropdown(conn_str,country,sector):

    conn = pyodbc.connect(conn_str)

    if sector=='Economic Activity':
        sqlstr='''SELECT DISTINCT data_name,sector FROM dbo.eco_data WHERE country=? and sector in ('Survey', 'Employment','Growth','Housing') ORDER BY sector'''
    else:
        sqlstr='''SELECT DISTINCT data_name,sector FROM dbo.eco_data WHERE country=? and sector in ('Inflation') ORDER BY sector'''

    data_list=pd.read_sql(sqlstr,conn,params=[country])

    return data_list['data_name'].values.tolist()
