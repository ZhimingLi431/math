from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30


class RULPredictionModel(Scene):
    """
    预测性维护核心模型：剩余使用寿命（RUL）
    完全避免 MathTex 中包含中文
    """
    
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== 场景1：问题引入 ==========
        title = Text("预测性维护：剩余使用寿命", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text("RUL — Remaining Useful Life", font="Microsoft YaHei", color=WHITE).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        # 绘制退化曲线坐标轴
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.5, 0.25],
            x_length=9,
            y_length=4,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.6, 0.25)},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)
        
        # 坐标轴标签（中文用 Text，数学用 MathTex）
        x_label = Text("时间 t", font="Microsoft YaHei", color=GRAY).scale(0.6)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("退化指标 D(t)", font="Microsoft YaHei", color=GRAY).scale(0.6)
        y_label.next_to(axes.y_axis, UP, buff=0.1)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # 退化曲线
        def degradation_curve(t, D0=0.02, lam=0.15):
            return D0 * np.exp(lam * t)
        
        curve = axes.plot(
            lambda t: degradation_curve(t),
            x_range=[0, 8.5],
            color=YELLOW,
            stroke_width=4,
        )
        
        # 失效阈值线
        threshold = 1.0
        threshold_line = DashedLine(
            start=axes.c2p(0, threshold),
            end=axes.c2p(10, threshold),
            color=RED,
            stroke_width=3,
            dash_length=0.1,
        )
        
        # 阈值标签：希腊字母 + 中文说明
        threshold_label = VGroup(
            MathTex(r"\theta", color=RED).scale(0.9),
            Text("失效阈值", font="Microsoft YaHei", color=RED).scale(0.5)
        ).arrange(RIGHT, buff=0.1)
        threshold_label.next_to(threshold_line, LEFT, buff=0.2)
        
        self.play(Create(curve), run_time=2)
        self.play(Create(threshold_line), Write(threshold_label))
        self.wait(1)
        
        # RUL 标注
        t_current = 4.0
        D_current = degradation_curve(t_current)
        current_dot = Dot(axes.c2p(t_current, D_current), color=GREEN)
        current_label = VGroup(
            MathTex("t", color=GREEN).scale(0.8),
            Text("(当前时刻)", font="Microsoft YaHei", color=GREEN).scale(0.5)
        ).arrange(RIGHT, buff=0.1)
        current_label.next_to(current_dot, DOWN, buff=0.2)
        
        t_fail = np.log(threshold / 0.02) / 0.15
        fail_dot = Dot(axes.c2p(t_fail, threshold), color=ORANGE)
        
        rul_brace = BraceBetweenPoints(
            axes.c2p(t_current, D_current + 0.15),
            axes.c2p(t_fail, threshold + 0.15),
            direction=UP,
            color=BLUE,
        )
        rul_label = Text("RUL", font="Microsoft YaHei", color=BLUE).scale(0.6)
        rul_label.next_to(rul_brace, UP, buff=0.1)
        
        self.play(
            FadeIn(current_dot),
            Write(current_label),
            FadeIn(fail_dot),
            Create(rul_brace),
            Write(rul_label),
            run_time=1.5
        )
        self.wait(1.5)
        
        # 清理
        self.play(
            FadeOut(title), FadeOut(subtitle),
            FadeOut(axes), FadeOut(curve),
            FadeOut(threshold_line), FadeOut(threshold_label),
            FadeOut(x_label), FadeOut(y_label),
            FadeOut(current_dot), FadeOut(current_label),
            FadeOut(fail_dot), FadeOut(rul_brace), FadeOut(rul_label),
        )
        
        # ========== 场景2：RUL 数学定义 ==========
        title_math = Text("RUL 的数学定义", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_math.to_edge(UP)
        self.play(Write(title_math))
        
        # 纯数学公式
        rul_def = MathTex(
            r"\operatorname{RUL}(t) = \inf \left\{ \tau > 0 : D(t + \tau) \ge \theta \right\}",
            color=YELLOW
        ).scale(1.2)
        rul_def.move_to(DOWN * 1.5)
        self.play(Write(rul_def))
        
        # 定义说明（全部用 Text，单独排列）
        desc_items = VGroup(
            Text("t：当前时刻", font="Microsoft YaHei", color=WHITE).scale(0.7),
            Text("τ：剩余时间", font="Microsoft YaHei", color=WHITE).scale(0.7),
            Text("D(t)：退化指标", font="Microsoft YaHei", color=WHITE).scale(0.7),
            Text("θ：失效阈值", font="Microsoft YaHei", color=WHITE).scale(0.7),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        desc_items.next_to(rul_def, DOWN, buff=0.8)
        
        self.play(Write(desc_items), run_time=1.5)
        self.wait(1.5)
        
        frame = SurroundingRectangle(rul_def, color=YELLOW, buff=0.15)
        self.play(Create(frame))
        self.wait(1)
        
        self.play(
            FadeOut(title_math), FadeOut(rul_def),
            FadeOut(desc_items), FadeOut(frame),
        )
        
        # ========== 场景3：指数退化模型推导 ==========
        title_model = Text("指数退化模型", font="Microsoft YaHei", color=GREEN).scale(0.9)
        title_model.to_edge(UP)
        self.play(Write(title_model))
        
        # 退化函数
        degradation_eq = MathTex(r"D(t) = D_0 \cdot e^{\lambda t}", color=WHITE).scale(1.2)
        degradation_eq.next_to(title_model, DOWN, buff=0.8)
        
        # 参数说明：数学符号 + 中文分开
        params = VGroup(
            VGroup(MathTex(r"D_0", color=YELLOW).scale(0.9),
                   Text("：初始退化量", font="Microsoft YaHei", color=YELLOW).scale(0.6)).arrange(RIGHT, buff=0.1),
            VGroup(MathTex(r"\lambda", color=GREEN).scale(0.9),
                   Text("：退化速率", font="Microsoft YaHei", color=GREEN).scale(0.6)).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.3)
        params.next_to(degradation_eq, DOWN, buff=0.5)
        
        self.play(Write(degradation_eq), Write(params))
        self.wait(1)
        
        # 推导步骤（纯公式，无中文）
        step1 = MathTex(r"D_0 \cdot e^{\lambda (t + \operatorname{RUL})} = \theta", color=WHITE).scale(1.0)
        step1.next_to(params, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait(0.5)
        
        step2 = MathTex(r"e^{\lambda (t + \operatorname{RUL})} = \frac{\theta}{D_0}", color=WHITE).scale(1.0)
        step2.next_to(step1, DOWN, buff=0.3)
        self.play(Transform(step1, step2))
        self.wait(0.5)
        
        step3 = MathTex(r"\lambda (t + \operatorname{RUL}) = \ln\left(\frac{\theta}{D_0}\right)", color=WHITE).scale(1.0)
        step3.next_to(step2, DOWN, buff=0.3)
        self.play(Transform(step1, step3))
        self.wait(0.5)
        
        step4 = MathTex(r"\operatorname{RUL} = \frac{1}{\lambda} \ln\left(\frac{\theta}{D_0}\right) - t", color=YELLOW).scale(1.1)
        step4.next_to(step3, DOWN, buff=0.3)
        self.play(Transform(step1, step4))
        self.wait(1.5)
        
        frame2 = SurroundingRectangle(step1, color=YELLOW, buff=0.15)
        self.play(Create(frame2))
        self.wait(1)
        
        self.play(
            FadeOut(title_model), FadeOut(degradation_eq),
            FadeOut(params), FadeOut(step1), FadeOut(frame2),
        )
        
        # ========== 场景4：参数代入 ==========
        title_calc = Text("数值计算实例", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_calc.to_edge(UP)
        self.play(Write(title_calc))
        
        params_given = VGroup(
            MathTex(r"D_0 = 0.02", color=WHITE).scale(0.9),
            MathTex(r"\lambda = 0.15 \text{ /month}", color=WHITE).scale(0.9),
            MathTex(r"\theta = 1.0", color=WHITE).scale(0.9),
            MathTex(r"t = 4 \text{ months}", color=WHITE).scale(0.9),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params_given.next_to(title_calc, DOWN, buff=0.6)
        params_given.to_edge(LEFT, buff=2.0)
        
        self.play(Write(params_given))
        self.wait(1)
        
        calc1 = MathTex(r"\operatorname{RUL} = \frac{1}{0.15} \ln\left(\frac{1.0}{0.02}\right) - 4", color=GREEN).scale(0.9)
        calc1.next_to(params_given, DOWN, buff=0.6)
        
        calc2 = MathTex(r"= \frac{1}{0.15} \ln(50) - 4", color=GREEN).scale(0.9)
        calc2.next_to(calc1, DOWN, buff=0.3)
        
        calc3 = MathTex(r"= \frac{3.912}{0.15} - 4 \approx 26.08 - 4 = 22.08 \text{ months}", color=YELLOW).scale(0.9)
        calc3.next_to(calc2, DOWN, buff=0.3)
        
        self.play(Write(calc1), Write(calc2), Write(calc3))
        self.wait(1.5)
        
        conclusion = Text(
            "结论：在当前工况下，设备剩余使用寿命约为 22 个月",
            font="Microsoft YaHei", color=BLUE
        ).scale(0.7)
        conclusion.next_to(calc3, DOWN, buff=0.6)
        self.play(Write(conclusion))
        self.wait(2)
        
        self.play(
            FadeOut(title_calc), FadeOut(params_given),
            FadeOut(calc1), FadeOut(calc2), FadeOut(calc3),
            FadeOut(conclusion),
        )
        
        # ========== 场景5：不同退化速率对比 ==========
        title_compare = Text("不同退化速率 λ 的影响", font="Microsoft YaHei", color=WHITE).scale(0.9)
        title_compare.to_edge(UP)
        self.play(Write(title_compare))
        
        axes2 = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 2.5, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes2.move_to(DOWN * 0.5)
        x_label2 = Text("时间 t (月)", font="Microsoft YaHei", color=GRAY).scale(0.6)
        x_label2.next_to(axes2.x_axis, RIGHT, buff=0.1)
        y_label2 = Text("退化指标 D(t)", font="Microsoft YaHei", color=GRAY).scale(0.6)
        y_label2.next_to(axes2.y_axis, UP, buff=0.1)
        
        self.play(Create(axes2), Write(x_label2), Write(y_label2))
        
        thresh_line = DashedLine(
            start=axes2.c2p(0, 1.0),
            end=axes2.c2p(12, 1.0),
            color=RED,
            stroke_width=3,
            dash_length=0.1,
        )
        thresh_text = Text("失效阈值 θ = 1.0", font="Microsoft YaHei", color=RED).scale(0.5)
        thresh_text.next_to(thresh_line, LEFT, buff=0.2)
        self.play(Create(thresh_line), Write(thresh_text))
        
        lambdas = [0.1, 0.15, 0.2]
        colors = [GREEN, YELLOW, ORANGE]
        curves = []
        for lam, col in zip(lambdas, colors):
            curve = axes2.plot(
                lambda t: 0.02 * np.exp(lam * t),
                x_range=[0, 12],
                color=col,
                stroke_width=4,
            )
            curves.append(curve)
            self.play(Create(curve), run_time=1)
        
        legend = VGroup()
        legend_items = [
            (GREEN, "λ = 0.1 (慢速退化)"),
            (YELLOW, "λ = 0.15 (中速退化)"),
            (ORANGE, "λ = 0.2 (快速退化)"),
        ]
        for col, lab in legend_items:
            item = VGroup(
                Dot(color=col),
                Text(lab, font="Microsoft YaHei", color=col).scale(0.45)
            ).arrange(RIGHT, buff=0.1)
            legend.add(item)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(UR, buff=0.5)
        self.play(Write(legend))
        self.wait(2)
        
        final_text = Text(
            "RUL 模型是预测性维护的基石，帮助工程师提前安排维修计划",
            font="Microsoft YaHei", color=BLUE
        ).scale(0.65)
        final_text.to_edge(DOWN, buff=0.5)
        self.play(Write(final_text))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)