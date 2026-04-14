from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30


class MassSpringDamper(Scene):
    """
    机械自动化最核心模型：弹簧-质量-阻尼系统
    包含完整的数学推导、代入过程和可视化演示
    """
    
    def construct(self):
        # 设置背景色为深色（类似3b1b风格）
        self.camera.background_color = "#1e1e1e"
        
        # ========== 场景1：物理系统展示 ==========
        title = Text("机械自动化的核心数学模型", font="Microsoft YaHei", color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        subtitle = Text("弹簧-质量-阻尼系统 (Mass-Spring-Damper System)", 
                        font="Microsoft YaHei", color=WHITE).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle))
        self.wait(0.5)
        
        # 绘制物理系统示意图
        wall = Rectangle(height=2.0, width=0.3, color=GRAY, fill_opacity=0.8)
        wall.move_to(LEFT * 4)
        
        # 弹簧（锯齿形）
        spring = self.create_spring(start=LEFT * 3.7, end=LEFT * 1.5, num_coils=10)
        
        # 质量块
        mass = Rectangle(height=1.2, width=1.2, color=BLUE, fill_opacity=0.7)
        mass.move_to(RIGHT * 1)
        mass_label = MathTex("m", color=WHITE).scale(1.2)
        mass_label.move_to(mass.get_center())
        
        # 阻尼器（活塞符号）
        damper = self.create_damper(start=RIGHT * 1.6, end=RIGHT * 3.0)
        
        # 坐标标注
        x_axis = Line(start=LEFT * 3, end=RIGHT * 4, color=GRAY)
        x_axis.next_to(mass, DOWN, buff=1.0)
        x_label = MathTex("x", color=WHITE).next_to(x_axis, RIGHT)
        origin_label = MathTex("0", color=GRAY).next_to(x_axis.get_start(), DOWN, buff=0.2)
        
        # 位移标注 x(t)
        x_brace = Brace(mass, DOWN, color=YELLOW)
        x_text = MathTex("x(t)", color=YELLOW).next_to(x_brace, DOWN, buff=0.2)
        
        # 力标注
        F_arrow = Arrow(start=mass.get_right(), end=mass.get_right() + RIGHT * 1.2, 
                        color=RED, buff=0)
        F_label = MathTex("F(t)", color=RED).next_to(F_arrow, RIGHT, buff=0.2)
        
        # 动画展示
        self.play(
            Create(wall),
            Create(spring),
            Create(mass),
            Write(mass_label),
            Create(damper),
            Create(x_axis),
            Write(x_label),
            Write(origin_label),
            Create(x_brace),
            Write(x_text),
            GrowArrow(F_arrow),
            Write(F_label),
            run_time=2
        )
        
        # 物理量说明 —— 修正：数学部分用MathTex，中文说明用Text
        params = VGroup()
        param_data = [
            ("m", "— 质量"),
            ("k", "— 弹簧刚度"),
            ("c", "— 阻尼系数"),
            ("x(t)", "— 位移响应"),
        ]
        for math_expr, chinese_desc in param_data:
            line = VGroup(
                MathTex(math_expr, color=WHITE),
                Text(chinese_desc, font="Microsoft YaHei", color=WHITE)
            ).arrange(RIGHT, buff=0.1)
            line.scale(0.7)
            params.add(line)
        
        params.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params.to_corner(DR, buff=0.5)
        
        self.play(Write(params), run_time=1.5)
        self.wait(1)
        
        # 清理场景1的辅助元素（保留主要系统图）
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(params),
            FadeOut(F_arrow),
            FadeOut(F_label),
            FadeOut(x_brace),
            FadeOut(x_text),
        )
        self.wait(0.5)
        
        # ========== 场景2：牛顿第二定律推导 ==========
        # 移动系统图到左侧
        system_group = VGroup(wall, spring, mass, mass_label, damper, x_axis, x_label, origin_label)
        self.play(system_group.animate.scale(0.7).to_edge(LEFT, buff=1.0))
        
        # 右侧显示推导
        title_derive = Text("动力学方程推导", font="Microsoft YaHei", color=GREEN).scale(0.8)
        title_derive.to_edge(UP, buff=0.5)
        self.play(Write(title_derive))
        
        # 牛顿第二定律
        eq1 = MathTex(r"F = m \cdot a", color=YELLOW).scale(1.2)
        eq1.next_to(title_derive, DOWN, buff=0.8)
        eq1.to_edge(RIGHT, buff=1.5)
        self.play(Write(eq1))
        self.wait(0.5)
        
        # 加速度 = 位移的二阶导数
        eq2 = MathTex(r"a = \frac{d^2x}{dt^2} = \ddot{x}", color=WHITE).scale(1.0)
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        
        # 受力分析
        eq3 = MathTex(
            r"m\ddot{x} = F(t) - kx - c\dot{x}",
            color=WHITE
        ).scale(1.0)
        eq3.next_to(eq2, DOWN, buff=0.5)
        
        # 高亮各个力 —— 修正：分开处理
        force_desc = VGroup()
        force_data = [
            (r"-kx", ORANGE, "弹簧恢复力"),
            (r"-c\dot{x}", TEAL, "阻尼力"),
            (r"F(t)", RED, "外力"),
        ]
        for math_expr, col, chinese_desc in force_data:
            line = VGroup(
                MathTex(math_expr, color=col).scale(0.9),
                Text(chinese_desc, font="Microsoft YaHei", color=col).scale(0.5)
            ).arrange(DOWN, buff=0.15)
            force_desc.add(line)
        force_desc.arrange(RIGHT, buff=0.3)
        force_desc.next_to(eq3, DOWN, buff=0.5)
        
        self.play(Write(eq3))
        self.play(Write(force_desc))
        self.wait(1.5)
        
        # ========== 场景3：标准形式整理 ==========
        # 清理之前的部分推导
        self.play(
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(force_desc),
        )
        
        # 移项整理
        eq4 = MathTex(r"m\ddot{x} + c\dot{x} + kx = F(t)", color=YELLOW).scale(1.2)
        eq4.next_to(title_derive, DOWN, buff=0.8)
        eq4.to_edge(RIGHT, buff=1.5)
        self.play(Transform(eq3, eq4))
        self.wait(1)
        
        # 除以 m
        eq5 = MathTex(r"\ddot{x} + \frac{c}{m}\dot{x} + \frac{k}{m}x = \frac{F(t)}{m}", 
                      color=WHITE).scale(1.0)
        eq5.next_to(eq3, DOWN, buff=0.6)
        self.play(Write(eq5))
        self.wait(1)
        
        # 引入固有频率和阻尼比 —— 修正：中文说明用Text
        intro_text = Text("引入两个关键参数", font="Microsoft YaHei", color=BLUE).scale(0.7)
        intro_text.next_to(eq5, DOWN, buff=0.6)
        self.play(Write(intro_text))
        
        # omega_0 定义：公式 + 中文
        omega_line = VGroup(
            MathTex(r"\omega_0 = \sqrt{\frac{k}{m}}", color=GREEN),
            Text("(固有频率)", font="Microsoft YaHei", color=GREEN)
        ).arrange(RIGHT, buff=0.15).scale(0.9)
        omega_line.next_to(intro_text, DOWN, buff=0.3)
        
        # zeta 定义：公式 + 中文
        zeta_line = VGroup(
            MathTex(r"\zeta = \frac{c}{2\sqrt{mk}}", color=PURPLE),
            Text("(阻尼比)", font="Microsoft YaHei", color=PURPLE)
        ).arrange(RIGHT, buff=0.15).scale(0.9)
        zeta_line.next_to(omega_line, DOWN, buff=0.2)
        
        self.play(Write(omega_line), Write(zeta_line))
        self.wait(1.5)
        
        # 标准形式
        eq6 = MathTex(r"\ddot{x} + 2\zeta\omega_0\dot{x} + \omega_0^2 x = \frac{F(t)}{m}", 
                      color=YELLOW).scale(1.0)
        eq6.next_to(zeta_line, DOWN, buff=0.5)
        
        self.play(Write(eq6))
        self.wait(1)
        
        # 画框强调
        frame = SurroundingRectangle(eq6, color=YELLOW, buff=0.15)
        self.play(Create(frame))
        self.wait(1.5)
        
        # ========== 场景4：参数代入 ==========
        # 清理场景
        self.play(
            FadeOut(title_derive),
            FadeOut(eq3),
            FadeOut(eq5),
            FadeOut(intro_text),
            FadeOut(omega_line),
            FadeOut(zeta_line),
            FadeOut(eq6),
            FadeOut(frame),
        )
        
        title_calc = Text("数值计算实例", font="Microsoft YaHei", color=BLUE).scale(0.9)
        title_calc.to_edge(UP, buff=0.5)
        self.play(Write(title_calc))
        
        # 给定参数 —— 无中文，直接用MathTex
        params_given = VGroup(
            MathTex(r"m = 10 \text{ kg}", color=WHITE).scale(0.9),
            MathTex(r"k = 1000 \text{ N/m}", color=WHITE).scale(0.9),
            MathTex(r"c = 40 \text{ N·s/m}", color=WHITE).scale(0.9),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        params_given.next_to(title_calc, DOWN, buff=0.6)
        params_given.to_edge(RIGHT, buff=1.5)
        
        self.play(Write(params_given))
        self.wait(1)
        
        # 计算过程（纯公式）
        calc1 = MathTex(r"\omega_0 = \sqrt{\frac{1000}{10}} = \sqrt{100} = 10 \text{ rad/s}", 
                        color=GREEN).scale(0.9)
        calc1.next_to(params_given, DOWN, buff=0.5)
        
        calc2 = MathTex(r"\zeta = \frac{40}{2\sqrt{10 \cdot 1000}} = \frac{40}{2 \cdot 100} = 0.2", 
                        color=PURPLE).scale(0.9)
        calc2.next_to(calc1, DOWN, buff=0.3)
        
        self.play(Write(calc1))
        self.wait(0.5)
        self.play(Write(calc2))
        self.wait(1)
        
        # 阻尼类型判断（纯中文，用Text）
        zeta_value = 0.2
        if zeta_value < 1:
            damping_type = "欠阻尼 (0 < ζ < 1)"
            type_color = GREEN
        elif zeta_value == 1:
            damping_type = "临界阻尼 (ζ = 1)"
            type_color = YELLOW
        else:
            damping_type = "过阻尼 (ζ > 1)"
            type_color = RED
            
        result_text = Text(f"ζ = 0.2 → {damping_type}", 
                          font="Microsoft YaHei", color=type_color).scale(0.8)
        result_text.next_to(calc2, DOWN, buff=0.5)
        
        self.play(Write(result_text))
        self.wait(1.5)
        
        # ========== 场景5：阻尼类型对比可视化 ==========
        # 清理左侧系统图
        self.play(FadeOut(system_group))
        
        # 清理计算内容
        self.play(
            FadeOut(params_given),
            FadeOut(calc1),
            FadeOut(calc2),
            FadeOut(result_text),
            FadeOut(title_calc),
        )
        
        # 绘制三种阻尼的响应曲线
        title_curves = Text("三种阻尼类型的响应曲线", font="Microsoft YaHei", color=WHITE).scale(0.9)
        title_curves.to_edge(UP, buff=0.5)
        self.play(Write(title_curves))
        
        # 创建坐标系
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
            x_axis_config={"numbers_to_include": np.arange(0, 6, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1.5, 2, 0.5)},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)
        
        x_label = axes.get_x_axis_label(MathTex("t"), edge=RIGHT, buff=0.2)
        y_label = axes.get_y_axis_label(MathTex("x(t)"), edge=UP, buff=0.2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # 欠阻尼响应 (ζ=0.2)
        def underdamped_response(t):
            omega_0 = 10
            zeta = 0.2
            omega_d = omega_0 * np.sqrt(1 - zeta**2)
            return np.exp(-zeta * omega_0 * t) * np.cos(omega_d * t)
        
        underdamped_graph = axes.plot(
            underdamped_response,
            x_range=[0, 5],
            color=GREEN,
            stroke_width=3,
        )
        
        # 临界阻尼响应 (ζ=1)
        def critical_response(t):
            omega_0 = 10
            return np.exp(-omega_0 * t) * (1 + omega_0 * t)
        
        critical_graph = axes.plot(
            critical_response,
            x_range=[0, 5],
            color=YELLOW,
            stroke_width=3,
        )
        
        # 过阻尼响应 (ζ=2.0)
        def overdamped_response(t):
            omega_0 = 10
            zeta = 2.0
            s1 = -omega_0 * (zeta - np.sqrt(zeta**2 - 1))
            s2 = -omega_0 * (zeta + np.sqrt(zeta**2 - 1))
            A1 = s2 / (s2 - s1)
            A2 = -s1 / (s2 - s1)
            return A1 * np.exp(s1 * t) + A2 * np.exp(s2 * t)
        
        overdamped_graph = axes.plot(
            overdamped_response,
            x_range=[0, 5],
            color=RED,
            stroke_width=3,
        )
        
        # 图例 —— 修正：用Text写中文部分
        legend_items = [
            (GREEN, "欠阻尼 (ζ=0.2)"),
            (YELLOW, "临界阻尼 (ζ=1)"),
            (RED, "过阻尼 (ζ=2)"),
        ]
        legend = VGroup()
        for color, label in legend_items:
            item = VGroup(
                Dot(color=color),
                Text(label, font="Microsoft YaHei", color=color).scale(0.5)
            ).arrange(RIGHT, buff=0.1)
            legend.add(item)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(UR, buff=0.5)
        
        # 依次显示三种响应
        self.play(Create(underdamped_graph), run_time=1.5)
        self.play(Write(legend[0]))
        self.wait(0.5)
        
        self.play(Create(critical_graph), run_time=1.5)
        self.play(Write(legend[1]))
        self.wait(0.5)
        
        self.play(Create(overdamped_graph), run_time=1.5)
        self.play(Write(legend[2]))
        self.wait(1)
        
        # 最终总结
        self.play(FadeOut(legend))
        
        conclusion = Text(
            "弹簧-质量-阻尼系统是理解机械自动化动态行为的基础模型",
            font="Microsoft YaHei", color=BLUE
        ).scale(0.7)
        conclusion.to_edge(DOWN, buff=0.8)
        
        self.play(Write(conclusion))
        self.wait(2)
        
        # 淡出结束
        self.play(FadeOut(axes), FadeOut(underdamped_graph), FadeOut(critical_graph), 
                  FadeOut(overdamped_graph), FadeOut(x_label), FadeOut(y_label),
                  FadeOut(title_curves), FadeOut(conclusion))
        self.wait(0.5)
        
    def create_spring(self, start, end, num_coils=10):
        """创建锯齿形弹簧"""
        direction = end - start
        length = np.linalg.norm(direction)
        unit = direction / length
        
        perp = np.array([-unit[1], unit[0], 0])
        
        points = [start]
        segment_length = length / num_coils
        
        for i in range(1, num_coils):
            t = i / num_coils
            point = start + t * direction
            
            if i % 2 == 1:
                point += perp * 0.15
            else:
                point -= perp * 0.15
            points.append(point)
        
        points.append(end)
        
        spring = VMobject(color=GRAY, stroke_width=4)
        spring.set_points_smoothly(points)
        
        return spring
    
    def create_damper(self, start, end):
        """创建阻尼器符号（活塞）"""
        direction = end - start
        length = np.linalg.norm(direction)
        unit = direction / length
        perp = np.array([-unit[1], unit[0], 0])
        
        # 缸体
        cylinder_center = start + direction * 0.3
        cylinder = Rectangle(
            height=0.5, width=0.8, color=GRAY, fill_opacity=0.3
        ).move_to(cylinder_center)
        
        # 活塞杆
        piston_rod = Line(
            start=cylinder.get_right(),
            end=cylinder.get_right() + direction * 0.5,
            color=GRAY,
            stroke_width=4
        )
        
        # 连接点
        mount_left = Line(start - perp * 0.2, start + perp * 0.2, color=GRAY, stroke_width=6)
        mount_right = Line(end - perp * 0.2, end + perp * 0.2, color=GRAY, stroke_width=6)
        
        damper = VGroup(cylinder, piston_rod, mount_left, mount_right)
        return damper