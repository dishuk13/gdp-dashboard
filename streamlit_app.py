import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    # Detect year columns dynamically to avoid dropping newer years in the dataset
    year_cols = [col for col in raw_gdp_df.columns if str(col).isdigit()]

    # Pivot all those year-columns into two: Year and GDP, keeping country name and code
    gdp_df = raw_gdp_df.melt(
        ['Country Name', 'Country Code'],
        year_cols,
        'Year',
        'GDP',
    )

    # Convert types
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df['GDP'] = pd.to_numeric(gdp_df['GDP'], errors='coerce')

    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

# Use a sorted list for a better UX
countries = sorted(gdp_df['Country Code'].unique().tolist())

# Removed an incorrect warning that checked the available countries instead of the selection

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# Validate selection properly and stop the script if nothing is selected
if not selected_countries:
    st.warning('Select at least one country')
    st.stop()

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

''
''

# No need to pre-slice by the endpoints only; we'll handle missing values robustly per country

st.header('Latest GDP within selected range', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        country_df = (
            filtered_gdp_df[filtered_gdp_df['Country Code'] == country]
            .dropna(subset=['GDP'])
            .sort_values('Year')
        )

        if country_df.empty:
            st.metric(
                label=f'{country} GDP',
                value='n/a',
                delta='n/a',
                delta_color='off'
            )
        else:
            first_gdp_val = country_df['GDP'].iloc[0] / 1_000_000_000
            last_gdp_val = country_df['GDP'].iloc[-1] / 1_000_000_000

            if not math.isfinite(first_gdp_val) or first_gdp_val <= 0 or not math.isfinite(last_gdp_val):
                growth = 'n/a'
                delta_color = 'off'
            else:
                growth = f'{last_gdp_val / first_gdp_val:,.2f}x'
                delta_color = 'normal'

            st.metric(
                label=f'{country} GDP',
                value=f'{last_gdp_val:,.0f}B' if math.isfinite(last_gdp_val) else 'n/a',
                delta=growth,
                delta_color=delta_color
            )
