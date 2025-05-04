from manim import *
from manim.opengl import *
import pandas as pd


class ElonMusk(Scene):
    def construct(self):

        ## Import BTC price data
        BTC_price_short = pd.read_csv('data/BTC_Price_Data_Short.csv', index_col = 'Datetime')
        # Convert the index to datetime format
        BTC_price_short.index = pd.to_datetime(BTC_price_short.index)
        # Only take in price for 29th January 2021 between time = available in sentiments data
        condition = (BTC_price_short.index > '2021-01-29 05:49:00') & (
                     BTC_price_short.index < '2021-01-29 16:06:00')
        # Sort in ascending
        BTC_price_short = BTC_price_short[condition].sort_index(ascending=True)
        
        ## Import  sentiment data
        sentiments_short = pd.read_csv('data/Sentiment_Data_short.csv', index_col = 'Datetime')
        
        # Caculate the volume per minute
        count_df = sentiments_short[['Negative']].copy()
        count_df.index = pd.to_datetime(count_df.index)
        count_df = count_df.resample('min').count().rename(columns={"Negative": "Count"}).sort_index(ascending=True)

        # x-axis values - Normalize datetime to x values
        x_vals = list(range(len(BTC_price_short)))
        date_labels = [d.strftime("%H:%M") for d in BTC_price_short.index]
        
        ## PRICE
        # y-values (Price)
        y_vals_price = list(BTC_price_short["Price"])

        # Axes
        max_y = max(BTC_price_short['Price'])
        min_y = min(BTC_price_short['Price'])
        axes_price = Axes(
            x_range = [0, len(x_vals) + 10, (len(x_vals) + 10)/20],
            y_range = [min_y*0.95, max_y*1.05, (max_y - min_y) // 5],
            x_length = 10,
            y_length = 6,
            axis_config = {"include_tip": False},
        ).to_edge(DOWN)

        # Custom y-ticks [Price]
        price_step_y = (max_y - min_y) // 5  # Adjust number of labels
        y_tick_labels = {
            round(i, 0): Text(f"$ {int(i//1000)} k")
            for i in [round(min_y + price_step_y * j, 0) for j in range(7)]
        }
        axes_price.get_y_axis().add_labels(y_tick_labels)

        # Create and plot line - PRICE
        points_price_1 = [axes_price.c2p(x, y) for x, y in zip(x_vals[:150], y_vals_price[:150])]
        graph_price_1 = VGroup(color = GREEN).set_points_as_corners(points_price_1)
        points_price_2 = [axes_price.c2p(x, y) for x, y in zip(x_vals[150:], y_vals_price[150:])]
        graph_price_2 = VGroup(color = GREEN).set_points_as_corners(points_price_2)
        
        ## VOLUME
        # y-values for volume
        y_vals_vol = list(count_df["Count"])

        # Scale for common comparison
        vol_min = min(y_vals_vol)
        vol_max = max(y_vals_vol)
        price_min = min(y_vals_price)
        price_max = max(y_vals_price)
        y_vals_vol_normalized = [(v - vol_min) / (vol_max - vol_min) for v in y_vals_vol]
        y_vals_vol = [v * (price_max - price_min) + price_min for v in y_vals_vol_normalized]
        
        # Create and plot line - VOLUME
        points_vol = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_vol)]
        graph_vol = VGroup(color = YELLOW).set_points_as_corners(points_vol)
        graph_vol.set_stroke(opacity=0.3)

        # Add custom x-axis labels (just a few for readability)
        step_x = max(1, len(date_labels) // 3)  # Adjust number of labels
        x_tick_labels = {
            i: Text(date_labels[i])
            for i in range(0, len(date_labels), step_x)
        }
        axes_price.get_x_axis().add_labels(x_tick_labels)

        ## Volume-Axes
        # Manually draw the right-side y-axis (volume)
        max_y = max(count_df['Count'])
        min_y = min(count_df['Count'])
        right_y_axis = NumberLine(
            x_range=[min_y*0.95, max_y*1.05, (max_y - min_y) // 5],
            length=6,
            rotation=90 * DEGREES,
            include_tip = False
        )

        # Move it to the far right of the main axes
        right_y_axis.move_to(axes_price.c2p(len(x_vals)+ 10, max(BTC_price_short['Price'])*0.92))

        # Add labels to right y-axis
        right_labels = right_y_axis.get_tick_range().tolist()
        right_tick_labels = VGroup(*[
            Text(str(int(val)), font_size=24).next_to(right_y_axis.n2p(val), RIGHT, buff=0.1)
            for val in right_labels
        ])
        
        # Axes Labels
        #right_y_label = Text("Volume", font_size=28, italic=True).next_to(right_y_axis, UP)
        #left_y_label = Text("Price", font_size=28, italic=True).next_to(axes_price.get_y_axis(), UP)
        #x_label = Text("Time", font_size=28, italic=True).next_to(axes_price.get_x_axis(), DOWN)
        right_y_label = Text("Volume", font_size=28).next_to(right_y_axis, UP)
        left_y_label = Text("Price", font_size=28).next_to(axes_price.get_y_axis(), UP)
        x_label = Text("Time", font_size=28).next_to(axes_price.get_x_axis(), DOWN)

        # Icons
        # BTC Icon
        #btc_icon = SVGMobject("images/BTC.png").scale(1).set_opacity(0.8)
        btc_icon = SVGMobject("images/BTC.svg").scale(5).set_opacity(0.1)
        btc_icon.to_corner(ORIGIN)  # UR = Upper Right

        # BTC Icon
        #elon_icon = ImageMobject("images/Elon.png").scale(0.125)
        elon_icon = SVGMobject("images/Elon.svg").scale(0.5).set_opacity(0.8)
        elon_icon.move_to(axes_price.c2p(210, min(BTC_price_short['Price'])*1.05))
        elon_text = Text("Elon Musk", font_size = 12).next_to(elon_icon, DOWN*0.50)

        # ANIMATE
        self.add(btc_icon)
        self.play(FadeIn(axes_price, 
                         left_y_label,
                         x_label))
        
        self.play(Create(graph_price_1, 
                         run_time = 3))
        self.wait(0.1)
        self.add(elon_icon, elon_text)
        self.wait(0.1)
        self.play(Create(graph_price_2, 
                         run_time = 3))
        self.play(FadeIn(right_y_axis, 
                         right_y_label,
                         right_tick_labels))
        self.play(Create(graph_vol, 
                         run_time = 6))

        #self.interactive_embed()

class ElonMusk_Sentiments(Scene):
    def construct(self):

        ## Import BTC price data
        BTC_price_short = pd.read_csv('data/BTC_Price_Data_Short.csv', index_col = 'Datetime')
        # Convert the index to datetime format
        BTC_price_short.index = pd.to_datetime(BTC_price_short.index)
        # Only take in price for 29th January 2021 between time = available in sentiments data
        condition = (BTC_price_short.index > '2021-01-29 05:49:00') & (
                     BTC_price_short.index < '2021-01-29 16:06:00')
        # Sort in ascending
        BTC_price_short = BTC_price_short[condition].sort_index(ascending=True)
        
        ## Import  sentiment data
        sentiments_short = pd.read_csv('data/Sentiment_Data_short.csv', index_col = 'Datetime')
        sentiments_short.index = pd.to_datetime(sentiments_short.index)
        sentiments_short = sentiments_short[['Compound']].resample('min').mean().sort_index(ascending=True)
        
        # x-axis values - Normalize datetime to x values
        x_vals = list(range(len(BTC_price_short)))
        date_labels = [d.strftime("%H:%M") for d in BTC_price_short.index]
        
        ## PRICE
        # y-values (Price)
        y_vals_price = list(BTC_price_short["Price"])

        # Axes
        max_y = max(BTC_price_short['Price'])
        min_y = min(BTC_price_short['Price'])
        axes_price = Axes(
            x_range = [0, len(x_vals) + 10, (len(x_vals) + 10)/20],
            y_range = [min_y*0.95, max_y*1.05, (max_y - min_y) // 5],
            x_length = 10,
            y_length = 6,
            axis_config = {"include_tip": False},
        ).to_edge(DOWN)

        # Custom y-ticks [Price]
        price_step_y = (max_y - min_y) // 5  # Adjust number of labels
        y_tick_labels = {
            round(i, 0): Text(f"$ {int(i//1000)} k")
            for i in [round(min_y + price_step_y * j, 0) for j in range(7)]
        }
        axes_price.get_y_axis().add_labels(y_tick_labels)

        # Create and plot line - PRICE
        points_price = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_price)]
        graph_price = VGroup(color = GREEN).set_points_as_corners(points_price)
        
        ## VOLUME
        # y-values for volume
        y_vals_sen = list(sentiments_short["Compound"])

        # Scale for common comparison
        sen_min = -1
        sen_max = 1
        price_min = min(y_vals_price)
        price_max = max(y_vals_price)
        y_vals_sen_normalized = [(v - sen_min) / (sen_max - sen_min) for v in y_vals_sen]
        y_vals_sen = [v * (price_max - price_min) + price_min for v in y_vals_sen_normalized]
        
        # Create and plot line - Sentiments:Compound
        points_sen = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen)]
        graph_sen = VGroup(color = BLUE).set_points_as_corners(points_sen)
        graph_sen.set_stroke(opacity = 0.3)

        # Add custom x-axis labels (just a few for readability)
        step_x = max(1, len(date_labels) // 3)  # Adjust number of labels
        x_tick_labels = {
            i: Text(date_labels[i])
            for i in range(0, len(date_labels), step_x)
        }
        axes_price.get_x_axis().add_labels(x_tick_labels)

        ## Sentiment-Axes
        # Manually draw the right-side y-axis (volume)
        right_y_axis = NumberLine(
            x_range=[sen_min*0.95, sen_max*1.05, 0.25],
            length=6,
            rotation=90 * DEGREES,
            include_tip = False
        )

        # Move it to the far right of the main axes
        right_y_axis.move_to(axes_price.c2p(len(x_vals) + 10, max(BTC_price_short['Price'])*0.92))

        # Add labels to right y-axis
        right_labels = right_y_axis.get_tick_range().tolist()
        right_tick_labels = VGroup(*[
            Text(f"{val:+.2f}", font_size=24).next_to(right_y_axis.n2p(val), RIGHT, buff=0.4)
            for val in right_labels
        ])

        # RESCALING
        new_sen_min = 0.05
        new_sen_max = 0.2
        new_right_y_axis = NumberLine(
            x_range=[new_sen_min, new_sen_max, 0.05],
            length=6,
            rotation=90 * DEGREES,
            include_tip=False
        )
        new_right_y_axis.move_to(axes_price.c2p(len(x_vals)+10, max(BTC_price_short['Price'])*0.92))

        # Rescale sentiment values
        y_vals_sen_ = list(sentiments_short["Compound"])
        y_vals_sen_normalized_zoomed = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_]
        y_vals_sen_zoomed = [v * (price_max - price_min) + price_min for v in y_vals_sen_normalized_zoomed]

        # Recreate the sentiment line
        points_sen_zoomed = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_zoomed)]
        graph_sen_zoomed = VGroup(color=BLUE).set_points_as_corners(points_sen_zoomed).set_stroke(opacity=0.7)

        # Tick labels for new axis
        new_right_tick_labels = VGroup(*[
            Text(f"{val:+.2f}", font_size=24).next_to(new_right_y_axis.n2p(val), RIGHT, buff=0.1)
            for val in new_right_y_axis.get_tick_range().tolist()
        ])

        y_vals_sen_ma = list(sentiments_short['Compound'].rolling(window = 30, min_periods = 1).mean())

        # Rescale to y-axis using new_sen_min / new_sen_max
        y_vals_sen_ma_normalized = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_ma]
        y_vals_sen_ma_scaled = [v * (price_max - price_min) + price_min for v in y_vals_sen_ma_normalized]

        # Plot line
        points_sen_ma = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_ma_scaled)]
        graph_sen_ma = VGroup(color = BLUE).set_points_as_corners(points_sen_ma).set_stroke(opacity=0.5)

        # Axes Labels
        right_y_label = Text("Sentiments", font_size=28).next_to(right_y_axis, UP)
        left_y_label = Text("Price", font_size=28).next_to(axes_price.get_y_axis(), UP)
        x_label = Text("Time", font_size=28).next_to(axes_price.get_x_axis(), DOWN)

        # BTC Icon
        btc_icon = SVGMobject("images/BTC.svg").scale(5).set_opacity(0.1)
        btc_icon.to_corner(ORIGIN)  # UR = Upper Right

        # ANIMATE
        self.add(btc_icon,
                 axes_price,
                 left_y_label,
                 x_label,
                 graph_price)
        
        self.play(FadeIn(right_y_axis, 
                         right_y_label,
                         right_tick_labels))
        self.play(Create(graph_sen, 
                         run_time = 6))
        self.play(
            FadeOut(right_y_axis),
            FadeOut(right_tick_labels),
            FadeIn(new_right_y_axis),
            FadeIn(new_right_tick_labels),
            Transform(graph_sen, graph_sen_zoomed),
            run_time = 1
            )
        self.wait(0.05)
        self.play(
            Transform(graph_sen_zoomed, graph_sen_ma),
            FadeOut(graph_sen),
            run_time = 1
            )
        self.interactive_embed()

class ElonMusk_Sentiments_(Scene):
    def construct(self):

        ## Import BTC price data
        BTC_price_short = pd.read_csv('data/BTC_Price_Data_Short.csv', index_col = 'Datetime')
        # Convert the index to datetime format
        BTC_price_short.index = pd.to_datetime(BTC_price_short.index)
        # Only take in price for 29th January 2021 between time = available in sentiments data
        condition = (BTC_price_short.index > '2021-01-29 05:49:00') & (
                     BTC_price_short.index < '2021-01-29 16:06:00')
        # Sort in ascending
        BTC_price_short = BTC_price_short[condition].sort_index(ascending=True)
        
        ## Import  sentiment data
        sentiments_short = pd.read_csv('data/Sentiment_Data_short.csv', index_col = 'Datetime')
        sentiments_short.index = pd.to_datetime(sentiments_short.index)
        sentiments_short = sentiments_short[['Compound']].resample('min').mean().sort_index(ascending=True)
        
        # x-axis values - Normalize datetime to x values
        x_vals = list(range(len(BTC_price_short)))
        date_labels = [d.strftime("%H:%M") for d in BTC_price_short.index]
        
        ## PRICE
        # y-values (Price)
        y_vals_price = list(BTC_price_short["Price"])

        # Axes
        max_y = max(BTC_price_short['Price'])
        min_y = min(BTC_price_short['Price'])
        axes_price = Axes(
            x_range = [0, len(x_vals) + 10, (len(x_vals) + 10)/20],
            y_range = [min_y*0.95, max_y*1.05, (max_y - min_y) // 5],
            x_length = 10,
            y_length = 6,
            axis_config = {"include_tip": False},
        ).to_edge(DOWN)

        # Custom y-ticks [Price]
        price_step_y = (max_y - min_y) // 5  # Adjust number of labels
        y_tick_labels = {
            round(i, 0): Text(f"$ {int(i//1000)} k")
            for i in [round(min_y + price_step_y * j, 0) for j in range(7)]
        }
        axes_price.get_y_axis().add_labels(y_tick_labels)

        # Create and plot line - PRICE
        points_price = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_price)]
        graph_price = VGroup(color = GREEN).set_points_as_corners(points_price)
        
        ## VOLUME
        # y-values for volume
        y_vals_sen = list(sentiments_short["Compound"])

        # Scale for common comparison
        sen_min = -1
        sen_max = 1
        price_min = min(y_vals_price)
        price_max = max(y_vals_price)
        y_vals_sen_normalized = [(v - sen_min) / (sen_max - sen_min) for v in y_vals_sen]
        y_vals_sen = [v * (price_max - price_min) + price_min for v in y_vals_sen_normalized]
        
        # Create and plot line - Sentiments:Compound
        points_sen = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen)]
        graph_sen = VGroup(color = BLUE).set_points_as_corners(points_sen)
        graph_sen.set_stroke(opacity = 0.3)

        # Add custom x-axis labels (just a few for readability)
        step_x = max(1, len(date_labels) // 3)  # Adjust number of labels
        x_tick_labels = {
            i: Text(date_labels[i])
            for i in range(0, len(date_labels), step_x)
        }
        axes_price.get_x_axis().add_labels(x_tick_labels)

        ## Sentiment-Axes
        # Manually draw the right-side y-axis (volume)
        right_y_axis = NumberLine(
            x_range=[sen_min*0.95, sen_max*1.05, 0.25],
            length=6,
            rotation=90 * DEGREES,
            include_tip = False
        )

        # Move it to the far right of the main axes
        right_y_axis.move_to(axes_price.c2p(len(x_vals) + 10, max(BTC_price_short['Price'])*0.92))

        # Add labels to right y-axis
        right_labels = right_y_axis.get_tick_range().tolist()
        right_tick_labels = VGroup(*[
            Text(f"{val:+.2f}", font_size=24).next_to(right_y_axis.n2p(val), RIGHT, buff=0.4)
            for val in right_labels
        ])

        # RESCALING
        new_sen_min = 0.05
        new_sen_max = 0.2
        new_right_y_axis = NumberLine(
            x_range=[new_sen_min, new_sen_max, 0.05],
            length=6,
            rotation=90 * DEGREES,
            include_tip=False
        )
        new_right_y_axis.move_to(axes_price.c2p(len(x_vals)+10, max(BTC_price_short['Price'])*0.92))

        # Rescale sentiment values
        y_vals_sen_ = list(sentiments_short["Compound"])
        y_vals_sen_normalized_zoomed = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_]
        y_vals_sen_zoomed = [v * (price_max - price_min) + price_min for v in y_vals_sen_normalized_zoomed]

        # Recreate the sentiment line
        points_sen_zoomed = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_zoomed)]
        graph_sen_zoomed = VGroup(color=BLUE).set_points_as_corners(points_sen_zoomed).set_stroke(opacity=0.7)

        # Tick labels for new axis
        new_right_tick_labels = VGroup(*[
            Text(f"{val:+.2f}", font_size=24).next_to(new_right_y_axis.n2p(val), RIGHT, buff=0.1)
            for val in new_right_y_axis.get_tick_range().tolist()
        ])

        y_vals_sen_ma = list(sentiments_short['Compound'].rolling(window = 30, min_periods = 1).mean())

        # Rescale to y-axis using new_sen_min / new_sen_max
        y_vals_sen_ma_normalized = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_ma]
        y_vals_sen_ma_scaled = [v * (price_max - price_min) + price_min for v in y_vals_sen_ma_normalized]

        # Plot line
        points_sen_ma = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_ma_scaled)]
        graph_sen_ma = VGroup(color = BLUE).set_points_as_corners(points_sen_ma).set_stroke(opacity=0.5)

        # Compute rolling standard deviation
        y_vals_sen_std = list(sentiments_short['Compound'].rolling(window=30, min_periods=1).std().fillna(0))

        # Compute upper and lower bounds (mean ± std), rescaled
        y_vals_sen_std_upper = [m + s for m, s in zip(y_vals_sen_ma, y_vals_sen_std)]
        y_vals_sen_std_lower = [m - s for m, s in zip(y_vals_sen_ma, y_vals_sen_std)]

        # Normalize
        y_vals_sen_std_upper_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_std_upper]
        y_vals_sen_std_lower_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_sen_std_lower]

        # Scale to plot height
        y_vals_sen_std_upper_scaled = [v * (price_max - price_min) + price_min for v in y_vals_sen_std_upper_norm]
        y_vals_sen_std_lower_scaled = [v * (price_max - price_min) + price_min for v in y_vals_sen_std_lower_norm]

        # Get points
        points_upper = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_std_upper_scaled)]
        points_lower = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_sen_std_lower_scaled)]

        # Combine points for polygon: upper -> reversed lower
        shaded_region = Polygon(
            *points_upper,
            *reversed(points_lower),
            fill_opacity=0.1,
            stroke_width=0,
            color=BLUE
        )

        # Axes Labels
        right_y_label = Text("Sentiments", font_size=28).next_to(right_y_axis, UP)
        left_y_label = Text("Price", font_size=28).next_to(axes_price.get_y_axis(), UP)
        x_label = Text("Time", font_size=28).next_to(axes_price.get_x_axis(), DOWN)

        # BTC Icon
        btc_icon = SVGMobject("images/BTC.svg").scale(5).set_opacity(0.1)
        btc_icon.to_corner(ORIGIN)  # UR = Upper Right

        # ANIMATE
        self.add(btc_icon,
                 axes_price,
                 left_y_label,
                 x_label,
                 graph_price)
        
        self.play(FadeIn(right_y_axis, 
                         right_y_label,
                         right_tick_labels))
        self.play(Create(graph_sen, 
                         run_time = 6))
        self.play(
            FadeOut(right_y_axis),
            FadeOut(right_tick_labels),
            FadeIn(new_right_y_axis),
            FadeIn(new_right_tick_labels),
            Transform(graph_sen, graph_sen_zoomed),
            run_time = 1
            )
        self.wait(0.05)
        self.play(
            Transform(graph_sen_zoomed, graph_sen_ma),
            FadeOut(graph_sen),
            FadeIn(shaded_region),
            run_time = 1
            )
        self.interactive_embed()

class ElonMusk_Sentiments_WordCloud(Scene):
    def construct(self):

        from wordcloud import STOPWORDS
        from wordcloud import WordCloud
        from collections import Counter
        import re

        #tweets = pd.read_csv('data\Cleaned_Tweets_short.csv')
        # Sample text
        text = """
        Elon Musk tweeted about Bitcoin. Bitcoin price fluctuated after Elon Musk’s tweets.
        Cryptocurrency is volatile. Elon Musk influences the crypto market.
        """

        # Clean text
        text = re.sub(r"[^\w\s]", "", text)

        # Tokenize and remove stopwords
        words = [word for word in text.split() if word not in STOPWORDS]

        # Count word frequencies
        word_counts = Counter(words)

        # Step 2: Generate word cloud layout (not image)
        wc = WordCloud(
            width = 1400, #1920,
            height = int(1400/1.7777777777777777), #1080,
            stopwords = STOPWORDS,
            colormap='viridis'
            ).generate(text)
        #wc.generate_from_frequencies(word_counts)

        # Step 3: Extract layout info
        layout = wc.layout_  # (word, font_size, position, orientation, color)
        print(layout)
        # 6. Place words
        word_mobs = []
        word_pos_x = []
        word_pos_y = []

        for ((word_str, scale), font_size, pos, orientation, color) in layout:
            # parse color if in rgb(...) string
            if isinstance(color, str) and color.startswith("rgb"):
                r, g, b = map(int, re.findall(r'\d+', color))
                color = rgb_to_color((r, g, b))

            word = Text(word_str, 
                        font_size = font_size*scale, 
                        color = color)

            if orientation == None or orientation == 0:
                pass
            else:
                word.rotate(PI / 2)
            
            word_pos_x.append(pos[1])
            word_pos_y.append(pos[0])
            word_mobs.append(word)
          
        x_max, x_min, y_max, y_min = max(word_pos_x), min(word_pos_y), max(word_pos_y), min(word_pos_y)
        
        x_ = [(v - x_min) / (x_max - x_min) for v in word_pos_x]
        x = [(v * 14) - 7 for v in x_]
        
        y_ = [(v - y_min) / (y_max - y_min) for v in word_pos_y]
        y = [(v * 8) - 4 for v in y_]
        
        for i, word in enumerate(word_mobs):
            word.move_to([x[i], y[i], 0], aligned_edge=DL)

        # 7. Animate all in
        self.play(*[FadeIn(word) for word in word_mobs], run_time=3)
        
        self.interactive_embed()

class ElonMusk_Sentiments_WordCloud_(Scene):
    def construct(self):

        from wordcloud import STOPWORDS
        from collections import Counter
        import re

        STOPWORDS.add('bitcoin')
        STOPWORDS.add('btc')
        STOPWORDS.add('eth')
        STOPWORDS.add('doge')
        STOPWORDS.add('dogecoin')
        STOPWORDS.add('crypto')
        STOPWORDS.add('cryptocurrency')
        STOPWORDS.add('-')
        STOPWORDS.add('_')
        STOPWORDS.add('1')
        STOPWORDS.add('5')
        STOPWORDS.add('will')
        STOPWORDS.add('ftm')


        tweets = pd.read_csv('data/Cleaned_Tweets_short.csv')
        tweets['Datetime'] = pd.to_datetime(tweets['Datetime'])
        tweets.set_index('Datetime', inplace = True)
        grouped = tweets.resample('30min')['Text'].apply(lambda texts: ' '.join(texts)).reset_index().sort_index(ascending=True)
        ind = list(grouped.index)
        texts = list(grouped.Text)

        text = texts[0]
        text = re.sub(r"[^\w\s]", "", text.lower())
        words = [w for w in text.split() if w not in STOPWORDS]
        word_counts = Counter(words)
        top_words = word_counts.most_common(5)
        #print(top_words)
        text_lines = [Text(f'{word[0]}', font_size=36) for word in top_words]
        word_list = VGroup(*text_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        for word in word_list:
            self.play(FadeIn(word), run_time = 0.2)

        for i in range(1, 5):
            text = texts[i]
            text = re.sub(r"[^\w\s]", "", text.lower())
            words = [w for w in text.split() if w not in STOPWORDS]
            word_counts = Counter(words)
            top_words = word_counts.most_common(5)
            text_lines = [Text(f'{word[0]}', font_size=36) for word in top_words]
            word_list_ = VGroup(*text_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

            # Step 5: Add a surrounding rectangle
            #box = SurroundingRectangle(word_list, color=WHITE, buff=0.4)
            
            for i in range(5):
                self.play(FadeOut(word_list[i]),
                          FadeIn(word_list_[i]), 
                          run_time = 0.2
                          )
            word_list = word_list_
                    
        self.interactive_embed()