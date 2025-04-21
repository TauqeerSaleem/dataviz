from manim import *
from manim.opengl import *
import numpy as np
import math
import pandas as pd
from datetime import datetime
import pandas as pd
from datetime import datetime

class StaticLineGraph(Scene):
    def construct(self):
        # Load and parse CSV
        df = pd.read_csv("BTC_Price_Data.csv")  # 🔁 Replace with your CSV path
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="%d-%b-%y")
        df.sort_values("Datetime", inplace=True)
        
        # Normalize datetime to x values
        x_vals = list(range(len(df)))
        y_vals = list(df["Price"])
        date_labels = [d.strftime("%b %y") for d in df["Datetime"]]

        # Create axes
        max_y = 70000
        axes = Axes(
            x_range = [0, len(x_vals) + 200, (len(x_vals) + 200)/20],
            y_range = [0, 70000*1.1, max_y / 5],
            x_length = 10,
            y_length = 6,
            axis_config = {"include_tip": True},
        ).to_edge(DOWN)

        axes_labels = axes.get_axis_labels(x_label = "Date", y_label = "Price")

        # Optional: Add custom x-axis labels (just a few for readability)
        step_x = max(1, len(date_labels) // 3)  # Adjust number of labels
        x_tick_labels = {
            i: Text(date_labels[i])
            for i in range(0, len(date_labels), step_x)
        }
        axes.get_x_axis().add_labels(x_tick_labels)

        step_y = max_y // 5   # Adjust number of labels
        y_tick_labels = {
            round(i, 0): Text(f"$ {i//1000} k")
            for i in [round(step_y * j, 0) for j in range(6)]
        }
        axes.get_y_axis().add_labels(y_tick_labels)

        # Create and plot line
        points = [axes.c2p(x, y) for x, y in zip(x_vals, y_vals)]
        graph = VGroup(color=GREEN).set_points_as_corners(points)

        self.add(axes, axes_labels)
        
        self.play(Create(graph, run_time = 6))
        self.interactive_embed()

class DynamicGrowingLineGraph(Scene):
    def construct(self):
        
        # Define the dataset
        df = pd.read_csv("BTC_Price_Data.csv")
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="%d-%b-%y")
        df.sort_values("Datetime", inplace=True)
        df.index = df['Datetime']
        df = df[['Price']]
        #df = df.resample('M').mean()

        # Get the x values (in integer form)
        x_vals = list(range(len(df)))

        # Get the y yalues
        y_vals = list(df["Price"])

        # get the labels for x axis (in month-year format)
        date_labels = [d.strftime("%b %y") for d in df.index]

        # Extra length for axis
        # x_buffer will determine how much the updated axes has extra x ticks during animation
        x_buffer = 1
        y_buffer_ratio = 1.1

        # Maximum for the plot (we start with x = 50, which is first 50 days)
        # and its corresponding y values (price of frist 50 days)
        max_x = 35
        max_y = max(y_vals[:max_x]) * y_buffer_ratio

        # Define the initial axes
        axes = Axes(
            x_range = [0, max_x + x_buffer, (max_x + x_buffer) / 10],
            y_range = [0, max_y, max_y / 5],
            x_length = 10,
            y_length = 6,
            axis_config = {"include_tip": True},
        ).to_edge(DOWN)
        axes_labels = axes.get_axis_labels("Date", "Price")

        # Here we define x and y axis labels
        # This basically tells the code to put in 10 x-axis labels
        step_x = len(date_labels) // 10
        x_tick_labels = VGroup(*[
            Text(date_labels[i], font_size=24).scale(0.5).next_to(axes.c2p(i, 0), DOWN)
            for i in range(0, len(date_labels), step_x)
            if i <= max_x + x_buffer
        ])

        # This basically tells the code to put in 5 y-axis labels
        step_y = max_y / 5
        y_tick_labels = VGroup(*[
            Text(f"$ {int(i)}", font_size=24).scale(0.5).next_to(axes.c2p(0, i), LEFT)
            for i in [step_y * j for j in range(6)]
        ])

        # Add the initial axes, axes lables, and axes tick marks
        self.add(axes, axes_labels, x_tick_labels, y_tick_labels)

        # Start the line with first two points
        # Note that it is here importaant to define the VGroup, and then initialize it with two points
        line = VGroup(color = GREEN)
        points = [axes.c2p(x_vals[0], y_vals[0])]
        line.set_points_as_corners(points)

        # Add the line
        self.add(line)

        # Main animation
        # Note that the loop starts from 1 instead of 0, 
        # because the points at 0 have already been added
        for i in range(1, len(x_vals)):
            # Define the next points
            x, y = x_vals[i], y_vals[i]

            # By default no need of rescaling
            needs_rescale = False

            # By default the nex max is the old max
            new_max_x, new_max_y = max_x, max_y

            # Check if we are exceeding the maximum on axes
            # if so, then update the new axes to have more length
            # and flag needs_rescale
            if x > max_x:
                new_max_x = x + x_buffer
                needs_rescale = True
            if y > max_y:
                new_max_y = y * y_buffer_ratio
                needs_rescale = True

            # flaged in the last conditional statement
            if needs_rescale:
                # The new axes will have always 10 x ticks and 5 y ticks
                new_axes = Axes(
                    x_range = [0, new_max_x, new_max_x / 10],
                    y_range = [0, new_max_y, new_max_y / 5],
                    x_length = 10,
                    y_length = 6,
                    axis_config = {"include_tip": True},
                ).to_edge(DOWN)
                new_axes_labels = new_axes.get_axis_labels("Date", "Price")

                new_x_tick_labels = VGroup(*[
                    Text(date_labels[j], font_size=24).scale(0.5).next_to(new_axes.c2p(j, 0), DOWN)
                    for j in range(0, len(date_labels), step_x)
                    if j <= new_max_x
                ])

                new_y_tick_labels = VGroup(*[
                    Text(f"$ {int(j)}", font_size=24).scale(0.5).next_to(new_axes.c2p(0, j), LEFT)
                    for j in [new_max_y / 5 * k for k in range(6)]
                ])

                # Properly handle axes update by fading old axes out and new ones in
                self.play(
                    FadeOut(VGroup(axes, axes_labels, x_tick_labels, y_tick_labels)),
                    FadeIn(VGroup(new_axes, new_axes_labels, new_x_tick_labels, new_y_tick_labels)),
                    run_time=0.0167
                )

                axes, axes_labels = new_axes, new_axes_labels
                x_tick_labels, y_tick_labels = new_x_tick_labels, new_y_tick_labels
                max_x, max_y = new_max_x, new_max_y

                points = [axes.c2p(x_vals[j], y_vals[j]) for j in range(i)]
                line.set_points_as_corners(points)

            new_point = axes.c2p(x, y)
            points.append(new_point)
            line.set_points_as_corners(points)
            self.wait(0.03)

        self.interactive_embed()