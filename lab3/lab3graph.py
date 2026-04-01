"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Function to plot the top 5 states with the highest population.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

try:
    from lab3.lab3states import States
except ImportError as e:
    from lab3states import States


def plot_top_5_state_populations(states: States) -> None:
    """
    This function visualizes the population of the top 5 states with the highest
    population. The data is sorted in descending order based on population,
    and a bar chart is plotted to represent the results. The chart includes
    population values annotated on each bar.

    :return: None
    :rtype: None
    """

    # Sort the list of dictionaries by population in _descending_ order, and
    # store the last 5 entries.
    top_5 = sorted(
        states.state_data, key=lambda state: int(state["population"]), reverse=True
    )[:5]

    # Store the state names and population values.
    top_5_pop_states = [state["state"] for state in top_5]
    populations = [int(state["population"]) for state in top_5]

    # Initialize the graph and define the bars.
    figure, axis = plt.subplots(figsize=(10, 6))
    if not figure:
        raise RuntimeError("Failed to create figure.")
    bars = axis.bar(top_5_pop_states, populations, color="green")

    # Set graph title, as well as x- and y-axis labels.
    axis.set_title("Top 5 State Populations")
    axis.set_xlabel("State")
    axis.set_ylabel("Population")

    # Format the y-axis to display commas as thousands separators.
    axis.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    # Rotate the x-axis labels to make them more readable.
    axis.tick_params(axis="x", rotation=45)

    for bar_line, population in zip(bars, populations):
        axis.text(
            # Center the text horizontally within the bar.
            bar_line.get_x() + bar_line.get_width() / 2,
            # Position the label at the top of the bar.
            bar_line.get_height(),
            # Format the population value with thousands separators.
            f"{population:,}",
            ha="center",
            va="bottom",
        )

    # Use tight_layout to adjust the spacing of the plot elements and prevent overlap.
    plt.tight_layout()
    # Display the graph.
    plt.show()
