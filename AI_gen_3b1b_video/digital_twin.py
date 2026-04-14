from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30


class CNNQualityInspection(Scene):
    """
    AI质检核心模型：卷积神经网络（CNN）
    包含架构展示、卷积原理、训练过程与应用演示
    """
    
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== 场景1：问题引入 ==========
        title = Text("AI质检：卷积神经网络", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text("CNN — Convolutional Neural Network", font="Microsoft YaHei", color=WHITE).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        # 展示一个简单的缺陷检测示意图
        product = RoundedRectangle(
            corner_radius=0.1,
            height=1.5,
            width=2.0,
            color=GRAY,
            fill_opacity=0.5,
            stroke_width=3,
        )
        product.move_to(LEFT * 3)
        
        defect = Circle(radius=0.15, color=RED, fill_opacity=0.8)
        defect.move_to(product.get_center() + RIGHT * 0.3 + UP * 0.2)
        
        arrow = Arrow(start=product.get_right(), end=product.get_right() + RIGHT * 2, color=WHITE)
        
        cnn_box = Rectangle(height=1.5, width=2.5, color=GREEN, fill_opacity=0.3)
        cnn_box.next_to(arrow, RIGHT, buff=0.5)
        cnn_text = Text("CNN", font="Microsoft YaHei", color=GREEN).scale(0.8)
        cnn_text.move_to(cnn_box.get_center())
        
        result_box = Rectangle(height=0.8, width=1.5, color=RED, fill_opacity=0.3)
        result_box.next_to(cnn_box, RIGHT, buff=0.8)
        result_text = Text("缺陷", font="Microsoft YaHei", color=RED).scale(0.6)
        result_text.move_to(result_box.get_center())
        
        self.play(
            Create(product),
            FadeIn(defect),
            GrowArrow(arrow),
            Create(cnn_box),
            Write(cnn_text),
            Create(result_box),
            Write(result_text),
            run_time=2
        )
        self.wait(1.5)
        
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(product),
            FadeOut(defect),
            FadeOut(arrow),
            FadeOut(cnn_box),
            FadeOut(cnn_text),
            FadeOut(result_box),
            FadeOut(result_text),
        )
        
        # ========== 场景2：CNN架构 ==========
        title_arch = Text("CNN 经典架构", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_arch.to_edge(UP)
        self.play(Write(title_arch))
        
        # 输入图像
        input_block = Rectangle(height=1.5, width=1.5, color=WHITE, fill_opacity=0.2)
        input_block.shift(LEFT * 5)
        input_label = Text("输入图像", font="Microsoft YaHei", color=WHITE).scale(0.5)
        input_label.next_to(input_block, DOWN, buff=0.2)
        
        # 卷积层1
        conv1_block = Rectangle(height=1.2, width=1.2, color=BLUE, fill_opacity=0.3)
        conv1_block.next_to(input_block, RIGHT, buff=0.8)
        conv1_label = Text("卷积层", font="Microsoft YaHei", color=BLUE).scale(0.45)
        conv1_label.next_to(conv1_block, DOWN, buff=0.2)
        
        # 池化层1
        pool1_block = Rectangle(height=0.9, width=0.9, color=GREEN, fill_opacity=0.3)
        pool1_block.next_to(conv1_block, RIGHT, buff=0.6)
        pool1_label = Text("池化层", font="Microsoft YaHei", color=GREEN).scale(0.45)
        pool1_label.next_to(pool1_block, DOWN, buff=0.2)
        
        # 卷积层2
        conv2_block = Rectangle(height=0.7, width=0.7, color=BLUE, fill_opacity=0.3)
        conv2_block.next_to(pool1_block, RIGHT, buff=0.6)
        conv2_label = Text("卷积层", font="Microsoft YaHei", color=BLUE).scale(0.4)
        conv2_label.next_to(conv2_block, DOWN, buff=0.2)
        
        # 池化层2
        pool2_block = Rectangle(height=0.5, width=0.5, color=GREEN, fill_opacity=0.3)
        pool2_block.next_to(conv2_block, RIGHT, buff=0.6)
        pool2_label = Text("池化层", font="Microsoft YaHei", color=GREEN).scale(0.4)
        pool2_label.next_to(pool2_block, DOWN, buff=0.2)
        
        # 全连接层
        fc_block = Rectangle(height=0.4, width=1.2, color=PURPLE, fill_opacity=0.3)
        fc_block.next_to(pool2_block, RIGHT, buff=0.8)
        fc_label = Text("全连接层", font="Microsoft YaHei", color=PURPLE).scale(0.4)
        fc_label.next_to(fc_block, DOWN, buff=0.2)
        
        # 输出
        out_block = Rectangle(height=0.3, width=0.6, color=YELLOW, fill_opacity=0.3)
        out_block.next_to(fc_block, RIGHT, buff=0.8)
        out_label = Text("输出", font="Microsoft YaHei", color=YELLOW).scale(0.4)
        out_label.next_to(out_block, DOWN, buff=0.2)
        
        # 箭头连接
        arrows = VGroup()
        blocks = [input_block, conv1_block, pool1_block, conv2_block, pool2_block, fc_block, out_block]
        for i in range(len(blocks) - 1):
            arr = Arrow(
                start=blocks[i].get_right(),
                end=blocks[i+1].get_left(),
                color=GRAY,
                buff=0.1,
            )
            arrows.add(arr)
        
        self.play(
            Create(input_block), Write(input_label),
            Create(conv1_block), Write(conv1_label),
            Create(pool1_block), Write(pool1_label),
            Create(conv2_block), Write(conv2_label),
            Create(pool2_block), Write(pool2_label),
            Create(fc_block), Write(fc_label),
            Create(out_block), Write(out_label),
            *[Create(arr) for arr in arrows],
            run_time=3
        )
        self.wait(2)
        
        self.play(
            FadeOut(title_arch),
            *[FadeOut(b) for b in blocks],
            *[FadeOut(l) for l in [input_label, conv1_label, pool1_label, conv2_label, pool2_label, fc_label, out_label]],
            *[FadeOut(arr) for arr in arrows],
        )
        
        # ========== 场景3：卷积操作原理 ==========
        title_conv = Text("卷积操作数学原理", font="Microsoft YaHei", color=GREEN).scale(0.9)
        title_conv.to_edge(UP)
        self.play(Write(title_conv))
        
        # 展示一个 5x5 输入矩阵和 3x3 卷积核
        input_matrix = Matrix(
            [[1, 2, 1, 0, 2],
             [0, 1, 3, 2, 1],
             [2, 1, 0, 1, 0],
             [1, 0, 2, 1, 3],
             [0, 2, 1, 0, 1]],
            v_buff=0.5,
            h_buff=0.5,
        )
        input_matrix.scale(0.6)
        input_matrix.move_to(LEFT * 3)
        input_title = Text("输入特征图 (5×5)", font="Microsoft YaHei", color=WHITE).scale(0.5)
        input_title.next_to(input_matrix, UP, buff=0.2)
        
        kernel_matrix = Matrix(
            [[1, 0, -1],
             [1, 0, -1],
             [1, 0, -1]],
            v_buff=0.5,
            h_buff=0.5,
        )
        kernel_matrix.scale(0.6)
        kernel_matrix.move_to(RIGHT * 0)
        kernel_title = Text("卷积核 (3×3)", font="Microsoft YaHei", color=WHITE).scale(0.5)
        kernel_title.next_to(kernel_matrix, UP, buff=0.2)
        
        op_symbol = MathTex(r"\circledast", color=YELLOW).scale(1.5)
        op_symbol.move_to(RIGHT * 2.5)
        
        output_matrix = Matrix(
            [[4, 2, 3],
             [3, 2, 4],
             [2, 3, 2]],
            v_buff=0.5,
            h_buff=0.5,
        )
        output_matrix.scale(0.6)
        output_matrix.move_to(RIGHT * 4.5)
        output_title = Text("输出特征图 (3×3)", font="Microsoft YaHei", color=WHITE).scale(0.5)
        output_title.next_to(output_matrix, UP, buff=0.2)
        
        self.play(
            Write(input_title),
            Create(input_matrix),
            Write(kernel_title),
            Create(kernel_matrix),
            Write(op_symbol),
            Write(output_title),
            Create(output_matrix),
            run_time=2
        )
        
        # 卷积公式
        conv_formula = MathTex(
            r"(I * K)(i,j) = \sum_{m=0}^{2} \sum_{n=0}^{2} I(i+m, j+n) \cdot K(m,n)",
            color=YELLOW
        ).scale(0.8)
        conv_formula.next_to(output_title, DOWN, buff=0.8)
        conv_formula.to_edge(RIGHT, buff=0.5)
        
        self.play(Write(conv_formula))
        self.wait(2)
        
        # 展示一个具体的计算示例
        example_calc = MathTex(
            r"1\times1 + 2\times0 + 1\times(-1) + 0\times1 + 1\times0 + 3\times(-1) + 2\times1 + 1\times0 + 0\times(-1) = 4",
            color=WHITE
        ).scale(0.6)
        example_calc.next_to(conv_formula, DOWN, buff=0.4)
        
        self.play(Write(example_calc))
        self.wait(2)
        
        self.play(
            FadeOut(title_conv),
            FadeOut(input_title), FadeOut(input_matrix),
            FadeOut(kernel_title), FadeOut(kernel_matrix),
            FadeOut(op_symbol),
            FadeOut(output_title), FadeOut(output_matrix),
            FadeOut(conv_formula), FadeOut(example_calc),
        )
        
        # ========== 场景4：训练过程 ==========
        title_train = Text("CNN 训练过程", font="Microsoft YaHei", color=PURPLE).scale(0.9)
        title_train.to_edge(UP)
        self.play(Write(title_train))
        
        # 前向传播
        forward_eq = MathTex(
            r"\text{前向传播: } \hat{y} = f_{\theta}(x)",
            color=GREEN
        ).scale(1.0)
        forward_eq.next_to(title_train, DOWN, buff=0.6)
        forward_eq.to_edge(LEFT, buff=1.5)
        
        # 损失函数
        loss_eq = MathTex(
            r"\text{损失函数: } \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell(y_i, \hat{y}_i)",
            color=ORANGE
        ).scale(0.9)
        loss_eq.next_to(forward_eq, DOWN, buff=0.4)
        
        # 反向传播
        backward_eq = MathTex(
            r"\text{反向传播: } \nabla_{\theta} \mathcal{L} = \frac{\partial \mathcal{L}}{\partial \theta}",
            color=RED
        ).scale(0.9)
        backward_eq.next_to(loss_eq, DOWN, buff=0.4)
        
        # 参数更新
        update_eq = MathTex(
            r"\text{参数更新: } \theta \leftarrow \theta - \eta \cdot \nabla_{\theta} \mathcal{L}",
            color=BLUE
        ).scale(0.9)
        update_eq.next_to(backward_eq, DOWN, buff=0.4)
        
        self.play(Write(forward_eq), run_time=0.8)
        self.play(Write(loss_eq), run_time=0.8)
        self.play(Write(backward_eq), run_time=0.8)
        self.play(Write(update_eq), run_time=0.8)
        
        # 训练循环图示
        loop_arrow = CurvedArrow(
            start_point=update_eq.get_bottom() + DOWN * 0.3 + RIGHT * 1,
            end_point=forward_eq.get_top() + UP * 0.3 + RIGHT * 1,
            angle=-0.8,
            color=GRAY,
        )
        loop_text = Text("迭代训练", font="Microsoft YaHei", color=GRAY).scale(0.5)
        loop_text.next_to(loop_arrow, RIGHT, buff=0.1)
        
        self.play(Create(loop_arrow), Write(loop_text))
        self.wait(2)
        
        self.play(
            FadeOut(title_train),
            FadeOut(forward_eq), FadeOut(loss_eq),
            FadeOut(backward_eq), FadeOut(update_eq),
            FadeOut(loop_arrow), FadeOut(loop_text),
        )
        
        # ========== 场景5：钢材缺陷检测应用 ==========
        title_app = Text("应用：钢材表面缺陷检测", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_app.to_edge(UP)
        self.play(Write(title_app))
        
        # 展示6种典型缺陷
        defects = ["轧入氧化皮", "斑块", "裂纹", "麻点", "夹杂", "划痕"]
        colors = [YELLOW, ORANGE, RED, GREEN, BLUE, PURPLE]
        
        defect_boxes = VGroup()
        for i, (d, c) in enumerate(zip(defects, colors)):
            box = RoundedRectangle(
                corner_radius=0.05,
                height=0.8,
                width=1.8,
                color=c,
                fill_opacity=0.3,
            )
            box.shift(LEFT * 4.5 + RIGHT * (i % 3) * 3.5)
            box.shift(UP * 1.5 + DOWN * (i // 3) * 1.5)
            label = Text(d, font="Microsoft YaHei", color=c).scale(0.45)
            label.move_to(box.get_center())
            defect_boxes.add(VGroup(box, label))
        
        self.play(Create(defect_boxes), run_time=2)
        
        # CNN检测流程图
        flow_text = Text(
            "CNN 自动识别 → 实时缺陷分类 → 质量数据反馈",
            font="Microsoft YaHei", color=WHITE
        ).scale(0.6)
        flow_text.next_to(defect_boxes, DOWN, buff=1.0)
        
        self.play(Write(flow_text))
        
        # 性能指标
        metrics = VGroup(
            MathTex(r"\text{mAP} = 81.4\%", color=GREEN).scale(0.8),
            Text("(在NEU-DET数据集上)", font="Microsoft YaHei", color=GRAY).scale(0.5),
        ).arrange(RIGHT, buff=0.2)
        metrics.next_to(flow_text, DOWN, buff=0.5)
        
        self.play(Write(metrics))
        self.wait(2)
        
        # 结论
        conclusion = Text(
            "CNN 已成为工业AI质检的核心技术，实现高效、准确的缺陷自动检测",
            font="Microsoft YaHei", color=BLUE
        ).scale(0.65)
        conclusion.to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(3)
        
        self.play(
            FadeOut(title_app),
            FadeOut(defect_boxes),
            FadeOut(flow_text),
            FadeOut(metrics),
            FadeOut(conclusion),
        )
        self.wait(0.5)