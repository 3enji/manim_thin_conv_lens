from manim import *


# manim -pql updators_example_for_cameron.py
# https://eertmans.be/posts/eucap-presentation/
# BE note (07/08/2023 @ 22:36)
# https://slama.dev/manim/groups-transformations-updaters/
# https://docs.devtaoism.com/docs/html/contents/_14_basic_updaters.html
# https://docs.manim.community/en/stable/reference/manim.animation.creation.ShowIncreasingSubsets.html
# https://docs.manim.community/en/stable/examples.html
# https://3b1b.github.io/manim/getting_started/example_scenes.html (different version)
# https://www.google.com/search?client=firefox-b-d&q=manim+plotting+graphs#fpstate=ive&vld=cid:3294879b,vid:jFqYq9quBds,st:0


def plot_ray(): ...


def get_coords_F(h, f, ylim=-3, xlim=-6):
    y = ylim
    start_coord = [0, h]
    f_dash_coord = [f, 0]
    m = (start_coord[1] - f_dash_coord[1]) / (start_coord[0] - f_dash_coord[0])
    if m == 0:
        x = xlim
        y = start_coord[1]
        return [x, y]
    elif m > 0:
        y = ylim
    elif m < 0:
        y = -ylim

    x = start_coord[0] + (y - start_coord[1]) / m
    if not (xlim <= x <= -xlim):
        x = xlim
        y = (m * x) + start_coord[1]

    return [x, y]


def get_coords_F_dash(h, f_dash, ylim=3, xlim=6, x_or_y="both"):
    y = ylim
    start_coord = [0, h]
    f_dash_coord = [f_dash, 0]
    m = (start_coord[1] - f_dash_coord[1]) / (start_coord[0] - f_dash_coord[0])
    if m == 0:
        x = xlim
        y = start_coord[1]
        return [x, y]
    elif m > 0:
        y = ylim
    elif m < 0:
        y = -ylim

    x = start_coord[0] + (y - start_coord[1]) / m
    if not (-xlim <= x <= xlim):
        x = xlim
        y = (m * x) + start_coord[1]

    if x_or_y == "both":
        return [x, y]
    elif x_or_y == "x":
        return x
    elif x_or_y == "y":
        return y


class DrawConvergingLensFocalPoints(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        focal_len = 2
        # Create axes
        axes = Axes(
            x_range=(-6, 6, 1),
            y_range=(-3, 3, 1),
            x_length=12,
            y_length=6,
            axis_config={"color": WHITE},
            x_axis_config={
                "include_ticks": False,
                "include_tip": False,
            },
            y_axis_config={
                "include_ticks": False,
                "include_tip": False,
            },
        )

        # Create faint grid
        x_lines = VGroup(
            *[
                DashedLine(
                    axes.c2p(x, -3),
                    axes.c2p(x, 3),
                    dash_length=0.05,
                    color=GRAY,
                    stroke_opacity=0.3,
                )
                for x in range(-5, 6)
            ]
        )
        y_lines = VGroup(
            *[
                DashedLine(
                    axes.c2p(-6, y),
                    axes.c2p(6, y),
                    dash_length=0.1,
                    color=GRAY,
                    stroke_opacity=0.3,
                )
                for y in range(-2, 3)
            ]
        )

        # Add axes and grid to the scene
        # self.add(axes, x_lines, y_lines)
        self.add(x_lines, y_lines)
        # self.play(Create(axes))
        self.wait()
        # Draw principal axis
        # principal_axis = Line(start=axes.c2p(-6, 0), end=axes.c2p(6, 0), color=BLUE

        principal_axis = DashedLine(
            start=axes.c2p(-6, 0), end=axes.c2p(6, 0), color=BLUE
        )

        self.play(Create(principal_axis))
        self.wait()
        # Draw lens
        lens = Line(start=axes.c2p(0, -3), end=axes.c2p(0, 3), color=YELLOW)
        lens_braces = Brace(lens, UP, buff=SMALL_BUFF)
        lens_label_intro = lens_braces.get_text("Thin Lens", buff=SMALL_BUFF)
        lens_label = lens_braces.get_text("Thin Converging Lens", buff=SMALL_BUFF)
        # self.play(Create(lens), Create(lens_braces), Write(lens_label))

        # Add hollow arrows to each end of the lens
        bottom_arrow_left = Line(
            start=axes.c2p(-0.2, -2.8),
            end=axes.c2p(0, -3),
            color=YELLOW,
            fill_opacity=0,
        )
        bottom_arrow_right = Line(
            start=axes.c2p(0.2, -2.8),
            end=axes.c2p(0, -3),
            color=YELLOW,
            fill_opacity=0,
        )

        top_arrow_left = Line(
            start=axes.c2p(0.2, 2.8),
            end=axes.c2p(0, 3),
            color=YELLOW,
            fill_opacity=0,
        )
        top_arrow_right = Line(
            start=axes.c2p(-0.2, 2.8),
            end=axes.c2p(0, 3),
            color=YELLOW,
            fill_opacity=0,
        )
        self.play(
            Create(lens),
            Create(lens_braces),
            Write(lens_label_intro),
        )
        self.wait()
        self.play(
            # Write(lens_label),
            Create(bottom_arrow_left),
            Create(bottom_arrow_right),
            Create(top_arrow_left),
            Create(top_arrow_right),
        )
        self.wait(0.3)
        self.play(ReplacementTransform(lens_label_intro, lens_label))
        self.wait()

        # Draw focal points
        focal1 = Dot(axes.c2p(-focal_len, 0), color=RED)
        focal1_label = MathTex("F").next_to(focal1, DOWN)

        # plot rays for the first focal point
        # self.next_section()

        x_coord_start = -6
        x_coord_end = 6
        height_list = [-2, -1, 0, 1, 2]
        lines_F = []
        for height in height_list:
            start_pos = get_coords_F(h=height, f=-focal_len)
            ray_start = Line(
                start=axes.c2p(start_pos[0], start_pos[1]),
                end=axes.c2p(0, height),
                color=WHITE,
                fill_opacity=0,
                buff=0,
            )
            ray_end = Line(
                start=axes.c2p(0, height),
                end=axes.c2p(x_coord_end, height),
                color=WHITE,
                fill_opacity=0,
                buff=0,
            )
            lines_F.append(ray_start)
            lines_F.append(ray_end)
            # self.play(Create(ray_start))
            # self.play(Create(ray_end))

        group_F = VGroup(*lines_F)

        # self.play(ShowIncreasingSubsets(group, run_time=3.0))
        self.play(Create(group_F), run_time=12.0)

        self.play(Create(focal1), Write(focal1_label))
        self.wait(8)

        # self.remove(group_F)
        self.play(Uncreate(group_F), run_time=3.0)

        self.wait()
        # plot rays for the second focal point
        # self.next_section(skip_animations=True)
        # self.next_section()

        x_coord_start = -5
        lines_F_dash = []
        # # LOOP functionality (better, but starting manually w. updaters)
        # for height in height_list:
        #     ray_start = Line(
        #         start=axes.c2p(x_coord_start, height),
        #         end=axes.c2p(0, height),
        #         color=WHITE,
        #         fill_opacity=0,
        #         buff=0,
        #     )
        #     end_pos = get_coords_F_dash(h=height, f_dash=focal_len)
        #     ray_end = Line(
        #         start=axes.c2p(0, height),
        #         end=axes.c2p(end_pos[0], end_pos[1]),
        #         color=WHITE,
        #         fill_opacity=0,
        #         buff=0,
        #     )
        #     lines_F_dash.append(ray_start)
        #     lines_F_dash.append(ray_end)
        #     # self.play(Create(ray_start))
        #     # self.play(Create(ray_end))

        # # Manually loading each ray - this is the worse code I have ever produced
        # # pls minimal judgement. Made this way for Health's got Talent video under
        # # time constraints
        height_1 = height_list[0]
        ray_start_1 = Line(
            start=axes.c2p(x_coord_start, height_1),
            end=axes.c2p(0, height_1),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        end_pos_1 = get_coords_F_dash(h=height_1, f_dash=focal_len)
        ray_end_1 = Line(
            start=axes.c2p(0, height_1),
            end=axes.c2p(end_pos_1[0], end_pos_1[1]),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        lines_F_dash.append(ray_start_1)
        lines_F_dash.append(ray_end_1)
        height_2 = height_list[1]
        ray_start_2 = Line(
            start=axes.c2p(x_coord_start, height_2),
            end=axes.c2p(0, height_2),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        end_pos_2 = get_coords_F_dash(h=height_2, f_dash=focal_len)
        ray_end_2 = Line(
            start=axes.c2p(0, height_2),
            end=axes.c2p(end_pos_2[0], end_pos_2[1]),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        lines_F_dash.append(ray_start_2)
        lines_F_dash.append(ray_end_2)
        height_3 = height_list[2]
        ray_start_3 = Line(
            start=axes.c2p(x_coord_start, height_3),
            end=axes.c2p(0, height_3),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        end_pos_3 = get_coords_F_dash(h=height_3, f_dash=focal_len)
        ray_end_3 = Line(
            start=axes.c2p(0, height_3),
            end=axes.c2p(end_pos_3[0], end_pos_3[1]),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        lines_F_dash.append(ray_start_3)
        lines_F_dash.append(ray_end_3)
        height_4 = height_list[3]
        ray_start_4 = Line(
            start=axes.c2p(x_coord_start, height_4),
            end=axes.c2p(0, height_4),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        end_pos_4 = get_coords_F_dash(h=height_4, f_dash=focal_len)
        ray_end_4 = Line(
            start=axes.c2p(0, height_4),
            end=axes.c2p(end_pos_4[0], end_pos_4[1]),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        lines_F_dash.append(ray_start_4)
        lines_F_dash.append(ray_end_4)
        height_5 = height_list[4]
        ray_start_5 = Line(
            start=axes.c2p(x_coord_start, height_5),
            end=axes.c2p(0, height_5),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        end_pos_5 = get_coords_F_dash(h=height_5, f_dash=focal_len)
        ray_end_5 = Line(
            start=axes.c2p(0, height_5),
            end=axes.c2p(end_pos_5[0], end_pos_5[1]),
            color=WHITE,
            fill_opacity=0,
            buff=0,
        )
        lines_F_dash.append(ray_start_5)
        lines_F_dash.append(ray_end_5)
        # lines_F_dash = [ray_start_1, ray_end_1, ray_start_2, ray_end_2, ...]

        group_F_dash = VGroup(*lines_F_dash)
        self.play(Create(group_F_dash), run_time=12.0)

        self.wait()

        # SECTION adding updators
        # self.next_section(skip_animations=True)

        focal2 = Dot(axes.c2p(focal_len, 0), color=RED)
        focal2_label = MathTex("F'").next_to(focal2, DOWN)

        # focal2.add_updater(lambda x: x.move_to(axes.c2p(t.get_value(), 0)))
        # focal2_label.add_updater(lambda x: x.move_to(axes.c2p(t.get_value(), 0)))

        self.play(
            Create(focal2),
            Write(focal2_label),
            # Write(focal_len_label_txt),
            # Write(focal_len_label_value),
        )
        # focal2.add_updater(lambda x: x.move_to(axes.c2p(focal_slider.get_value(), 0)))
        # focal2_label.add_updater(lambda x: x.next_to(focal2, DOWN))  # Adjust position
        # focal_len_label_value.add_updater(
        #     lambda x: x.next_to(focal_len_label_txt, RIGHT)
        # )

        self.wait()

        # self.next_section(skip_animations=True)

        # Create f' label and brace
        brace_f_dash = BraceBetweenPoints(
            [0, -2, 0],
            [focal_len, -2, 0],
            buff=0.1,
            color=BLUE,
        )
        self.play(Write(brace_f_dash))
        f_dash_desc_1 = Tex("Focal length", color=BLUE).scale(0.6).move_to([1, -2.6, 0])
        f_dash_desc_2 = Tex("$f'$", color=BLUE).scale(1).move_to([1, -2.7, 0])
        self.play(Write(f_dash_desc_1))
        self.wait()
        self.play(ReplacementTransform(f_dash_desc_1, f_dash_desc_2))

        self.wait()
        brace_f = BraceBetweenPoints(
            [-focal_len, -2, 0],
            [0, -2, 0],
            buff=0.1,
            color=BLUE,
        )
        self.play(Write(brace_f))
        f_desc = Tex("$f$", color=BLUE).scale(1).move_to([-1, -2.7, 0])
        self.play(Write(f_desc))

        # self.next_section(skip_animations=True)

        # self.next_section()

        # entire_ray_diagram -= focal2
        focal_len_scaling_factor = 2
        focal_len_label_txt = Tex("$f' = $", color=BLUE).scale(0.8).move_to([1, 2.7, 0])
        focal_len_label_value = (
            DecimalNumber(
                focal_len / focal_len_scaling_factor,
                num_decimal_places=3,
                unit="\\;\\text{m}",
                color=BLUE,
            )
            .scale(0.8)
            .next_to(focal_len_label_txt, RIGHT)
        )
        focal_pow_label_txt = (
            Tex("$F = $", color=BLUE).scale(0.8).move_to([-2.5, 2.7, 0])
        )
        focal_pow_label_value = (
            DecimalNumber(
                1 / (focal_len / focal_len_scaling_factor),
                num_decimal_places=3,
                unit="\\;\\text{D}",
                color=BLUE,
            )
            .scale(0.8)
            .next_to(focal_pow_label_txt, RIGHT)
        )

        # line = Line(axes.c2p(0, -2.2), axes.c2p(focal_len, -2.2), color=BLUE)
        # label_text = MathTex("f'").scale(0.65)
        # label_text.next_to(line, DOWN)

        def update_focal_elements(obj):
            f_dash = focal_slider.get_value()
            focal1.move_to(axes.c2p(-f_dash, 0))
            focal1_label.next_to(focal1, DOWN)
            focal2.move_to(axes.c2p(f_dash, 0))
            focal2_label.next_to(focal2, DOWN)
            focal_len_label_value.set_value(f_dash / focal_len_scaling_factor)
            focal_pow_label_value.set_value(1 / (f_dash / focal_len_scaling_factor))
            # line.put_start_and_end_on(axes.c2p(0, -2.2), axes.c2p(f_dash, -2.2))
            # label_text.next_to(line, DOWN)
            # braces
            brace_f_dash.become(
                BraceBetweenPoints(
                    [0, -2, 0],
                    [f_dash, -2, 0],
                    buff=0.1,
                    color=BLUE,
                ).scale(0.65)
            )
            f_dash_desc_2.next_to(brace_f_dash, DOWN)
            brace_f.become(
                BraceBetweenPoints(
                    [-f_dash, -2, 0],
                    [0, -2, 0],
                    buff=0.1,
                    color=BLUE,
                ).scale(0.65)
            )
            f_desc.next_to(brace_f, DOWN)
            # rays
            # line.put_start_and_end_on(axes.c2p(0, -2.2), axes.c2p(f_dash, -2.2))
            end_pos_1 = get_coords_F_dash(h=height_1, f_dash=f_dash)
            ray_end_1.put_start_and_end_on(
                axes.c2p(0, height_1), axes.c2p(end_pos_1[0], end_pos_1[1])
            )
            end_pos_2 = get_coords_F_dash(h=height_2, f_dash=f_dash)
            ray_end_2.put_start_and_end_on(
                axes.c2p(0, height_2), axes.c2p(end_pos_2[0], end_pos_2[1])
            )
            end_pos_4 = get_coords_F_dash(h=height_4, f_dash=f_dash)
            ray_end_4.put_start_and_end_on(
                axes.c2p(0, height_4), axes.c2p(end_pos_4[0], end_pos_4[1])
            )
            end_pos_5 = get_coords_F_dash(h=height_5, f_dash=f_dash)
            ray_end_5.put_start_and_end_on(
                axes.c2p(0, height_5), axes.c2p(end_pos_5[0], end_pos_5[1])
            )

        # Create sliders
        focal_slider = ValueTracker(focal_len)
        focal_slider.add_updater(update_focal_elements)

        focal1.add_updater(lambda x: x.move_to(axes.c2p(-focal_slider.get_value(), 0)))
        focal2.add_updater(lambda x: x.move_to(axes.c2p(focal_slider.get_value(), 0)))
        focal1_label.add_updater(lambda x: x.next_to(focal1, DOWN))
        focal2_label.add_updater(lambda x: x.next_to(focal2, DOWN))
        focal_len_label_value.add_updater(
            lambda x: x.next_to(focal_len_label_txt, RIGHT)
        )
        focal_pow_label_value.add_updater(
            lambda x: x.next_to(focal_pow_label_txt, RIGHT)
        )
        # lines used for testing
        # line.add_updater(
        #     lambda x: x.put_start_and_end_on(
        #         axes.c2p(0, -2.2), axes.c2p(focal_slider.get_value(), -2.2)
        #     )
        # )
        # label_text.add_updater(lambda x: x.next_to(line, DOWN))
        brace_f_dash.add_updater(
            lambda x: x.become(
                BraceBetweenPoints(
                    axes.c2p(0, -2),
                    axes.c2p(focal_slider.get_value(), -2),
                    buff=0.1,
                    color=BLUE,
                )
            )
        )
        f_dash_desc_2.add_updater(lambda x: x.next_to(brace_f_dash, DOWN))
        brace_f.add_updater(
            lambda x: x.become(
                BraceBetweenPoints(
                    axes.c2p(-focal_slider.get_value(), -2),
                    axes.c2p(0, -2),
                    buff=0.1,
                    color=BLUE,
                )
            )
        )
        f_desc.add_updater(lambda x: x.next_to(brace_f, DOWN))
        # rays
        ray_end_1.add_updater(
            lambda x: x.put_start_and_end_on(
                axes.c2p(0, height_1),
                axes.c2p(
                    get_coords_F_dash(
                        h=height_1, f_dash=focal_slider.get_value(), x_or_y="x"
                    ),
                    get_coords_F_dash(
                        h=height_1, f_dash=focal_slider.get_value(), x_or_y="y"
                    ),
                ),
            )
        )
        ray_end_2.add_updater(
            lambda x: x.put_start_and_end_on(
                axes.c2p(0, height_2),
                axes.c2p(
                    get_coords_F_dash(
                        h=height_2, f_dash=focal_slider.get_value(), x_or_y="x"
                    ),
                    get_coords_F_dash(
                        h=height_2, f_dash=focal_slider.get_value(), x_or_y="y"
                    ),
                ),
            )
        )
        ray_end_4.add_updater(
            lambda x: x.put_start_and_end_on(
                axes.c2p(0, height_4),
                axes.c2p(
                    get_coords_F_dash(
                        h=height_4, f_dash=focal_slider.get_value(), x_or_y="x"
                    ),
                    get_coords_F_dash(
                        h=height_4, f_dash=focal_slider.get_value(), x_or_y="y"
                    ),
                ),
            )
        )
        ray_end_5.add_updater(
            lambda x: x.put_start_and_end_on(
                axes.c2p(0, height_5),
                axes.c2p(
                    get_coords_F_dash(
                        h=height_5, f_dash=focal_slider.get_value(), x_or_y="x"
                    ),
                    get_coords_F_dash(
                        h=height_5, f_dash=focal_slider.get_value(), x_or_y="y"
                    ),
                ),
            )
        )

        # self.play(
        #     Uncreate(brace_f_dash),
        #     Uncreate(f_dash_desc_2),
        # )

        # group everything
        entire_ray_diagram = VGroup(
            x_lines,
            y_lines,
            principal_axis,
            lens,
            # lens_label,
            bottom_arrow_left,
            bottom_arrow_right,
            top_arrow_left,
            top_arrow_right,
            # group_F,
            group_F_dash,
            focal1,
            focal1_label,
            focal2,
            focal2_label,
            brace_f_dash,
            f_dash_desc_2,
            brace_f,
            f_desc,
        )

        # f_always(entire_ray_diagram.move_to, lambda: axes.c2p(1, 1))
        # self.remove(axes)
        self.play(
            axes.animate.scale(0.65).to_edge(LEFT),
            entire_ray_diagram.animate.scale(0.65).to_edge(LEFT),
            run_time=2,
        )
        # self.play(
        #     Create(brace_f_dash),
        #     Create(f_dash_desc_2),
        # )
        self.wait()

        self.next_section()
        lens_power_eq = (
            Tex("$F= \\frac{1}{f'}$", color=BLUE).scale(1).move_to([4, 1, 0])
        )
        self.play(Write(lens_power_eq))
        self.wait()
        lens_power_eq_desc_intro = (
            Tex("where", color=BLUE).scale(0.8).move_to([4, 0, 0])
        )
        lens_power_eq_desc_1 = (
            Tex("$F$ - lens power (dioptres)", color=BLUE)
            .scale(0.8)
            .move_to([4, -0.5, 0])
        )
        lens_power_eq_desc_2 = (
            Tex("$f'$ - focal length (metres)", color=BLUE)
            .scale(0.8)
            .move_to([4, -1, 0])
        )
        self.play(
            Write(lens_power_eq_desc_intro),
            Write(lens_power_eq_desc_1),
            Write(lens_power_eq_desc_2),
        )

        self.next_section()

        self.wait()

        # self.remove(brace_f_dash, f_dash_desc_2)

        self.play(
            # Create(focal2_label),
            Write(focal_len_label_txt),
            Write(focal_len_label_value),
            Write(focal_pow_label_txt),
            Write(focal_pow_label_value),
        )

        # self.play(Create(line), Create(label_text))

        self.play(focal_slider.animate.set_value(0.6), run_time=4)
        self.play(focal_slider.animate.set_value(0.6), run_time=4)
        # using repeat instead of wait to avoid graphical bug
        # self.wait()
        self.play(focal_slider.animate.set_value(5), run_time=4)
        self.play(focal_slider.animate.set_value(5), run_time=4)

        self.play(focal_slider.animate.set_value(2), run_time=4)

        # self.play(Write(lens_power_eq_desc_1))
        # self.play(Write(lens_power_eq_desc_2))
