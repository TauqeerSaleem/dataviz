from manim import *
from manim.opengl import *
import pandas as pd

class Intro(Scene):
    def construct(self):
        # Create both texts
        text = Text("Behavioral Economics\nMarketing")

        # Arrange vertically
        #text.move_to(ORIGIN)

        text.align_on_border(UP)  # optional
        text.center()             # <--- THIS centers it horizontally and vertically 

        # Create a rectangle around the group
        box = SurroundingRectangle(text, color=WHITE, buff=0.5)

        # Fade in the texts
        self.play(FadeIn(text),
                  Create(box)
                  )
        
        #self.interactive_embed()

class Second(Scene):
    def construct(self):
        # grid = NumberPlane(
        #     x_range=[-8, 8, 1],  # X-axis from -8 to 8 with 1 unit steps
        #     y_range=[-5, 5, 1],  # Y-axis from -5 to 5 with 1 unit steps
        #     background_line_style={
        #         "stroke_color": BLUE_D,
        #         "stroke_width": 1,
        #         "stroke_opacity": 0.5
        #     }
        # )
        # self.add(grid)

        title = Title("Behavioral Economics - Prospect Theory")
        pic = ImageMobject("images/pic.webp").scale(0.5)

        pic.move_to(ORIGIN - (0, 0.5, 0))
        text = Text("Amos Tversk & Daniel Kahneman", font_size = 18).next_to(pic, DOWN*0.50)

        t1 = Text("Reference dependence",
                  font_size = 32).move_to((3, 1.75-0.0, 0))
        t2 = Text("Loss aversion",
                  font_size = 32).move_to((3, 1.75-1.5, 0))
        t3 = Text("Risk aversion",
                  font_size = 32).move_to((3, 1.75-3.0, 0))
        t4 = Text("Probability weighting",
                  font_size = 32).move_to((3, 1.75-4.5, 0))
        
        t5 = Text("People evaluate potential gains/ losses relative to a reference",
                  font_size = 32).move_to((-6, 1.75-0.75, 0), aligned_edge = LEFT)
        
        t6 = Text("Losses hurt more than gains feel good",
                  font_size = 32).move_to((-6, 1.75-3.75, 0), aligned_edge = LEFT)

        self.add(title)
        self.play(
            FadeIn(pic),
            FadeIn(text)
            )
        self.play(
            pic.animate.move_to(pic.get_center() + LEFT * 4),
            text.animate.move_to(text.get_center() + LEFT * 4)
            )
        
        self.play(Write(t1))
        self.play(Write(t2))
        self.play(Write(t3))
        self.play(Write(t4))

        self.play(FadeOut(t3),
                  FadeOut(t4),
                  FadeOut(pic),
                  FadeOut(text),
                  t1.animate.set_color(BLUE).move_to((-6, 1.75-0.0, 0), aligned_edge = LEFT),
                  t2.animate.set_color(BLUE).move_to((-6, 1.75-3.0, 0), aligned_edge = LEFT)
                  )
        self.play(Write(t5))
        self.play(Write(t6))

        #self.interactive_embed()

class Third(Scene):
    def construct(self):
        # grid = NumberPlane(
        #     x_range=[-8, 8, 1],  # X-axis from -8 to 8 with 1 unit steps
        #     y_range=[-5, 5, 1],  # Y-axis from -5 to 5 with 1 unit steps
        #     background_line_style={
        #         "stroke_color": BLUE_D,
        #         "stroke_width": 1,
        #         "stroke_opacity": 0.5
        #     }
        # )
        # self.add(grid)

        title = Title("Loss Aversion in Sentiments")
        
        happy = ImageMobject("images/happy_chipmunk.png").scale(0.7)
        happy.move_to((-3,0,0))
        happy_emoji_1 = ImageMobject("images/happy_emoji.png").scale(0.1).next_to(happy, DOWN)
        happy_emoji_2 = ImageMobject("images/happy_emoji.png").scale(0.1).next_to(happy_emoji_1, RIGHT)
        happy_emoji_3 = ImageMobject("images/happy_emoji.png").scale(0.1).next_to(happy_emoji_1, LEFT)

        sad = ImageMobject("images/sad_chipmunk.png").scale(0.7)
        sad.move_to((3,0,0))
        sad_emoji_1 = ImageMobject("images/sad_emoji.png").scale(0.1).next_to(sad, DOWN)
        sad_emoji_2 = ImageMobject("images/sad_emoji.png").scale(0.1).next_to(sad_emoji_1, RIGHT)
        sad_emoji_3 = ImageMobject("images/sad_emoji.png").scale(0.1).next_to(sad_emoji_1, LEFT)
        sad_emoji_4 = ImageMobject("images/sad_emoji.png").scale(0.1).next_to(sad_emoji_2, RIGHT)
        sad_emoji_5 = ImageMobject("images/sad_emoji.png").scale(0.1).next_to(sad_emoji_3, LEFT)


        self.add(title)
        
        self.play(FadeIn(happy))
        self.play(FadeIn(sad))
        
        self.play(FadeIn(happy_emoji_3))
        self.play(FadeIn(happy_emoji_1))
        self.play(FadeIn(happy_emoji_2))

        self.play(FadeIn(sad_emoji_5))
        self.play(FadeIn(sad_emoji_3))
        self.play(FadeIn(sad_emoji_1))
        self.play(FadeIn(sad_emoji_2))
        self.play(FadeIn(sad_emoji_4))

        # Animate: scale up slightly and then back to normal
        self.play(
            sad_emoji_5.animate.scale(1.1),
            sad_emoji_4.animate.scale(1.1),
            sad_emoji_3.animate.scale(1.1),
            sad_emoji_2.animate.scale(1.1),
            sad_emoji_1.animate.scale(1.1),  # Scale up to 110%
            run_time=0.5
        )
        self.wait(0.2)
        self.play(
            sad_emoji_5.animate.scale(1/1.1),
            sad_emoji_4.animate.scale(1/1.1),
            sad_emoji_3.animate.scale(1/1.1),
            sad_emoji_2.animate.scale(1/1.1),
            sad_emoji_1.animate.scale(1/1.1),  # Scale back to original size
            run_time=0.5
        )

        #self.interactive_embed()

class Forth(Scene):
    def construct(self):
        import random

        title = Title("Loss Aversion in Sentiments")

        def generate_trending_list(length, drift, randomness, start = 50):
            numbers = [start]
            for _ in range(length - 1):
                change = random.uniform(-randomness, randomness) + drift
                numbers.append(numbers[-1] + change)
            return numbers

        # Get the x values (in integer form)
        x_len = 100
        x_vals = list(range(x_len))

        # Get the y yalues
        # y_vals_1 = generate_trending_list(length = x_len, 
        #                                   drift = 0.3, 
        #                                   randomness = 5)
        # y_vals_2 = generate_trending_list(length = x_len, 
        #                                   drift = -0.3, 
        #                                   randomness = 5)

        y_vals_1 = [
            50,
            49.351028694393314,
            52.88429592531506,
            49.12101230971053,
            51.082741296054316,
            47.439131791259264,
            43.67274292786832,
            46.88323837281365,
            43.046078279420016,
            44.10452510629322,
            39.584538521297596,
            41.05594375169451,
            39.57295482655539,
            37.93216696027774,
            34.647657059411564,
            37.67528926419441,
            39.56383518172986,
            42.06524110364719,
            46.13499457552716,
            47.54943256159699,
            45.124482788054316,
            41.004007543610655,
            43.696380098248525,
            46.25510280677072,
            44.20202772618344,
            43.68037816472402,
            46.755205223784365,
            42.55164579962322,
            43.07338627200921,
            47.30417984323234,
            48.319357194993906,
            53.25259814177445,
            58.21224991461262,
            61.8362161660051,
            57.1884342797906,
            62.05636271475425,
            65.82881081164281,
            66.85576661268821,
            68.36800189124087,
            72.85576618353387,
            70.44684687872345,
            66.54389645785756,
            66.97898914424887,
            68.14975600463048,
            67.76575050321482,
            69.64496004629498,
            71.1852195581806,
            68.63689164296666,
            69.72589423533779,
            74.3416521173702,
            79.30551162405195,
            74.86178259081495,
            78.5976714894477,
            74.64219069586083,
            74.13635718470117,
            74.54271127585146,
            73.03817156660881,
            72.92494035218672,
            69.43183653181799,
            70.02227629187892,
            75.13492979975405,
            78.75061354347447,
            83.38301081365596,
            80.49380587182573,
            79.1906387624172,
            80.33268277172509,
            85.13934569941897,
            83.24304869943163,
            82.03211933339455,
            84.81242484399247,
            81.07516111067108,
            79.46492809464023,
            84.71984997809508,
            86.1007431133522,
            82.47546901843693,
            82.34147667593156,
            83.045367239573,
            79.81313648694531,
            78.91769539113938,
            74.53101409903111,
            79.37631428854715,
            76.8095913731604,
            79.30137685357359,
            76.25019334730747,
            78.96058502132176,
            83.83539314835919,
            87.04074830664652,
            89.564982355934,
            92.36441429022254,
            87.82670723653715,
            90.26232046574874,
            93.18985952459602,
            93.15377425322939,
            88.8107797357338,
            90.4121538235793,
            89.54767215425072,
            89.42691154840625,
            86.85414339518965,
            86.00491299216532,
            82.18999284625455
        ]

        y_vals_2 = [
           50,
            47.78869907547862,
            46.21346622709709,
            46.90285371336892,
            49.616432913423345,
            52.22633554692976,
            49.712254480013364,
            48.57547412626643,
            45.43929143047254,
            43.13426561096315,
            42.93387996504382,
            41.31390794210732,
            37.52870194177519,
            36.914115424142196,
            38.64843617682537,
            41.09300003470602,
            38.39935631322422,
            43.032502041373,
            41.33326813269297,
            38.298514300144646,
            38.88116928338665,
            42.052202106417774,
            36.98794475976004,
            41.66876352699954,
            44.57871425396486,
            40.608813671472596,
            39.6642717394008,
            35.56755909422951,
            31.67434965564296,
            32.17467866433607,
            31.079867275036502,
            26.865830954223576,
            31.048687237366547,
            32.99687948779046,
            28.59342043128553,
            26.768013503123655,
            25.65708841441835,
            25.145764893343458,
            26.98938901190008,
            22.58645209248465,
            26.59714662570175,
            30.92162308433816,
            32.36301769217019,
            34.47393766478618,
            31.44746747053538,
            33.85439596344436,
            33.852241487782265,
            37.44615320499218,
            38.66598104289974,
            35.63258512939815,
            39.30839356607497,
            37.505442087234684,
            32.24154946517499,
            35.35741131482974,
            36.29077306693335,
            37.492016150714846,
            39.68285307128587,
            40.61044626429868,
            37.01489758684753,
            38.598054011085175,
            40.172897934145055,
            38.60884961904856,
            37.36754126955414,
            39.27594547231414,
            41.6078138374614,
            39.68789672766966,
            41.83833631415506,
            43.834281093507116,
            39.40712362656754,
            39.569904007890884,
            36.9645461099615,
            41.159527788188086,
            37.94151103433606,
            36.66117343311789,
            37.56385747541243,
            41.65283156881683,
            42.64061701580121,
            42.335613514782686,
            42.96238420767662,
            44.60487187161297,
            43.52565141668111,
            40.92229616693767,
            40.97135049012151,
            43.08056569712717,
            46.51680056537395,
            48.47693139820461,
            47.71897353300158,
            45.17081462331686,
            48.58082581880608,
            46.1989158235668,
            43.052256715978444,
            39.885237408512175,
            36.578755202344674,
            31.684747458684,
            32.332691727115915,
            33.120254052391864,
            34.97052004083363,
            36.48028964130052,
            31.486486440085866,
            29.56747995921141 
        ]

        sen_1 = 10*np.log(np.arange(1, x_len))
        sen_2 = 2*sen_1

        # Create axes
        axes_1 = Axes(
            x_range = [0, 101, 101/20],
            y_range = [0, 151, 301/20],
            x_length = 4,
            y_length = 4,
            axis_config = {"include_tip": False},
        ).to_edge(DOWN)
        axes_1.move_to((-3,0,0))
        axes_labels_1 = axes_1.get_axis_labels(x_label = "Date", y_label = "Price")
        
        axes_2 = Axes(
            x_range = [0, 101, 101/20],
            y_range = [0, 151, 301/20],
            x_length = 4,
            y_length = 4,
            axis_config = {"include_tip": False},
        ).to_edge(DOWN)
        axes_2.move_to((3,0,0))
        axes_labels_2 = axes_2.get_axis_labels(x_label = "Date", y_label = "Price")
        
        # Create and plot line
        points_1 = [axes_1.c2p(x, y) for x, y in zip(x_vals, y_vals_1)]
        graph_1 = VGroup(color=GREEN).set_points_as_corners(points_1)

        points_2 = [axes_2.c2p(x, y) for x, y in zip(x_vals, y_vals_2)]
        graph_2 = VGroup(color=GREEN).set_points_as_corners(points_2)

        points_3 = [axes_1.c2p(x, y) for x, y in zip(x_vals, sen_1)]
        graph_3 = VGroup(color=BLUE).set_points_as_corners(points_3)
        
        points_4 = [axes_2.c2p(x, y) for x, y in zip(x_vals, sen_2)]
        graph_4 = VGroup(color=RED).set_points_as_corners(points_4)

        # Animations
        self.add(title)

        self.add(axes_1, axes_labels_1)
        self.add(axes_2, axes_labels_2)
        
        self.play(
            Create(graph_1, run_time = 6),
            Create(graph_2, run_time = 6)
            )
        
        self.play(
            Create(graph_3, run_time = 6)
            )
        
        self.play(
            Create(graph_4, run_time = 6)
            )

        self.interactive_embed()

class Loss_Aversion(Scene):
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
        sentiments_short = sentiments_short.resample('min').mean().sort_index(ascending=True)
        
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
        
        ## Setiments / Proportions
        # y-values for volume
        y_vals_pos = list(sentiments_short["Postive"])
        y_vals_neg = list(sentiments_short["Negative"])

        # Scale for common comparison
        sen_min = 0
        sen_max = 1
        price_min = min(y_vals_price)
        price_max = max(y_vals_price)

        y_vals_pos_normalized = [(v - sen_min) / (sen_max - sen_min) for v in y_vals_pos]
        y_vals_pos = [v * (price_max - price_min) + price_min for v in y_vals_pos_normalized]

        y_vals_neg_normalized = [(v - sen_min) / (sen_max - sen_min) for v in y_vals_neg]
        y_vals_neg = [v * (price_max - price_min) + price_min for v in y_vals_neg_normalized]
        
        # Create and plot line - Sentiments/ Proportions
        points_pos = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_pos)]
        graph_pos = VGroup(color = BLUE).set_points_as_corners(points_pos)
        graph_pos.set_stroke(opacity = 0.3)

        points_neg = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_neg)]
        graph_neg = VGroup(color = RED).set_points_as_corners(points_neg)
        graph_neg.set_stroke(opacity = 0.3)

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
            x_range=[0, 1.05, 0.25],
            length=6,
            rotation=90 * DEGREES,
            include_tip = False
        )

        # Move it to the far right of the main axes
        right_y_axis.move_to(axes_price.c2p(len(x_vals) + 10, max(BTC_price_short['Price'])*0.92))

        # Add labels to right y-axis
        right_labels = right_y_axis.get_tick_range().tolist()
        right_tick_labels = VGroup(*[
            Text(f"{val:.2f}", font_size=24).next_to(right_y_axis.n2p(val), RIGHT, buff=0.4)
            for val in right_labels
        ])

        # RESCALING
        new_sen_min = 0
        new_sen_max = 0.15
        new_right_y_axis = NumberLine(
            x_range=[new_sen_min, new_sen_max, 0.02],
            length=6,
            rotation=90 * DEGREES,
            include_tip=False
        )
        new_right_y_axis.move_to(axes_price.c2p(len(x_vals)+10, max(BTC_price_short['Price'])*0.92))

        # Rescale sentiment values
        y_vals_pos_ = list(sentiments_short["Postive"])
        y_vals_pos_normalized_zoomed = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_pos_]
        y_vals_pos_zoomed = [v * (price_max - price_min) + price_min for v in y_vals_pos_normalized_zoomed]

        y_vals_neg_ = list(sentiments_short["Negative"])
        y_vals_neg_normalized_zoomed = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_neg_]
        y_vals_neg_zoomed = [v * (price_max - price_min) + price_min for v in y_vals_neg_normalized_zoomed]

        # Recreate the sentiment line
        points_pos_zoomed = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_pos_zoomed)]
        graph_pos_zoomed = VGroup(color=BLUE).set_points_as_corners(points_pos_zoomed).set_stroke(opacity=0.7)

        points_neg_zoomed = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_neg_zoomed)]
        graph_neg_zoomed = VGroup(color=RED).set_points_as_corners(points_neg_zoomed).set_stroke(opacity=0.7)

        # Tick labels for new axis
        new_right_tick_labels = VGroup(*[
            Text(f"{val:.2f}", font_size=24).next_to(new_right_y_axis.n2p(val), RIGHT, buff=0.1)
            for val in new_right_y_axis.get_tick_range().tolist()
        ])

        y_vals_pos_ma = list(sentiments_short['Postive'].rolling(window = 30, min_periods = 1).mean())
        y_vals_neg_ma = list(sentiments_short['Negative'].rolling(window = 30, min_periods = 1).mean())

        # Rescale to y-axis using new_sen_min / new_sen_max
        y_vals_pos_ma_normalized = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_pos_ma]
        y_vals_pos_ma_scaled = [v * (price_max - price_min) + price_min for v in y_vals_pos_ma_normalized]

        y_vals_neg_ma_normalized = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_neg_ma]
        y_vals_neg_ma_scaled = [v * (price_max - price_min) + price_min for v in y_vals_neg_ma_normalized]

        # Plot line
        points_pos_ma = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_pos_ma_scaled)]
        graph_pos_ma = VGroup(color = BLUE).set_points_as_corners(points_pos_ma).set_stroke(opacity=0.5)

        points_neg_ma = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_neg_ma_scaled)]
        graph_neg_ma = VGroup(color = RED).set_points_as_corners(points_neg_ma).set_stroke(opacity=0.5)

        # # Compute rolling standard deviation
        # y_vals_pos_std = list(sentiments_short['Postive'].rolling(window=30, min_periods=1).std().fillna(0))
        # y_vals_neg_std = list(sentiments_short['Negative'].rolling(window=30, min_periods=1).std().fillna(0))

        # # Compute upper and lower bounds (mean ± std), rescaled
        # y_vals_pos_std_upper = [m + s for m, s in zip(y_vals_pos_ma, y_vals_pos_std)]
        # y_vals_pos_std_lower = [m - s for m, s in zip(y_vals_pos_ma, y_vals_pos_std)]

        # y_vals_neg_std_upper = [m + s for m, s in zip(y_vals_neg_ma, y_vals_neg_std)]
        # y_vals_neg_std_lower = [m - s for m, s in zip(y_vals_neg_ma, y_vals_neg_std)]

        # # Normalize
        # y_vals_pos_std_upper_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_pos_std_upper]
        # y_vals_pos_std_lower_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_pos_std_lower]

        # y_vals_neg_std_upper_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_neg_std_upper]
        # y_vals_neg_std_lower_norm = [(v - new_sen_min) / (new_sen_max - new_sen_min) for v in y_vals_neg_std_lower]

        # # Scale to plot height
        # y_vals_pos_std_upper_scaled = [v * (price_max - price_min) + price_min for v in y_vals_pos_std_upper_norm]
        # y_vals_pos_std_lower_scaled = [v * (price_max - price_min) + price_min for v in y_vals_pos_std_lower_norm]

        # y_vals_neg_std_upper_scaled = [v * (price_max - price_min) + price_min for v in y_vals_neg_std_upper_norm]
        # y_vals_neg_std_lower_scaled = [v * (price_max - price_min) + price_min for v in y_vals_neg_std_lower_norm]

        # # Get points
        # points_upper_pos = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_pos_std_upper_scaled)]
        # points_lower_pos = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_pos_std_lower_scaled)]

        # points_upper_neg = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_neg_std_upper_scaled)]
        # points_lower_neg = [axes_price.c2p(x, y) for x, y in zip(x_vals, y_vals_neg_std_lower_scaled)]

        # # Combine points for polygon: upper -> reversed lower
        # shaded_region_pos = Polygon(
        #     *points_upper_pos,
        #     *reversed(points_lower_pos),
        #     fill_opacity=0.1,
        #     stroke_width=0,
        #     color=BLUE
        # )

        # shaded_region_neg = Polygon(
        #     *points_upper_neg,
        #     *reversed(points_lower_neg),
        #     fill_opacity=0.1,
        #     stroke_width=0,
        #     color=BLUE
        # )

        ###
        sentiments_l = pd.read_csv("data/Sentiment_Data.csv", index_col = 'Datetime')
        sentiments_l.index = pd.to_datetime(sentiments_l.index)
        avg_sentiments = sentiments_l.mean()

        max_neg_ma_scaled = max(y_vals_neg_ma_scaled)
        min_neg_ma_scaled = min(y_vals_neg_ma_scaled)

        max_pos_ma_scaled = max(y_vals_pos_ma_scaled)
        min_pos_ma_scaled = min(y_vals_pos_ma_scaled)

        avg_pos = (avg_sentiments['Postive'] * (max_pos_ma_scaled - min_pos_ma_scaled)) + min_pos_ma_scaled + 1000
        start = axes_price.c2p(0, avg_pos)
        end = axes_price.c2p(len(x_vals) + 10, avg_pos)
        dotted_line_pos = DashedLine(start=start, end=end, dash_length=0.1, color=BLUE)

        avg_neg = (avg_sentiments['Negative'] * (max_neg_ma_scaled - min_neg_ma_scaled)) + min_neg_ma_scaled + 1000
        start = axes_price.c2p(0, avg_neg)
        end = axes_price.c2p(len(x_vals) + 10, avg_neg)
        dotted_line_neg = DashedLine(start=start, end=end, dash_length=0.1, color=RED)

        # Axes Labels
        right_y_label = Text("Proportion", font_size=28).next_to(right_y_axis, UP)
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
        self.play(Create(graph_pos, 
                         run_time = 6))
        self.play(Create(graph_neg, 
                         run_time = 6))
        
        self.play(
            FadeOut(right_y_axis),
            FadeOut(right_tick_labels),
            FadeIn(new_right_y_axis),
            FadeIn(new_right_tick_labels),
            Transform(graph_pos, graph_pos_zoomed),
            Transform(graph_neg, graph_neg_zoomed),
            run_time = 1
            )
        self.wait(0.05)
        self.play(
            Transform(graph_pos_zoomed, graph_pos_ma),
            FadeOut(graph_pos),
            Transform(graph_neg_zoomed, graph_neg_ma),
            FadeOut(graph_neg),
            #FadeIn(shaded_region_pos),
            #FadeIn(shaded_region_neg),
            run_time = 1
            )
        # self.interactive_embed()
        # self.play(
        #     Create(dotted_line_pos), 
        #     Create(dotted_line_neg)
        #     )

        # self.interactive_embed()

class reference_dependence_story(Scene):
    def construct(self):
        # grid = NumberPlane(
        #     x_range=[-8, 8, 1],  # X-axis from -8 to 8 with 1 unit steps
        #     y_range=[-5, 5, 1],  # Y-axis from -5 to 5 with 1 unit steps
        #     background_line_style={
        #         "stroke_color": BLUE_D,
        #         "stroke_width": 1,
        #         "stroke_opacity": 0.5
        #     }
        # )
        # self.add(grid)

        title = Title("Reference Dependence in Sentiments")
        
        scene_1 = ImageMobject("images/scene_1.png").scale(0.5).move_to((-5,-1,0))
        scene_2 = ImageMobject("images/scene_2.png").scale(0.5).move_to((0,-1,0))
        scene_3 = ImageMobject("images/scene_3.png").scale(0.5).move_to((5,-1,0))

        self.add(title)
        
        self.play(FadeIn(scene_1))
        self.play(FadeIn(scene_2))
        self.play(FadeIn(scene_3))
