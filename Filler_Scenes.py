from manim import *
from manim.opengl import *
import pandas as pd

class Causes_Correlation(Scene):
    def construct(self):
        # Create both texts
        text = Text("1. Institutional Adoption\n2. Inflation Hedge\n3. Scarcity and Halving Events\n4. Global Economic Instability\n...\n...")

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

class focus(Scene):
    def construct(self):
        # Create both texts
        text = Text("Correlation of Human Emotions with Bitcoin Prices", font_size = 24)

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