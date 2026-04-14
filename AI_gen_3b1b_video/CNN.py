from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30


class CNNCoreMechanisms(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        self.show_main_title()
        self.section_card("第一部分：CNN 基础机制", "Core Mechanisms of CNN")

        self.kernel_mechanism()
        self.stride_mechanism()
        self.padding_mechanism()
        self.multichannel_mechanism()
        self.pooling_mechanism()
        self.activation_mechanism()

        self.final_summary()

    # ---------------- Common helpers ----------------
    def show_main_title(self):
        title = Text("CNN 基础机制", font="Microsoft YaHei", color=BLUE).scale(1.0)
        subtitle = Text("Core Mechanisms of Convolutional Neural Networks", font="Microsoft YaHei", color=WHITE).scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.16)
        note = Text("每一段都包含：公式、参数标注、图形演示、参数变化", font="Microsoft YaHei", color=GRAY).scale(0.42)
        note.next_to(subtitle, DOWN, buff=0.26)
        self.play(Write(title), Write(subtitle), FadeIn(note), run_time=2)
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(note), run_time=0.8)

    def section_card(self, cn, en):
        card = RoundedRectangle(corner_radius=0.18, width=10.8, height=3.0, color=BLUE, fill_opacity=0.14)
        title = Text(cn, font="Microsoft YaHei", color=BLUE).scale(0.88)
        subtitle = Text(en, font="Microsoft YaHei", color=WHITE).scale(0.52)
        subtitle.next_to(title, DOWN, buff=0.16)
        title.move_to(card.get_center() + UP * 0.3)
        subtitle.move_to(card.get_center() + DOWN * 0.4)
        self.play(FadeIn(card), Write(title), Write(subtitle), run_time=1.6)
        self.wait(0.9)
        self.play(FadeOut(card), FadeOut(title), FadeOut(subtitle), run_time=0.8)

    def page_header(self, cn, en, color=YELLOW):
        header_cn = Text(cn, font="Microsoft YaHei", color=color).scale(0.82)
        header_en = Text(en, font="Microsoft YaHei", color=WHITE).scale(0.42)
        header_en.next_to(header_cn, DOWN, buff=0.12)
        header = VGroup(header_cn, header_en)
        header.to_edge(UP, buff=0.36)
        self.play(Write(header), run_time=0.8)
        return header

    def clear_except(self, keep=None):
        keep = keep or []
        keep_ids = {id(m) for m in keep}
        fade_targets = [m for m in self.mobjects if id(m) not in keep_ids]
        if fade_targets:
            self.play(*[FadeOut(m) for m in fade_targets], run_time=0.6)

    def make_param_box(self, title, items, width=4.8):
        box = RoundedRectangle(corner_radius=0.12, width=width, height=0.9 + 0.42 * len(items), color=BLUE, fill_opacity=0.08)
        t = Text(title, font="Microsoft YaHei", color=BLUE).scale(0.42)
        t.move_to(box.get_top() + DOWN * 0.28)
        lines = VGroup(*[
            Text(line, font="Microsoft YaHei", color=WHITE).scale(0.36)
            for line in items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lines.next_to(t, DOWN, buff=0.18)
        lines.align_to(box.get_left() + RIGHT * 0.25, LEFT)
        return VGroup(box, t, lines)

    def make_bullets(self, lines, y=-3.0):
        group = VGroup(*[
            Text(line, font="Microsoft YaHei", color=WHITE).scale(0.36)
            for line in lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        group.to_edge(DOWN, buff=0.35)
        group.shift(UP * (y + 3.0))
        return group

    def matrix_with_title(self, data, title_text, scale=0.55, color=WHITE):
        mat = Matrix(data, v_buff=0.55, h_buff=0.55).scale(scale)
        title = Text(title_text, font="Microsoft YaHei", color=color).scale(0.38)
        title.next_to(mat, UP, buff=0.14)
        return VGroup(mat, title)

    def output_size_value(self, n, f, p, s):
        return int(np.floor((n + 2 * p - f) / s) + 1)

    def _convolve2d(self, input_matrix, kernel_matrix):
        input_rows, input_cols = input_matrix.shape
        kernel_rows, kernel_cols = kernel_matrix.shape
        
        output_rows = input_rows - kernel_rows + 1
        output_cols = input_cols - kernel_cols + 1
        
        output_matrix = np.zeros((output_rows, output_cols), dtype=int)
        
        for i in range(output_rows):
            for j in range(output_cols):
                patch = input_matrix[i:i+kernel_rows, j:j+kernel_cols]
                output_matrix[i, j] = np.sum(patch * kernel_matrix)
                
        return output_matrix

    def draw_feature_grid(self, rows, cols, cell_size=0.35, values=None, color=WHITE):
        squares = VGroup()
        texts = VGroup()
        for i in range(rows):
            for j in range(cols):
                sq = Square(side_length=cell_size, color=color, stroke_width=1.5)
                sq.move_to(np.array([(j - (cols - 1) / 2) * cell_size, ((rows - 1) / 2 - i) * cell_size, 0]))
                squares.add(sq)
                if values is not None:
                    txt = Text(str(values[i][j]), font="Arial", color=WHITE).scale(cell_size * 0.95)
                    txt.move_to(sq.get_center())
                    texts.add(txt)
        return VGroup(squares, texts)

    # ---------------- 1. Kernel mechanism ----------------
    def kernel_mechanism(self):
        header = self.page_header("机制1：卷积核在做什么", "Mechanism 1: What a Convolution Kernel Does", YELLOW)

        input_data = np.array([
            [1, 2, 1, 0, 2],
            [0, 1, 3, 2, 1],
            [2, 1, 0, 1, 0],
            [1, 0, 2, 1, 3],
            [0, 2, 1, 0, 1],
        ])
        kernel_data = np.array([
            [ 1,  0, -1],
            [ 1,  0, -1],
            [ 1,  0, -1],
        ])

        # Correctly calculate the output for the initial edge detection kernel
        correct_edge_output = self._convolve2d(input_data, kernel_data)

        # Define a smoothing kernel for later use
        smoothing_kernel_data = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])

        input_group = self.matrix_with_title(input_data, "输入特征图 X")
        kernel_group = self.matrix_with_title(kernel_data, "卷积核 K", scale=0.5, color=YELLOW)
        out_group = self.matrix_with_title(correct_edge_output, "输出特征图 Z", scale=0.5, color=GREEN)

        # Arrange the three main groups horizontally
        VGroup(input_group, kernel_group, out_group).arrange(RIGHT, buff=1.0).center()

        a1 = Arrow(input_group[0].get_right(), kernel_group[0].get_left(), buff=0.14)
        a2 = Arrow(kernel_group[0].get_right(), out_group[0].get_left(), buff=0.14)

        self.play(FadeIn(input_group), FadeIn(kernel_group), FadeIn(out_group), GrowArrow(a1), GrowArrow(a2), run_time=1.8)

        formula = MathTex(
            r"z_{i,j}=\sum_{u=0}^{f-1}\sum_{v=0}^{f-1}K_{u,v}X_{i+u,j+v}",
            color=YELLOW,
        ).scale(0.72)
        formula.move_to(DOWN * 2.5)
        param_box = self.make_param_box("参数含义", [
            r"X: 输入图像或特征图",
            r"K: 卷积核",
            r"f: 卷积核尺寸",
            r"z_{i,j}: 输出位置 (i,j) 的响应",
            r"u,v: 卷积核内部坐标",
        ], width=4.6)
        param_box.next_to(formula, RIGHT, buff=1.0)

        self.play(Write(formula), FadeIn(param_box), run_time=1.5)

        # highlight one local patch
        cell_size = 0.55 * 0.6
        origin = input_group[0].get_center()
        matrix = input_group[0]
        input_entries = matrix.get_entries()
        patch_indices = [0,1,2,5,6,7,10,11,12]
        patch_rects = VGroup(*[SurroundingRectangle(input_entries[i], color=RED, buff=0.03) for i in patch_indices])
        out_entry = SurroundingRectangle(out_group[0].get_entries()[0], color=RED, buff=0.03)
        calc = MathTex(
            r"1\cdot1+2\cdot0+1\cdot(-1)+0\cdot1+1\cdot0+3\cdot(-1)+2\cdot1+1\cdot0+0\cdot(-1)=-1",
            color=WHITE,
        ).scale(0.48)
        calc.next_to(formula, UP, buff=0.22)
        self.play(Write(calc), run_time=1.6)

        # parameter change: kernel content
        smooth_group = self.matrix_with_title(smoothing_kernel_data, "平滑卷积核", scale=0.5, color=BLUE)
        smooth_group.move_to(kernel_group)
        note = self.make_bullets([
            "同样大小的卷积核，内容不同，提取的模式也不同。",
            "边缘核更关注突变，平滑核更关注局部平均。",
        ], y=-2.7)
        self.play(ReplacementTransform(kernel_group, smooth_group), FadeIn(note), run_time=1.4)
        self.wait(1.1)

        self.clear_except([])

    # ---------------- 2. Stride mechanism ----------------
    def stride_mechanism(self):
        header = self.page_header("机制2：Stride 的作用", "Mechanism 2: The Role of Stride", YELLOW)

        formula = MathTex(
            r"n_{out}=\left\lfloor \frac{n+2p-f}{s} \right\rfloor + 1",
            color=YELLOW,
        ).scale(0.86)
        formula.shift(LEFT * 2.5 + UP * 0.5)
        param_box = self.make_param_box("参数含义", [
            r"n: 输入尺寸",
            r"f: 卷积核大小",
            r"p: padding 大小",
            r"s: stride 步长",
            r"n_{out}: 输出尺寸",
        ], width=4.4)
        param_box.next_to(formula, RIGHT, buff=1.0)

        self.play(Write(formula), FadeIn(param_box), run_time=1.4)

        base = self.draw_feature_grid(5, 5, cell_size=0.46, values=[["" for _ in range(5)] for _ in range(5)])
        base.to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        label = Text("输入网格", font="Microsoft YaHei", color=WHITE).scale(0.38).next_to(base, UP, buff=0.16)
        self.play(FadeIn(base), Write(label), run_time=0.8)

        # stride 1 path
        s1_positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        squares = base[0]
        highlight1 = VGroup()
        for i, j in s1_positions:
            idx = i * 5 + j
            highlight1.add(SurroundingRectangle(squares[idx], color=GREEN, buff=0.02))
        s1_text = Text("s = 1", font="Arial", color=GREEN).scale(0.44).shift(LEFT * 0.8 + DOWN * 0.1)
        out1 = self.draw_feature_grid(3, 3, cell_size=0.34)
        out1.next_to(base, RIGHT, buff=2.0).shift(UP * 0.2)
        out1_label = Text("输出尺寸 3×3", font="Microsoft YaHei", color=GREEN).scale(0.36).next_to(out1, UP, buff=0.14)
        self.play(Create(highlight1), Write(s1_text), FadeIn(out1), Write(out1_label), run_time=1.5)

        # stride 2 path
        self.play(FadeOut(highlight1), FadeOut(s1_text), FadeOut(out1), FadeOut(out1_label), run_time=0.5)
        s2_positions = [(0,0), (0,2), (2,0), (2,2)]
        highlight2 = VGroup()
        for i, j in s2_positions:
            idx = i * 5 + j
            highlight2.add(SurroundingRectangle(squares[idx], color=RED, buff=0.02))
        s2_text = Text("s = 2", font="Arial", color=RED).scale(0.44).shift(LEFT * 0.8 + DOWN * 0.1)
        out2 = self.draw_feature_grid(2, 2, cell_size=0.42)
        out2.move_to(out1)
        out2_label = Text("输出尺寸 2×2", font="Microsoft YaHei", color=RED).scale(0.36).next_to(out2, UP, buff=0.14)
        note = self.make_bullets([
            "stride 变大后，采样位置更稀疏。",
            "输出尺寸减小，细节信息也更容易丢失。",
        ], y=-2.7)
        self.play(Create(highlight2), Write(s2_text), FadeIn(out2), Write(out2_label), FadeIn(note), run_time=1.6)
        self.wait(1.1)

        self.clear_except([])

    # ---------------- 3. Padding mechanism ----------------
    def padding_mechanism(self):
        header = self.page_header("机制3：Padding 的作用", "Mechanism 3: The Role of Padding", YELLOW)

        formula = MathTex(
            r"n_{out}=\left\lfloor \frac{n+2p-f}{s} \right\rfloor + 1",
            color=YELLOW,
        ).scale(0.84)
        formula.shift(LEFT * 2.5 + UP * 0.5)
        param_box = self.make_param_box("参数含义", [
            r"p: 在边界外补零的层数",
            r"p = 0: 无 padding",
            r"p > 0: 保留更多边界信息",
        ], width=4.2)
        param_box.next_to(formula, RIGHT, buff=1.0)
        self.play(Write(formula), FadeIn(param_box), run_time=1.3)

        input_grid = self.draw_feature_grid(5, 5, cell_size=0.44)
        input_grid.to_edge(LEFT, buff=1.0).shift(DOWN * 1.0)
        input_label = Text("输入 5×5", font="Microsoft YaHei", color=WHITE).scale(0.36).next_to(input_grid, UP, buff=0.14)
        self.play(FadeIn(input_grid), Write(input_label), run_time=0.8)

        no_pad = self.draw_feature_grid(3, 3, cell_size=0.34)
        no_pad.shift(RIGHT * 0.5 + DOWN * 0.05)
        no_pad_label = Text("p = 0 → 输出 3×3", font="Microsoft YaHei", color=RED).scale(0.36).next_to(no_pad, UP, buff=0.14)
        same_pad = self.draw_feature_grid(5, 5, cell_size=0.28)
        same_pad.shift(RIGHT * 4.3 + DOWN * 0.05)
        same_pad_label = Text("p = 1 → 输出 5×5", font="Microsoft YaHei", color=GREEN).scale(0.36).next_to(same_pad, UP, buff=0.14)
        edge_box = SurroundingRectangle(input_grid[0][0], color=YELLOW, buff=0.02)
        self.play(Create(edge_box), FadeIn(no_pad), Write(no_pad_label), FadeIn(same_pad), Write(same_pad_label), run_time=1.5)

        note = self.make_bullets([
            "padding 不只是为了保持尺寸。",
            "它还会影响边界区域被卷积核看到多少次。",
        ], y=-2.7)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(1.0)

        self.clear_except([])

    # ---------------- 4. Multi-channel mechanism ----------------
    def multichannel_mechanism(self):
        header = self.page_header("机制4：多通道卷积", "Mechanism 4: Multi-channel Convolution", YELLOW)

        formula = MathTex(
            r"z_{i,j,k}=\sum_{u,v,c}W^{(k)}_{u,v,c}X_{i+u,j+v,c}+b_k",
            color=YELLOW,
        ).scale(0.72)
        formula.shift(LEFT * 2.5 + UP * 0.5)
        param_box = self.make_param_box("参数含义", [
            r"c: 输入通道索引",
            r"k: 输出通道索引",
            r"W^{(k)}: 第 k 个卷积核组",
            r"b_k: 第 k 个输出通道偏置",
        ], width=4.4)
        param_box.next_to(formula, RIGHT, buff=1.0)
        self.play(Write(formula), FadeIn(param_box), run_time=1.4)

        # RGB inputs
        ch1 = Square(side_length=1.2, color=RED, fill_opacity=0.25)
        ch2 = Square(side_length=1.2, color=GREEN, fill_opacity=0.25)
        ch3 = Square(side_length=1.2, color=BLUE, fill_opacity=0.25)
        rgb = VGroup(ch1, ch2, ch3).arrange(RIGHT, buff=0.18).to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        rgb_labels = VGroup(
            Text("R", font="Arial", color=RED).scale(0.52).move_to(ch1),
            Text("G", font="Arial", color=GREEN).scale(0.52).move_to(ch2),
            Text("B", font="Arial", color=BLUE).scale(0.52).move_to(ch3),
        )
        kernel_stack = VGroup(
            Square(side_length=0.7, color=RED, fill_opacity=0.2),
            Square(side_length=0.7, color=GREEN, fill_opacity=0.2),
            Square(side_length=0.7, color=BLUE, fill_opacity=0.2),
        ).arrange(DOWN, buff=0.06).next_to(rgb, RIGHT, buff=1.5)
        kernel_label = Text("一个卷积核组", font="Microsoft YaHei", color=YELLOW).scale(0.36).next_to(kernel_stack, UP, buff=0.14)
        out1 = Square(side_length=1.0, color=YELLOW, fill_opacity=0.2).next_to(kernel_stack, RIGHT, buff=1.5)
        out1_text = Text("1 个输出通道", font="Microsoft YaHei", color=YELLOW).scale(0.34).next_to(out1, DOWN, buff=0.14)
        a1 = Arrow(rgb.get_right(), kernel_stack.get_left(), buff=0.14)
        a2 = Arrow(kernel_stack.get_right(), out1.get_left(), buff=0.14)
        self.play(FadeIn(rgb), FadeIn(rgb_labels), GrowArrow(a1), FadeIn(kernel_stack), Write(kernel_label), GrowArrow(a2), FadeIn(out1), Write(out1_text), run_time=1.9)

        # multiple output channels
        out_multi = VGroup(
            Square(side_length=0.72, color=YELLOW, fill_opacity=0.18),
            Square(side_length=0.72, color=ORANGE, fill_opacity=0.18),
            Square(side_length=0.72, color=PURPLE, fill_opacity=0.18),
            Square(side_length=0.72, color=TEAL, fill_opacity=0.18),
        ).arrange(RIGHT, buff=0.12).move_to(out1)
        out_multi_text = Text("输出通道数增加", font="Microsoft YaHei", color=GREEN).scale(0.36).next_to(out_multi, DOWN, buff=0.14)
        note = self.make_bullets([
            "输入通道数固定时，输出通道数越多，学到的特征类型通常越丰富。",
            "但参数量和计算量也会一起增加。",
        ], y=-2.7)
        self.play(ReplacementTransform(out1, out_multi), ReplacementTransform(out1_text, out_multi_text), FadeIn(note), run_time=1.3)
        self.wait(1.1)

        self.clear_except([])

    # ---------------- 5. Pooling mechanism ----------------
    def pooling_mechanism(self):
        header = self.page_header("机制5：Pooling 的作用", "Mechanism 5: The Role of Pooling", YELLOW)

        max_formula = MathTex(
            r"y_{i,j,k}=\max_{(u,v)\in\Omega} x_{i+u,j+v,k}",
            color=YELLOW,
        ).scale(0.62)
        avg_formula = MathTex(
            r"y_{i,j,k}=\frac{1}{|\Omega|}\sum_{(u,v)\in\Omega} x_{i+u,j+v,k}",
            color=BLUE,
        ).scale(0.62)
        formulas = VGroup(max_formula, avg_formula).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        formulas.shift(LEFT * 2.5 + UP * 0.5)
        param_box = self.make_param_box("参数含义", [
            r"\Omega: 池化窗口",
            r"|\Omega|: 窗口元素个数",
            r"max pooling: 保留最强响应",
            r"avg pooling: 取局部平均",
        ], width=4.6)
        param_box.next_to(formulas, RIGHT, buff=1.0)
        self.play(Write(formulas), FadeIn(param_box), run_time=1.4)

        values = [[1, 3, 2, 1], [0, 4, 1, 2], [2, 1, 5, 0], [1, 2, 2, 3]]
        inp = self.matrix_with_title(values, "输入特征图", scale=0.46)
        inp.to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        max_out = self.matrix_with_title([[4, 2], [2, 5]], "Max Pooling", scale=0.5, color=YELLOW)
        max_out.next_to(inp, RIGHT, buff=1.5).shift(UP * 0.2)
        avg_out = self.matrix_with_title([[2.0, 1.5], [1.5, 2.5]], "Average Pooling", scale=0.5, color=BLUE)
        avg_out.next_to(max_out, RIGHT, buff=1.5).shift(UP * 0.2)
        a1 = Arrow(inp[0].get_right(), max_out[0].get_left(), buff=0.14)
        a2 = Arrow(inp[0].get_right(), avg_out[0].get_left(), buff=0.14)
        self.play(FadeIn(inp), GrowArrow(a1), GrowArrow(a2), FadeIn(max_out), FadeIn(avg_out), run_time=1.8)

        patch = VGroup(*[SurroundingRectangle(inp[0].get_entries()[i], color=RED, buff=0.02) for i in [0,1,4,5]])
        note = self.make_bullets([
            "max pooling 更容易保留局部最显著的激活。",
            "average pooling 更平滑，更像局部平均压缩。",
        ], y=-2.7)
        self.play(Create(patch), FadeIn(note), run_time=1.2)
        self.wait(1.1)

        self.clear_except([])

    # ---------------- 6. Activation mechanism ----------------
    def activation_mechanism(self):
        header = self.page_header("机制6：Activation 的作用", "Mechanism 6: The Role of Activation", YELLOW)

        relu = MathTex(r"\mathrm{ReLU}(x)=\max(0,x)", color=YELLOW).scale(0.8)
        drelu = MathTex(
            r"\frac{d}{dx}\mathrm{ReLU}(x)=\begin{cases}1,&x>0\\0,&x<0\end{cases}",
            color=YELLOW,
        ).scale(0.68)
        sigmoid = MathTex(r"\sigma(x)=\frac{1}{1+e^{-x}}", color=BLUE).scale(0.76)
        dsg = MathTex(r"\sigma'(x)=\sigma(x)(1-\sigma(x))", color=BLUE).scale(0.68)
        left_group = VGroup(relu, drelu, sigmoid, dsg).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left_group.to_edge(LEFT, buff=1.0).shift(UP * 0.5)
        param_box = self.make_param_box("变量说明", [
            r"x: 神经元输入",
            r"ReLU(x): 激活输出",
            r"\sigma(x): sigmoid 输出",
        ], width=3.8)
        param_box.next_to(left_group, RIGHT, buff=1.0)
        self.play(Write(left_group), FadeIn(param_box), run_time=1.4)

        axes = Axes(x_range=[-3, 3, 1], y_range=[-0.2, 3, 1], x_length=4.0, y_length=2.7, tips=False)
        axes.next_to(param_box, RIGHT, buff=1.0).shift(DOWN * 0.5)
        relu_curve = axes.plot(lambda x: max(0, x), x_range=[-3, 3], color=YELLOW)
        sig_curve = axes.plot(lambda x: 1 / (1 + np.exp(-x)), x_range=[-3, 3], color=BLUE)
        curve_label = VGroup(
            Text("ReLU", font="Arial", color=YELLOW).scale(0.36),
            Text("sigmoid", font="Arial", color=BLUE).scale(0.36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(axes, RIGHT, buff=0.18)
        self.play(Create(axes), Create(relu_curve), Create(sig_curve), Write(curve_label), run_time=1.6)

        feature_before = self.matrix_with_title([[-2, 1, -1], [0, 3, -2], [2, -1, 1]], "激活前", scale=0.46)
        feature_before.shift(LEFT * 1.2 + DOWN * 2.0)
        feature_after = self.matrix_with_title([[0, 1, 0], [0, 3, 0], [2, 0, 1]], "ReLU 后", scale=0.46, color=GREEN)
        feature_after.shift(RIGHT * 2.4 + DOWN * 2.0)
        arrow = Arrow(feature_before[0].get_right(), feature_after[0].get_left(), buff=0.14)
        note = self.make_bullets([
            "ReLU 会把负值直接截断为 0。",
            "相比 sigmoid，ReLU 在正半轴的梯度传播更直接。",
        ], y=-2.8)
        self.play(FadeIn(feature_before), GrowArrow(arrow), FadeIn(feature_after), FadeIn(note), run_time=1.6)
        self.wait(1.2)

        self.clear_except([])

    # ---------------- Final summary ----------------
    def final_summary(self):
        header = self.page_header("总结", "Summary", BLUE)
        box = RoundedRectangle(corner_radius=0.15, width=11.3, height=4.6, color=WHITE, fill_opacity=0.08)
        points = VGroup(
            Text("1. 卷积核决定提取什么局部模式", font="Microsoft YaHei", color=WHITE).scale(0.5),
            Text("2. stride 和 padding 决定采样密度与空间尺寸", font="Microsoft YaHei", color=WHITE).scale(0.5),
            Text("3. 通道数、pooling 和 activation 会改变特征表达方式", font="Microsoft YaHei", color=WHITE).scale(0.5),
            Text("4. 后面的 CNN 变体，本质上都在围绕这些基础机制做改造", font="Microsoft YaHei", color=WHITE).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        points.move_to(box.get_center())
        self.play(Create(box), Write(points), run_time=1.9)
        self.wait(1.8)
        self.clear_except([])
