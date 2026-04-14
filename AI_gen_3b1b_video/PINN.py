from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30


class PhysicsInformedNN(Scene):
    """
    数字孪生关键技术：物理信息神经网络（PINN）
    包含数学框架、PDE案例、训练对比与应用
    """
    
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== 场景1：数字孪生与PINN引入 ==========
        title = Text("数字孪生的核心技术", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title.to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text("PINN — Physics-Informed Neural Network", font="Microsoft YaHei", color=WHITE).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        # 物理世界 vs 数字世界
        physical = Rectangle(height=2.0, width=3.0, color=GREEN, fill_opacity=0.2)
        physical.move_to(LEFT * 3.5)
        physical_label = Text("物理世界", font="Microsoft YaHei", color=GREEN).scale(0.7)
        physical_label.next_to(physical, UP, buff=0.2)
        
        digital = Rectangle(height=2.0, width=3.0, color=BLUE, fill_opacity=0.2)
        digital.move_to(RIGHT * 3.5)
        digital_label = Text("数字世界", font="Microsoft YaHei", color=BLUE).scale(0.7)
        digital_label.next_to(digital, UP, buff=0.2)
        
        arrow1 = DoubleArrow(
            start=physical.get_right(),
            end=digital.get_left(),
            color=YELLOW,
        )
        arrow_label = Text("实时双向映射", font="Microsoft YaHei", color=YELLOW).scale(0.5)
        arrow_label.move_to(ORIGIN)
        
        self.play(
            Create(physical), Write(physical_label),
            Create(digital), Write(digital_label),
            Create(arrow1), Write(arrow_label),
            run_time=2
        )
        
        # PINN 核心思想
        pinn_idea = Text(
            "PINN：将物理定律（PDE）嵌入神经网络训练过程",
            font="Microsoft YaHei", color=ORANGE
        ).scale(0.6)
        pinn_idea.next_to(physical, DOWN, buff=0.8)
        pinn_idea.to_edge(DOWN, buff=0.5)
        
        self.play(Write(pinn_idea))
        self.wait(2)
        
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(physical), FadeOut(physical_label),
            FadeOut(digital), FadeOut(digital_label),
            FadeOut(arrow1), FadeOut(arrow_label),
            FadeOut(pinn_idea),
        )
        
        # ========== 场景2：PINN 数学框架 ==========
        title_math = Text("PINN 数学框架", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_math.to_edge(UP)
        self.play(Write(title_math))
        
        # 网络架构
        network = VGroup()
        layers = [3, 5, 5, 5, 1]
        for i, n in enumerate(layers):
            x = LEFT * 4 + RIGHT * i * 2
            for j in range(n):
                y = DOWN * 1 + UP * j * 0.5
                circle = Circle(radius=0.15, color=BLUE, fill_opacity=0.5)
                circle.move_to([x[0], y[1], 0])
                network.add(circle)
        
        network.scale(0.6)
        network.move_to(LEFT * 2)
        network_label = Text("神经网络", font="Microsoft YaHei", color=BLUE).scale(0.5)
        network_label.next_to(network, DOWN, buff=0.2)
        
        self.play(Create(network), Write(network_label))
        
        # 损失函数
        loss_title = Text("损失函数构成", font="Microsoft YaHei", color=YELLOW).scale(0.6)
        loss_title.next_to(network, RIGHT, buff=1.5)
        loss_title.to_edge(UP, buff=1.5)
        
        loss_eq = MathTex(
            r"\mathcal{L} = \mathcal{L}_{\text{data}} + \mathcal{L}_{\text{PDE}} + \mathcal{L}_{\text{BC}}",
            color=YELLOW
        ).scale(0.9)
        loss_eq.next_to(loss_title, DOWN, buff=0.3)
        
        data_loss = MathTex(
            r"\mathcal{L}_{\text{data}} = \frac{1}{N_d}\sum_{i=1}^{N_d} |u_{\theta}(x_i) - u_i|^2",
            color=GREEN
        ).scale(0.7)
        data_loss.next_to(loss_eq, DOWN, buff=0.3)
        
        pde_loss = MathTex(
            r"\mathcal{L}_{\text{PDE}} = \frac{1}{N_p}\sum_{i=1}^{N_p} |\mathcal{N}[u_{\theta}](x_i)|^2",
            color=ORANGE
        ).scale(0.7)
        pde_loss.next_to(data_loss, DOWN, buff=0.2)
        
        bc_loss = MathTex(
            r"\mathcal{L}_{\text{BC}} = \frac{1}{N_b}\sum_{i=1}^{N_b} |\mathcal{B}[u_{\theta}](x_i)|^2",
            color=RED
        ).scale(0.7)
        bc_loss.next_to(pde_loss, DOWN, buff=0.2)
        
        self.play(
            Write(loss_title),
            Write(loss_eq),
            run_time=1
        )
        self.play(Write(data_loss), run_time=0.8)
        self.play(Write(pde_loss), run_time=0.8)
        self.play(Write(bc_loss), run_time=0.8)
        
        # 说明
        explain = VGroup(
            Text("ℒ_data：数据匹配项", font="Microsoft YaHei", color=GREEN).scale(0.45),
            Text("ℒ_PDE：方程残差项", font="Microsoft YaHei", color=ORANGE).scale(0.45),
            Text("ℒ_BC：边界条件项", font="Microsoft YaHei", color=RED).scale(0.45),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        explain.next_to(bc_loss, DOWN, buff=0.4)
        
        self.play(Write(explain))
        self.wait(2)
        
        self.play(
            FadeOut(title_math),
            FadeOut(network), FadeOut(network_label),
            FadeOut(loss_title), FadeOut(loss_eq),
            FadeOut(data_loss), FadeOut(pde_loss),
            FadeOut(bc_loss), FadeOut(explain),
        )
        
        # ========== 场景3：一维热传导方程案例 ==========
        title_heat = Text("案例：一维热传导方程", font="Microsoft YaHei", color=GREEN).scale(0.9)
        title_heat.to_edge(UP)
        self.play(Write(title_heat))
        
        # 热传导方程
        heat_eq = MathTex(
            r"\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}",
            color=YELLOW
        ).scale(1.2)
        heat_eq.move_to(UP * 1)
        self.play(Write(heat_eq))
        
        params = VGroup(
            MathTex(r"u(x,t)", color=WHITE).scale(0.9),
            Text("：温度分布", font="Microsoft YaHei", color=WHITE).scale(0.6),
            MathTex(r"\alpha", color=BLUE).scale(0.9),
            Text("：热扩散系数", font="Microsoft YaHei", color=BLUE).scale(0.6),
        ).arrange(RIGHT, buff=0.15)
        params.next_to(heat_eq, DOWN, buff=0.4)
        
        self.play(Write(params))
        
        # 边界条件
        bc = MathTex(
            r"u(0,t) = 0, \quad u(L,t) = 0",
            color=RED
        ).scale(0.9)
        bc.next_to(params, DOWN, buff=0.5)
        
        ic = MathTex(
            r"u(x,0) = \sin\left(\frac{\pi x}{L}\right)",
            color=GREEN
        ).scale(0.9)
        ic.next_to(bc, DOWN, buff=0.3)
        
        self.play(Write(bc), Write(ic))
        self.wait(1.5)
        
        # 解析解
        analytic = MathTex(
            r"u(x,t) = \sin\left(\frac{\pi x}{L}\right) e^{-\alpha \pi^2 t / L^2}",
            color=PURPLE
        ).scale(0.9)
        analytic.next_to(ic, DOWN, buff=0.5)
        
        analytic_label = Text("解析解", font="Microsoft YaHei", color=PURPLE).scale(0.5)
        analytic_label.next_to(analytic, LEFT, buff=0.2)
        
        self.play(Write(analytic), Write(analytic_label))
        self.wait(2)
        
        self.play(
            FadeOut(title_heat),
            FadeOut(heat_eq), FadeOut(params),
            FadeOut(bc), FadeOut(ic),
            FadeOut(analytic), FadeOut(analytic_label),
        )
        
        # ========== 场景4：训练结果对比 ==========
        title_compare = Text("PINN vs 传统数值方法", font="Microsoft YaHei", color=WHITE).scale(0.9)
        title_compare.to_edge(UP)
        self.play(Write(title_compare))
        
        # 绘制对比曲线
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=3.5,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)
        x_label = Text("x / L", font="Microsoft YaHei", color=GRAY).scale(0.6)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("u(x, t)", font="Microsoft YaHei", color=GRAY).scale(0.6)
        y_label.next_to(axes.y_axis, UP, buff=0.1)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # 解析解曲线（参考基准）
        def exact_solution(x, t=0.1, alpha=1.0, L=1.0):
            return np.sin(np.pi * x) * np.exp(-alpha * np.pi**2 * t / L**2)
        
        exact_curve = axes.plot(
            lambda x: exact_solution(x),
            x_range=[0, 1],
            color=WHITE,
            stroke_width=3,
        )
        exact_label = Text("解析解 (基准)", font="Microsoft YaHei", color=WHITE).scale(0.5)
        exact_label.next_to(exact_curve, UP, buff=0.1)
        
        self.play(Create(exact_curve), Write(exact_label))
        self.wait(0.5)
        
        # PINN 预测曲线（模拟）
        def pinn_prediction(x, t=0.1):
            return exact_solution(x) + 0.03 * np.sin(3 * np.pi * x) * np.exp(-2 * t)
        
        pinn_curve = axes.plot(
            lambda x: pinn_prediction(x),
            x_range=[0, 1],
            color=GREEN,
            stroke_width=3,
        )
        pinn_label = Text("PINN 预测", font="Microsoft YaHei", color=GREEN).scale(0.5)
        pinn_label.next_to(pinn_curve, DOWN, buff=0.2)
        
        self.play(Create(pinn_curve), Write(pinn_label))
        
        # 误差比较
        error_text = MathTex(
            r"\text{均方误差} = 2.3 \times 10^{-4}",
            color=ORANGE
        ).scale(0.8)
        error_text.to_corner(UR, buff=0.8)
        
        self.play(Write(error_text))
        self.wait(2)
        
        self.play(
            FadeOut(title_compare),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(exact_curve), FadeOut(exact_label),
            FadeOut(pinn_curve), FadeOut(pinn_label),
            FadeOut(error_text),
        )
        
        # ========== 场景5：数字孪生应用 ==========
        title_app = Text("PINN 在数字孪生中的应用", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_app.to_edge(UP)
        self.play(Write(title_app))
        
        apps = VGroup(
            Text("• 实时仿真：替代耗时的传统CFD/FEM计算", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("• 参数反演：从传感器数据推断未知物理参数", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("• 多保真融合：整合不同精度层级的仿真数据", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("• 不确定性量化：评估预测结果的置信区间", font="Microsoft YaHei", color=WHITE).scale(0.6),
            Text("• 异常检测：基于物理规律的偏差识别", font="Microsoft YaHei", color=WHITE).scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        apps.move_to(ORIGIN)
        
        self.play(Write(apps), run_time=2.5)
        
        # 结论
        conclusion = Text(
            "PINN 将物理知识与数据驱动相结合，为数字孪生提供更可靠的建模方法",
            font="Microsoft YaHei", color=YELLOW
        ).scale(0.65)
        conclusion.to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(3)
        
        self.play(
            FadeOut(title_app),
            FadeOut(apps),
            FadeOut(conclusion),
        )
        self.wait(0.5)