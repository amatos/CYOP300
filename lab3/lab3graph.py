"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Function to plot the top 5 states with the highest population.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

try:
    import lab3common
    import lab3prompt
    import lab3search_states
    import lab3states
    import lab3modify_pop
except ImportError:
    from . import lab3common
    from . import lab3prompt
    from . import lab3search_states
    from . import lab3states
    from . import lab3modify_pop


def plot_top_5_state_populations() -> None:
    """
    This function visualizes the population of the top 5 states with the highest
    population. The data is sorted in descending order based on population,
    and a bar chart is plotted to represent the results. The chart includes
    population values annotated on each bar.

    :return: None
    :rtype: None
    """

    # Load the state data using the States class.
    state_data = lab3states.States().state_data
    # Sort the list of dictionaries by population in _descending_ order, and store the last 5 entries.
    top_5 = sorted(
        state_data, key=lambda state: int(state["population"]), reverse=True
    )[:5]

    # Store the state names and population values.
    states = [state["state"] for state in top_5]
    populations = [int(state["population"]) for state in top_5]

    # Initialize the graph and define the bars.
    figure, axis = plt.subplots(figsize=(10, 6))
    bars = axis.bar(states, populations, color="green")

    # Set graph title, as well as x- and y-axis labels.
    axis.set_title("Top 5 State Populations")
    axis.set_xlabel("State")
    axis.set_ylabel("Population")

    # Format the y-axis to display commas as thousands separators.
    axis.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    # Rotate the x-axis labels to make them more readable.
    axis.tick_params(axis="x", rotation=45)

    for bar, population in zip(bars, populations):
        axis.text(
            # Center the text horizontally within the bar.
            bar.get_x() + bar.get_width() / 2,
            # Position the label at the top of the bar.
            bar.get_height(),
            # Format the population value with thousands separators.
            f"{population:,}",
            ha="center",
            va="bottom",
        )

    # Use tight_layout to adjust the spacing of the plot elements and prevent overlap.
    plt.tight_layout()
    # Display the graph.
    plt.show()
