from manim import *
from manim_slides import Slide
from PIL import Image

template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
template.add_to_preamble(r"""
\usepackage{fontspec}
\setmainfont{Liberation Sans}
\setsansfont{Liberation Sans}
\renewcommand{\familydefault}{\sfdefault}
""")
config.tex_template = template

class EvoluzioneParametro(Slide):
    def construct(self):
        self.camera.background_color = WHITE
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        # numeri slide
        self.slide_n = 0
        self.num = None
        self.n_tot = 13

        def nuova_slide():
            self.slide_n += 1
            nuovo = Tex(f"{self.slide_n} / {self.n_tot}", font_size=24)
            nuovo.to_corner(UL, buff=0.3)
            if self.num is not None:
                self.remove(self.num)
            self.num = nuovo
            self.add(nuovo)

        def mostra(*mob, t=0.1):
            self.add(*mob)
            self.wait(t)

        def nascondi(*mob):
            self.remove(*mob)

        # pulizia immagine
        im = Image.open("Phonon_dispersion.png").convert("RGB")
        w, h = im.size
        box = (0, int(h*0.90), int(w*0.3), h)
        im.paste((255, 255, 255), box)
        im.save("Phonon_dispersion_clean.png")

        # --- slide 1: titolo ---------------------------------------
        riga1 = Tex("Shear stiffening associated", font_size=52)
        riga2 = Tex("with angular forces", font_size=52)
        titolo = VGroup(riga1, riga2).arrange(DOWN, buff=0.3)
        sotto = Tex("Fabio Tonelli", font_size=32).next_to(titolo, DOWN, buff=0.8)
        logo_unimi = ImageMobject("Unimi-logo.png").to_corner(UR , buff=0.3)
        nuova_slide()
        mostra(titolo, sotto,logo_unimi)
        self.next_slide()
        nascondi(titolo, sotto,logo_unimi)
        

        # slide 7: fononi longitudinali maggiori dei trasversali
        titolo7 = Tex("Typical phonon dispersion curves", font_size=44).to_edge(UP)
        img7 = ImageMobject("Phonon_dispersion_clean.png")
        img7.scale_to_fit_height(5.4)
        img7.next_to(titolo7, DOWN, buff=0.3)

        # label_y = Tex(
        #     r"$\boldsymbol{\omega(q)}\ [10^{13}\,\text{rad/s}]$", font_size=32
        # ).rotate(90 * DEGREES)
        # label_y.next_to(img7, LEFT, buff=0.2)

        # label_x = Tex(
        #     r"$\boldsymbol{q/q_{[\mathrm{zone\ boundary}]}}$", font_size=32
        # )
        # label_x.next_to(img7, DOWN, buff=0.2)

        # Phonons_fig = Group(img7, label_x, label_y)
        # Phonons_fig.to_edge(RIGHT, buff=0.3)
        img7.to_edge(RIGHT, buff = 0.3)
        Approximation_Title = Tex(
        r"Long wave-length approximation:\\[0.2cm] "
        r"$\boldsymbol{|\vec{q}|\rightarrow 0}$",
        font_size=36,
        )

        punto1 = Tex(r"$\bullet$ $\boldsymbol{\omega(\vec{q}) = v |\vec{q}|}$ $\vspace{0.1cm}$", font_size=30)
        punto2 = Tex(r"$\bullet$ Wave velocities from the elastic constants.", font_size=30)
        punto3 = Tex(r"$\bullet$ Uniform deformations", font_size=30)
        
        Approx_group = VGroup(Approximation_Title, punto1, punto2,punto3).arrange(
            DOWN, aligned_edge=LEFT, buff=1.2
        )

# spazio libero a sinistra della figura (label_y inclusa)
        # larghezza_disp = Phonons_fig.get_left()[0] - (-config.frame_width / 2) - 0.4 - 0.3
        larghezza_disp = img7.get_left()[0] - (-config.frame_width / 2) - 0.4 - 0.3
        if Approx_group.width > larghezza_disp:
            Approx_group.scale_to_fit_width(larghezza_disp)

        Approx_group.to_edge(LEFT, buff=0.2)
        Approx_group.align_to(img7, UP) 
        Approx_group.shift(DOWN*0.4)

        nuova_slide()
        # mostra(titolo7, Phonons_fig)
        mostra(titolo7, img7)
        self.next_slide()
        mostra(Approximation_Title)
        self.next_slide()
        mostra(punto1)
        self.next_slide()
        mostra(punto2)
        self.next_slide()
        # mostra(punto3)
        # self.next_slide()
        # nascondi(titolo7, Phonons_fig, Approximation_Title, punto1 , punto2, punto3)
        nascondi(titolo7, img7, Approximation_Title, punto1 , punto2, punto3)
        
        

      # --- slide 10: modello del cristallo ---------------------------------------

        Crystal_model = Tex("Crystal model", font_size=44).to_edge(UP)

        label_SC_vicini = Tex("Simple Cubic (SC):", font_size=36)
        label_FCC_vicini = Tex("Face-Centered Cubic (FCC):", font_size=36)

        img_SC_vicini = ImageMobject("SC_vicini.png")
        img_FCC_vicini = ImageMobject("FCC_primi_vicini.png")

        # area disponibile per ciascuna colonna
        margin = 0.1                      # margine ai bordi dello schermo
        gap = 1.2                         # spazio tra le due colonne
        col_w = (config.frame_width - 2 * margin - gap) / 2

        # altezza disponibile sotto il titolo (meno label e spaziature)
        label_h = max(label_SC_vicini.height, label_FCC_vicini.height)
        top_y = Crystal_model.get_bottom()[1] - 0.3
        bottom_y = -config.frame_height / 2 + margin
        col_h = (top_y - bottom_y) - label_h - 0.3   # 0.3 = buff label-immagine

        for img in (img_SC_vicini, img_FCC_vicini):
            # scala per stare dentro col_w x col_h, mantenendo le proporzioni
            scale = min(col_w / img.width, col_h / img.height)
            img.scale(scale)

        group_SC_vicini = Group(label_SC_vicini, img_SC_vicini).arrange(DOWN, buff=0.3)
        group_FCC_vicini = Group(label_FCC_vicini, img_FCC_vicini).arrange(DOWN, buff=0.3)

        gruppo_vicini = Group(group_SC_vicini, group_FCC_vicini).arrange(RIGHT, buff=gap)
        gruppo_vicini.next_to(Crystal_model, DOWN, buff=0.3)

        # # formula al centro, sotto le immagini
        # U_totale = MathTex(r"U_{TOT} = U_{LJ} + U_{TB}.", font_size=44)
        # U_totale.next_to(gruppo_vicini, DOWN, buff=0.7)
        # U_totale.set_x(0)

        nuova_slide()
        mostra(Crystal_model)
        self.next_slide()
        mostra(group_SC_vicini)
        self.next_slide()
        mostra(group_FCC_vicini)
        self.next_slide()
        # mostra(U_totale)
        # self.next_slide()

        # nascondi(Crystal_model,group_SC_vicini,group_FCC_vicini,U_totale)
        nascondi(Crystal_model,group_SC_vicini,group_FCC_vicini)

                 # --- slide 6: Potential ---------------
        titolo6 = Tex("Potential", font_size=44).to_edge(UP)

        notation_label = Tex(r"\textbf{$\gamma_w$}:", font_size=38)
        notation_eq = MathTex(
            r"""
            \begin{aligned}
            45^\circ \leftrightarrow w=1 &\qquad 120^\circ \leftrightarrow w=4&\\[0.2cm]
            60^\circ \leftrightarrow w=2 &\qquad 135^\circ \leftrightarrow w=5&\\[0.2cm]
            90^\circ \leftrightarrow w=3 &\qquad 180^\circ \leftrightarrow w=6&
            \end{aligned}
            """,
            font_size=32,
        )

        notation_group = VGroup(notation_label, notation_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        notation_group.to_corner(UR, buff=0.3).shift(DOWN*0.78,RIGHT*0.3)

        # --- LJ ---
        lj_label = Tex(r"\textbf{U$_{LJ}$}:", font_size=36)
        lj_eq = MathTex(
            r"""
            U_{LJ}(r_{ij}) &= \sum_{\text{pairs }i j} V_{LJ}(r_{ij})
            = \sum_{i=1}^N \sum_{j<i} V_{LJ}(r_{ij}) \\
            V_{LJ}(r) &= 4\epsilon \left[
            \left(\frac{\sigma}{r}\right)^{12}
            - \left(\frac{\sigma}{r}\right)^{6}
            \right]
            """,
            font_size=32,
        )
        lj_group = VGroup(lj_label, lj_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        
        
        # --- Three-body ---
        tb_label = Tex(r"\textbf{U$_{TB}$}:", font_size=36)
        tb_eq = MathTex(
            r"""
            U_{TB} &= \sum_{\substack{i,j,l \\ i<j<l}}
            \gamma(\theta_{0ijl})
            \left[1-\cos(\theta_{ijl}-\theta_{0ijl})\right] \\
            &\equiv \sum_{\substack{i,j,l \\ i<j<l}}
            \gamma_{w}
            \left[1-\cos(\theta_{ijl}-\theta_{0ijl})\right]
            """,
            font_size=32,
        )
        tb_group = VGroup(tb_label, tb_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        potenziali = VGroup(lj_group, tb_group).arrange(DOWN, aligned_edge=LEFT, buff=1.0)

        # --- layout: formule a sinistra, tripletta a destra ---
        x_split = 1.0                                   # coordinata x che separa le due zone
        larghezza_disp = x_split - (-config.frame_width / 2) - 0.4 - 0.3
        altezza_disp = config.frame_height - 2
        if potenziali.width > larghezza_disp:
            potenziali.scale_to_fit_width(larghezza_disp)
        if potenziali.height > altezza_disp:
            potenziali.scale_to_fit_height(altezza_disp)
        potenziali.to_edge(LEFT, buff=0.4)

        # --- tripletta con angolo theta0 -> theta ---
        L = 2.5
        theta0 = 110 * DEGREES
        theta = 120 * DEGREES
        dir_i = np.array([1.0, 0.0, 0.0])

        def rot(v, ang):
            return np.array([
                v[0] * np.cos(ang) - v[1] * np.sin(ang),
                v[0] * np.sin(ang) + v[1] * np.cos(ang),
                0,
            ])

        shift_x = 1
        # centro della zona destra, tb_group allineato verticalmente
        C = np.array([x_split + (config.frame_width / 2 - x_split) / 2 - shift_x,
                      tb_group.get_center()[1], 0])
        J = C - np.array([0.5, 0.85, 0])      # vertice (particella j)
        I = J + L * dir_i
        L0 = J + L * rot(dir_i, theta0)

        # parte fissa: configurazione di equilibrio
        bond_ji = Line(J, I, color=BLACK)
        bond_jl0 = DashedLine(J, L0, color=BLACK, dash_length=0.12)
        arc0 = Angle(Line(J, I), Line(J, L0), radius=1, color=GRAY)
        lab0 = MathTex(r"\theta_{0ijl}", font_size=28, color=GRAY).move_to(
            J + 1.15 * rot(dir_i, theta0 / 3) + np.array([0.15, 0.1, 0]))
        ghost = Dot(L0, color=PURPLE, radius=0.08).set_opacity(0.8)
        dot_i = Dot(I, color=GREEN, radius=0.1)
        dot_j = Dot(J, color=BLUE, radius=0.1)
        name_i = MathTex("i", font_size=28).next_to(dot_i, DOWN, buff=0.12)
        name_j = MathTex("j", font_size=28).next_to(dot_j, DOWN, buff=0.12)
        name_l = MathTex("l", font_size=28).next_to(L0, UP, buff=0.12)

        triplet_static = VGroup(bond_ji, bond_jl0, arc0, lab0, ghost,
                                dot_i, dot_j, name_i, name_j, name_l)
        
        

        # parte mobile
        t = ValueTracker(theta0)
        bond_jl = always_redraw(lambda: Line(
            J, J + L * rot(dir_i, t.get_value()), color=RED))
        dot_l = always_redraw(lambda: Dot(
            J + L * rot(dir_i, t.get_value()), color=RED, radius=0.1))
        arc = always_redraw(lambda: Angle(
            Line(J, I), Line(J, J + L * rot(dir_i, t.get_value())),
            radius=0.45, color=RED))
        lab = always_redraw(lambda: MathTex(r"\theta_{ijl}", font_size=28, color=RED).move_to(
            J + 0.8 * rot(dir_i, t.get_value() / 2)))
        triplet_live = VGroup(bond_jl, dot_l, arc, lab)

        # --- legame che da r0ij va a rij -> theta ---

        nuova_slide()
        # --- sequenza ---
        mostra(titolo6)
        self.next_slide()
        mostra(notation_group)
        self.next_slide()
        mostra(lj_group)
        self.next_slide()
        mostra(tb_group)
        self.next_slide()
        mostra(triplet_static)          # tripletta all'equilibrio
        self.next_slide()
        self.add(triplet_live)                     # compare sopra la traccia
        self.play(t.animate.set_value(theta), run_time=2.5, rate_func=smooth)
        self.next_slide()
        nascondi(titolo6, lj_group, tb_group,notation_group,triplet_static,triplet_live)
        #self.play(FadeOut(triplet_static), FadeOut(triplet_live))

       

#              # --- slide 9: densità di energia---------------------------------------
        Energy_density = Tex("Energy density", font_size=44).to_edge(UP)

        r_to_rprimo = Tex(r"\textbf{$r \rightarrow r'$} :", font_size=40)

        spostamento_R = Tex(
            r"\textbf{$R = r' - r = \xi(r)\,\hat{x} + \psi(r)\,\hat{y} + \zeta(r)\,\hat{z}$}",
            font_size=40,
        )

        energy_density_mix = MathTex(
            r"u\equiv",
            r"u-u_0 = \frac{U}{V}",
            r"=",
            r"\frac{1}{2}\sum_{\substack{\lambda,\mu}}{C}_{\lambda\mu}e_\lambda e_\mu",
            font_size=36,
        )

        energy_density_symm = MathTex(
            r"=",
            r"\frac{1}{2}C_{11}(e_{xx}^2 + e_{yy}^2 + e_{zz}^2)"
            r"+ \frac{1}{2}C_{44}(e_{yz}^2 + e_{zx}^2 + e_{xy}^2)"
            r"+ C_{12}(e_{yy}e_{zz} + e_{zz}e_{xx} + e_{xx}e_{yy})",
            font_size=36,
        )

        # gruppo r -> r', R: al posto di epsilon + deformazione (a sinistra, sotto il titolo)
        gruppo_spostamentoR = VGroup(r_to_rprimo, spostamento_R).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        gruppo_spostamentoR.next_to(Energy_density, DOWN, buff=0.4)
        gruppo_spostamentoR.to_edge(LEFT, buff=0.2)

                # freccia blu verticale tra gruppo r e densità di energia
        x_freccia = gruppo_spostamentoR.get_left()[0] + 1.5
        freccia = Arrow(
            start=[x_freccia, gruppo_spostamentoR.get_bottom()[1], 0],
            end=[x_freccia, energy_density_mix.get_top()[1]-0.8, 0],
            buff=0.15,
            color=BLUE,
            stroke_width=5,
        )

        # densità di energia sotto il gruppo
        energy_density_mix.next_to(gruppo_spostamentoR, DOWN, buff=2.3)
        energy_density_mix.to_edge(LEFT, buff=0.2)
        energy_density_symm.next_to(energy_density_mix, DOWN, buff=0.3)

        # allinea l'= della symm al primo elemento della mix
        dx = energy_density_mix[0].get_center()[0] - energy_density_symm[0].get_center()[0]
        energy_density_symm.shift(RIGHT * dx)

        # matrice: a destra, subito sotto il titolo
        C_matrix = MathTex(
            r"""
            C = \begin{bmatrix}
            C_{11} & C_{12} & C_{12} & 0 & 0 & 0 \\
            C_{12} & C_{11} & C_{12} & 0 & 0 & 0 \\
            C_{12} & C_{12} & C_{11} & 0 & 0 & 0 \\
            0 & 0 & 0 & C_{44} & 0 & 0 \\
            0 & 0 & 0 & 0 & C_{44} & 0 \\
            0 & 0 & 0 & 0 & 0 & C_{44}
            \end{bmatrix}
            """,
            font_size=40,
        )
        C_matrix.next_to(Energy_density, DOWN, buff=1.3)
        C_matrix.to_edge(RIGHT, buff=0.2)   # dopo il next_to, che altrimenti la centra sotto il titolo

        nuova_slide()
        mostra(Energy_density)
        self.next_slide()
        mostra(gruppo_spostamentoR)
        self.next_slide()
        mostra(energy_density_mix,freccia)
        self.next_slide()
        mostra(C_matrix)
        self.next_slide()
        mostra(energy_density_symm)
        self.next_slide()
        nascondi(Energy_density, gruppo_spostamentoR, energy_density_mix, energy_density_symm, C_matrix,freccia)

        #Costanti elastiche
        titolo_costanti = Tex("Elastic constants", font_size=44).to_edge(UP)

        primo_epsilon = MathTex(
            r"""& \boldsymbol{\bullet e_{xx} \neq 0} \\
            & \rightarrow u(e_{xx}^2) \simeq \frac{1}{2}C_{11}\,e_{xx}^2""",
            font_size=36,
        )
        secondo_epsilon = MathTex(
            r"""&\boldsymbol{ \bullet e_{xx}=e_{yy}\equiv e_{12} \neq 0} \\
            & \rightarrow u(e_{12}^2) \simeq (C_{11}+C_{12})\,e_{12}^2""",
            font_size=36,
        )
        terzo_epsilon = MathTex(
            r"""&\boldsymbol{ \bullet e_{xy} \neq 0 }\\
            & \rightarrow u(e_{xy}^2) \simeq \frac{1}{2}C_{44}\,e_{xy}^2""",
            font_size=36,
        )

        epsilon_def = VGroup(primo_epsilon, secondo_epsilon, terzo_epsilon).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        epsilon_def.to_edge(LEFT, buff=0.3)
        epsilon_def.next_to(titolo_costanti, DOWN, buff=0.4)
        epsilon_def.to_edge(LEFT, buff=0.3)

        Elastic_constants = MathTex(
            r"""
            \text{SC: } &
            \begin{cases}
            C_{11}=\frac{1}{r_0^3}\left[72 \epsilon + 4(\gamma_{1}+\gamma_{2}+2\gamma_{3}+\gamma_{4}+\gamma_{5})\right] \\[0.4cm]
            C_{12}=-\frac{2}{r_{0}^3}(\gamma_{1}+\gamma_{2}+2\gamma_{3}+\gamma_{4}+\gamma_{5}) \\[0.4cm]
            C_{44}=\frac{2}{r_{0}^3}\left(\gamma_{1}+2\gamma_{2}+6\gamma_{3}+2\gamma_{4}+\gamma_{5}\right)
            \end{cases}
            \\[1cm]
            \text{FCC: } &
            \begin{cases}
            C_{11}=\frac{\sqrt{2}}{r_{0}^3}\left[72 \epsilon + 4(\gamma_{2}+2\gamma_{3}+\gamma_{4})\right] \\[0.4cm]
            C_{12}=\frac{\sqrt{2}}{r_{0}^3}\left[36 \epsilon - 2(\gamma_{2}+2\gamma_{3}+\gamma_{4})\right] \\[0.4cm]
            C_{44}=\frac{4\sqrt2}{r_{0}^3}\left(9\epsilon +\gamma_{2}+\gamma_{4}\right)
            \end{cases}
            """,
            font_size=28,
        )
        Elastic_constants.to_edge(RIGHT, buff=0.3)

        y = Elastic_constants.get_center()[1]

        frecciac = Arrow(
            start=[epsilon_def.get_right()[0], y, 0],
            end=[Elastic_constants.get_left()[0], y, 0],
            buff=0.2,
            color=BLUE,
            stroke_width=6,
        )

        nuova_slide()
        mostra(titolo_costanti, epsilon_def)
        self.next_slide()
        mostra(Elastic_constants, frecciac)
        self.next_slide()
        nascondi(titolo_costanti, epsilon_def, Elastic_constants, frecciac)
        
        #sounf velocities

        titolo_costanti = Tex("Sound velocities", font_size=44).to_edge(UP)
        
        n_def = Tex(r"$\vec{n} \equiv \frac {\vec{q}}{|\vec{q}|}$", font_size=44).to_corner(UR,buff = 0.6)
        n_def.shift(DOWN*0.5,LEFT*1)
        eigenv = MathTex(
            r"""
            \rho\, v^2
            \begin{bmatrix} \xi \\ \psi \\ \zeta \end{bmatrix}
            = \Gamma(\vec{n})
            \begin{bmatrix} \xi \\ \psi \\ \zeta \end{bmatrix}
            """,
            font_size=36,
        )

        dynmat = MathTex(
            r"""
            \Gamma(\vec{n}) =
            \begin{bmatrix}
            C_{11}n_x^2 + C_{44}(n_y^2 + n_z^2) & (C_{12}+C_{44})n_x n_y & (C_{12}+C_{44})n_x n_z \\[0.3cm]
            (C_{12}+C_{44})n_x n_y & C_{11}n_y^2 + C_{44}(n_x^2 + n_z^2) & (C_{12}+C_{44})n_y n_z \\[0.3cm]
            (C_{12}+C_{44})n_x n_z & (C_{12}+C_{44})n_y n_z & C_{11}n_z^2 + C_{44}(n_x^2 + n_y^2)
            \end{bmatrix}
            """,
            font_size=30,
        )

        eigenv.next_to(titolo_costanti, DOWN, buff=0.8)
        dynmat.next_to(eigenv, DOWN, buff=1)
        dynmat.set_x(0)
        eigenv.set_x(0)

        nuova_slide()
        mostra(titolo_costanti,eigenv,dynmat,n_def)
        self.next_slide()
        nascondi(eigenv, dynmat,titolo_costanti,n_def)
        
#         # --- slide 5: direzioni speciali ---------------------------------
        titolo5 = Tex("Special directions", font_size=44).to_edge(UP)
        img5 = ImageMobject("map_gamma_TL_analytic.png")

        altezza_disp = config.frame_height - titolo5.height - 1.2
        img5.scale_to_fit_height(altezza_disp)
        if img5.width > 0.6 * config.frame_width:
            img5.scale_to_fit_width(0.6 * config.frame_width)

        img5.to_edge(RIGHT, buff=0.3)
        img5.shift(UP * (titolo5.get_bottom()[1] - 0.3 - img5.get_top()[1]))

        #check
        spunta_ok = MathTex(r"\checkmark", color=GREEN, font_size=48)
        spunta_no = MathTex(r"\times", color=RED, font_size=48)
        # --- SC ---
        sc_label = Tex(r"\textbf{SC}:", font_size=38)
        sc_eq = MathTex(
            r"""\begin{array}{@{}l@{\quad}r@{\,:\,}l@{}}
            {[1\,0\,0]} & T>L   & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_1+\gamma_5}{2} \\[2.5ex]
            {[1\,1\,0]} & T_1>L & \gamma_3 < -18\,\epsilon - \dfrac{\gamma_1+\gamma_2+\gamma_4+\gamma_5}{2} \\[2.5ex]
                        & T_2>L & \gamma_3 < -\dfrac{\gamma_2+\gamma_4}{4} \\[2.5ex]
            {[1\,1\,1]} & T>L   & \gamma_3 < -\dfrac{\gamma_2+\gamma_4}{4}
            \end{array}""",
            font_size=32,
        )
        sc_group = VGroup(sc_label, sc_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # --- FCC ---
        fcc_label = Tex(r"\textbf{FCC}:", font_size=38)
        fcc_eq = MathTex(
            r"""\begin{array}{@{}l@{\quad}r@{\,:\,}l@{}}
            {[1\,0\,0]} & T>L   & \gamma_3 < -\dfrac{9}{2}\,\epsilon \\[2.5ex]
            {[1\,1\,0]} & T_1>L & \gamma_3 < -27\,\epsilon - \dfrac{\gamma_2+\gamma_4}{2} \\[2.5ex]
                        & T_2>L & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_2+\gamma_4}{2} \\[2.5ex]
            {[1\,1\,1]} & T>L   & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_2+\gamma_4}{2}\,
            \end{array}""",
            font_size=32,
        )
        fcc_group = VGroup(fcc_label, fcc_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        relazioni_speciali = VGroup(sc_group, fcc_group).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        larghezza_disp = img5.get_left()[0] - (-config.frame_width / 2) - 0.4 - 0.3
        if relazioni_speciali.width > larghezza_disp:
            relazioni_speciali.scale_to_fit_width(larghezza_disp)
        if relazioni_speciali.height > altezza_disp:
            relazioni_speciali.scale_to_fit_height(altezza_disp)

        relazioni_speciali.to_edge(LEFT, buff=0.4)
        relazioni_speciali.match_y(img5)

                # --- simboli per ogni riga (posizionati dopo il layout finale) ---
        def centro_riga(eq, i, n=4):
            # centro verticale stimato della riga i (0 = prima) di n righe equispaziate
            return eq.get_top()[1] - eq.height * (i + 0.5) / n

        def simbolo_a(eq, i, ok, dx=0.3):
            if ok:
                s = MathTex(r"\checkmark", color=GREEN, font_size=40)
            else:
                s = MathTex(r"\times", color=RED, font_size=40)
            s.set_stroke(color=s.get_color(), width=2.5)   # più alto = più grassetto
            s.move_to([eq.get_right()[0] + dx + s.width / 2, centro_riga(eq, i), 0])
            return s

        # True = spunta verde (">"), False = x rossa ("< -")
        segni_sc  = [True, False, False, False]
        segni_fcc = [False, False, True, True]

        checks_sc  = VGroup(*[simbolo_a(sc_eq, i, ok) for i, ok in enumerate(segni_sc)])
        checks_fcc = VGroup(*[simbolo_a(fcc_eq, i, ok) for i, ok in enumerate(segni_fcc)])
        checks = VGroup(checks_sc, checks_fcc)

        nuova_slide()
        mostra(titolo5)
        self.next_slide()
        mostra(img5,sc_group)
        self.next_slide()
        mostra(checks_sc)
        self.next_slide()
        mostra(fcc_group,checks_fcc)
        self.next_slide()
        nascondi(titolo5, sc_group, fcc_group, img5, checks_sc,checks_fcc)

        
                        #  --- slide 4: Random sampling of the unit sphere ---------------
        from pathlib import Path

        titolo4 = Tex("Random sampling of the unit sphere", font_size=44).to_edge(UP)
        N = 60
        frames = [np.array(Image.open(f"frames/f_{i:03d}.png").convert("RGBA"))
                  for i in range(N)]

        # png finali prodotti da plot_sphere.py (stesso ordine di gamma3_val)
        gamma3_val = [1, 1.5, 2, 2.5, 3,3.5,4,4.5,5]
        cartella_png = Path(__file__).parent      # cambia se i png stanno altrove
        png_files = [cartella_png / f"sphere_SC_FCC_{i}.png" for i in range(len(gamma3_val))]
        for p in png_files:
            assert p.exists(), f"manca {p}"
        png_arrays = [np.array(Image.open(p).convert("RGBA")) for p in png_files]

        def immagine(arr):
            img = ImageMobject(arr).scale_to_fit_height(5.6)
            img.next_to(titolo4, DOWN, buff=0.1)
            return img

        def parametri(img, g3):
            def x_pannello(frac):
                return img.get_left()[0] + frac * img.width

            par_sc = Tex(rf"$\gamma_1 = \gamma_5 = 1$\\$\gamma_3 = {g3}$", font_size=32)
            par_fcc = Tex(rf"$\gamma_2 = \gamma_4 = 1$\\$\gamma_3 = {g3}$", font_size=32)
            y = img.get_bottom()[1] + 0.2
            par_sc.move_to([x_pannello(0.22), y, 0], aligned_edge=UP)
            par_fcc.move_to([x_pannello(0.66), y, 0], aligned_edge=UP)
            return par_sc, par_fcc

        nuova_slide()
        # --- crescita dei puntini (solo per il primo) ---
        corrente = immagine(frames[0])
        mostra(titolo4, corrente)
        self.next_slide()                        # click: parte la crescita

        durata = 2.5
        for i in range(1, N):
            nuovo = immagine(frames[i])
            self.remove(corrente)
            self.add(nuovo)
            corrente = nuovo
            self.wait(durata / N)

        self.next_slide()                        # click: mostra i parametri

        par_sc, par_fcc = parametri(corrente, gamma3_val[0])
        mostra(par_sc, par_fcc)
        self.next_slide()                        # click: valore successivo

        # --- valori successivi: un click per ciascun png ---
        for k in range(1, len(png_arrays)):
            nuovo = immagine(png_arrays[k])
            nuovo_sc, nuovo_fcc = parametri(nuovo, gamma3_val[k])

            nascondi(corrente, par_sc, par_fcc)  # prima tolgo tutto il vecchio
            mostra(nuovo, nuovo_sc, nuovo_fcc)
            corrente, par_sc, par_fcc = nuovo, nuovo_sc, nuovo_fcc
            self.next_slide()

        nascondi(corrente, titolo4, par_sc, par_fcc)
        
        #slide 8
# --- slide 2: Color maps ------------------------------------
        titolo2 = Tex("Fraction of directions", font_size=44).to_edge(UP)

        img1 = ImageMobject("color_map_gamma_SC_TL_shared.png")
        img2 = ImageMobject("color_map_gamma_FCC_TL_shared.png")

        immagini = Group(img1, img2).arrange(DOWN, buff=0.2)
        immagini.scale_to_fit_height(6.6)
        if immagini.width > config.frame_width - 0.6:
            immagini.scale_to_fit_width(config.frame_width - 0.6)
        immagini.next_to(titolo2, DOWN, buff=0.2)

        # etichette a sinistra, alla stessa altezza di ciascuna figura
        label_SC = Tex(r"\textbf{SC:}", font_size=38)
        label_FCC = Tex(r"\textbf{FCC:}", font_size=38)

        label_SC.next_to(img1, LEFT, buff=0.3)
        label_FCC.next_to(img2, LEFT, buff=0.3)
        label_FCC.align_to(label_SC, RIGHT)   # etichette allineate tra loro sul bordo destro

        nuova_slide()
        mostra(titolo2)
        self.next_slide()
        mostra(img1, label_SC)
        self.next_slide()
        mostra(img2, label_FCC)
        self.next_slide()
        nascondi(titolo2, img1, img2, label_SC, label_FCC)




        # --- slide: conclusioni ---
        titolo_concl = Tex("Conclusions", font_size=44).to_edge(UP)

        concl = VGroup(
            Tex(r"$\bullet$ In the adopted model, regions of the parameter space", font_size=34),
            Tex(r"\phantom{$\bullet$} where the velocity inversion occurs have been found", font_size=34),
            Tex(r"$\bullet$ No region was found where $v_L < v_{T_1}, v_{T_2}$", font_size=34),
            Tex(r"\phantom{$\bullet$} for every propagation direction simultaneously", font_size=34),
        )
        concl.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        concl[2].shift(DOWN * 0.3)
        concl[3].shift(DOWN * 0.3)
        concl.next_to(titolo_concl, DOWN, buff=0.8)
        concl.to_edge(LEFT, buff=0.8)

        nuova_slide()
        mostra(titolo_concl)
        self.next_slide()
        mostra(concl[0], concl[1])
        self.next_slide()
        mostra(concl[2], concl[3])
        self.next_slide()
        nascondi(titolo_concl, concl[0],concl[1],concl[2],concl[3])
        # --- slide finale: conclusioni e sviluppi futuri ---
        titolo_fine = Tex("Future developments", font_size=44).to_edge(UP)

        punti = VGroup(
            Tex(r"$\bullet$ Extend the analysis to other lattices, starting from BCC", font_size=34),
            Tex(r"$\bullet$ Add second-neighbor angular terms for FCC, as done for SC", font_size=34),
            Tex(r"$\bullet$ Enlarge the parameter space: independent parameters", font_size=34),
            Tex(r"\phantom{$\bullet$} for each non-equivalent angular term", font_size=34),
            Tex(r"$\bullet$ Replace fixed neighbor lists with a flexible force field", font_size=34),
            Tex(r"\phantom{$\bullet$} (distances and angles on the fly, Stillinger-Weber style)", font_size=34),
        )
        punti.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        punti.next_to(titolo_fine, DOWN, buff=0.8)
        punti.to_edge(LEFT, buff=0.8)

        nuova_slide()
        mostra(titolo_fine)
        self.next_slide()
        mostra(punti[0])
        self.next_slide()
        mostra(punti[1])
        self.next_slide()
        mostra(punti[2], punti[3])
        self.next_slide()
        mostra(punti[4], punti[5])
        self.next_slide()
        nascondi(titolo_fine, punti[0],punti[1],punti[2],punti[3],punti[4],punti[5])


        #grazie per l'attenzione
        grazie = Tex("Thanks for the attention", font_size=52)
        nuova_slide()
        mostra(grazie)
        self.next_slide()
        nascondi(grazie)



#------------------------------------------------------------------------------------------------------------------
         # --- slide 3: maps ------------------------------------
        titolo3 = Tex(r"General $\vec{n}$ phase diagrams", font_size=44).to_edge(UP)

        img3 = ImageMobject("map_gamma_SC_TL.png")
        img4 = ImageMobject("map_gamma_FCC_TL.png")

        immagini = Group(img3, img4).arrange(RIGHT, buff=0.1)
        immagini.scale_to_fit_height(6.6)
        if immagini.width > config.frame_width - 0.6:
            immagini.scale_to_fit_width(config.frame_width - 0.6)
        immagini.next_to(titolo3, DOWN, buff=0.2)
        immagini.shift(LEFT * 0.02)

        mostra(titolo3)
        self.next_slide()
        mostra(img3)
        self.next_slide()
        mostra(img4)
        self.next_slide()
        nascondi(titolo3, img3, img4)
        

                        # problema secolare
        sec_title = Tex(r"Secular equation", font_size=44).to_edge(UP)

        eq_moto = Tex(
            r"$\rho\frac{\partial^2\xi}{\partial t^2}=\frac{\partial \sigma_{xx}}{\partial x}+\frac{\partial\sigma_{xy}}{\partial y}+\frac{\partial \sigma_{xz}}{\partial z}$",
            font_size=36,
        )
        eq_moto1 = Tex(
            r"""$\rho\frac{\partial^2\xi}{\partial t^2} = C_{11}\frac{\partial^2\xi}{\partial x^2}+
                C_{44}\left( \frac{\partial^2\xi}{\partial y^2}+\frac{\partial^2\xi}{\partial z^2}\right)+
                (C_{12} + C_{44})\left( \frac{\partial ^2\psi}{\partial x\partial y}+\frac{\partial^2\zeta}{\partial x \partial z}\right)$""",
            font_size=36,
        )

        larghezza_max = config.frame_width - 0.6
        if eq_moto1.width > larghezza_max:
            eq_moto1.scale_to_fit_width(larghezza_max)

        eqs = VGroup(eq_moto, eq_moto1).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eqs.next_to(sec_title, DOWN, buff=0.3)
        eqs.to_edge(LEFT, buff=0.3)

        # formula agli autovalori, in basso
        eq_secolare = MathTex(
            r"""
            \rho\, v^2
            \begin{bmatrix} \xi \\ \psi \\ \zeta \end{bmatrix}
            = \Gamma(\vec{n})
            \begin{bmatrix} \xi \\ \psi \\ \zeta \end{bmatrix}
            """,
            font_size=36,
        )
        eq_secolare.move_to([0, -2.0, 0])        # regola l'altezza a gusto

        # freccia blu verticale, al centro della slide in x
        freccia_sec = Arrow(
            start=[0, eqs.get_bottom()[1], 0],
            end=[0, eq_secolare.get_top()[1], 0],
            buff=0.15,
            color=BLUE,
            stroke_width=5,
        )

        # onda piana, a destra della freccia, a metà altezza
        onda = MathTex(
            r"\xi &= \xi_{0}\exp[i(\vec{q}\cdot \vec{s}-\omega t)]",
            font_size=36,
        )
        onda.next_to(freccia_sec, RIGHT, buff=0.3)

        velocitàq = MathTex(
        r"v(\omega,\vec{q}) = \frac{\omega}{|\vec{q}|}",
        font_size=36,
        )
        velocitàq.next_to(freccia_sec, LEFT, buff=0.3)
        mostra(sec_title)
        self.next_slide()
        mostra(eq_moto)
        self.next_slide()
        mostra(eq_moto1)
        self.next_slide()
        mostra(freccia_sec, onda,velocitàq)
        self.next_slide()
        mostra(eq_secolare)
        self.next_slide()
        nascondi(sec_title, eq_moto, eq_moto1, freccia_sec, onda, eq_secolare,velocitàq)


        #codice c++ diagonalizzazione, da fare
    #PDF-------------------------------------------------------------------------------------------------------------------
# import os
# from manim import *
# from manim_slides import Slide
# from PIL import Image

# # PDF_MODE=1 -> una sola pagina per slide (stato finale)
# PDF_MODE = os.environ.get("PDF_MODE", "0") == "1"

# template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
# template.add_to_preamble(r"""
# \usepackage{fontspec}
# \setmainfont{Liberation Sans}
# \setsansfont{Liberation Sans}
# \renewcommand{\familydefault}{\sfdefault}
# """)
# config.tex_template = template


# class EvoluzioneParametro(Slide):
#     def construct(self):
#         self.camera.background_color = WHITE
#         Tex.set_default(color=BLACK)
#         MathTex.set_default(color=BLACK)

#         # comparsa/scomparsa istantanea
#         def mostra(*mob, t=0.1):
#             self.add(*mob)
#             self.wait(t)

#         def nascondi(*mob):
#             self.remove(*mob)

#         # passo intermedio: nel PDF viene saltato
#         def passo():
#             if not PDF_MODE:
#                 self.next_slide()

#         # fine slide: sempre presente
#         def fine():
#             self.next_slide()

#         # --- slide 1: titolo ---------------------------------------
#         riga1 = Tex("Shear stiffening associated", font_size=52)
#         riga2 = Tex("with angular forces", font_size=52)
#         titolo = VGroup(riga1, riga2).arrange(DOWN, buff=0.3)
#         sotto = Tex("Fabio Tonelli", font_size=32).next_to(titolo, DOWN, buff=0.8)

#         mostra(titolo, sotto)
#         fine()
#         nascondi(titolo, sotto)

#         # --- slide 2: fononi ---------------------------------------
#         titolo7 = Tex("Typical phonon dispersion curves", font_size=44).to_edge(UP)
#         img7 = ImageMobject("Phonon_dispersion.png")
#         img7.scale_to_fit_height(5.4)
#         img7.next_to(titolo7, DOWN, buff=0.3)

#         label_y = Tex(
#             r"$\boldsymbol{\omega(q)}\ [10^{13}\,\text{rad/s}]$", font_size=32
#         ).rotate(90 * DEGREES)
#         label_y.next_to(img7, LEFT, buff=0.2)

#         label_x = Tex(
#             r"$\boldsymbol{q/q_{[\mathrm{zone\ boundary}]}}$", font_size=32
#         )
#         label_x.next_to(img7, DOWN, buff=0.2)

#         Phonons_fig = Group(img7, label_x, label_y)
#         Phonons_fig.to_edge(RIGHT, buff=0.3)

#         Approximation_Title = Tex(
#             r"Long wave-length approximation:\\[0.2cm] "
#             r"$\boldsymbol{\omega(q) \lesssim 10^{12}\text{-}10^{13}\,\text{rad/s}}$.",
#             font_size=36,
#         )

#         punto1 = Tex(r"$\bullet$ $\boldsymbol{\omega(q) = v \cdot q}$ $\vspace{0.1cm}$ for $\vspace{0.1cm}$ $q \to 0$.", font_size=30)
#         punto2 = Tex(r"$\bullet$ Wave velocities from the elastic constants.", font_size=30)
#         punto3 = Tex(r"$\bullet$ Uniform deformations.", font_size=30)

#         Approx_group = VGroup(Approximation_Title, punto1, punto2, punto3).arrange(
#             DOWN, aligned_edge=LEFT, buff=1.2
#         )

#         # spazio libero a sinistra della figura (label_y inclusa)
#         larghezza_disp = Phonons_fig.get_left()[0] - (-config.frame_width / 2) - 0.4 - 0.3
#         if Approx_group.width > larghezza_disp:
#             Approx_group.scale_to_fit_width(larghezza_disp)

#         Approx_group.to_edge(LEFT, buff=0.2)
#         Approx_group.align_to(img7, UP)
#         Approx_group.shift(DOWN * 0.4)

#         mostra(titolo7, Phonons_fig)
#         passo()
#         mostra(Approximation_Title)
#         passo()
#         mostra(punto1)
#         passo()
#         mostra(punto2)
#         fine()
#         nascondi(titolo7, Phonons_fig, Approximation_Title, punto1, punto2, punto3)

#         # --- slide 3: modello del cristallo ------------------------
#         Crystal_model = Tex("Crystal model", font_size=44).to_edge(UP)

#         label_SC_vicini = Tex("Simple Cubic (SC):", font_size=36)
#         label_FCC_vicini = Tex("Face-Centered Cubic (FCC):", font_size=36)

#         img_SC_vicini = ImageMobject("SC_vicini.png")
#         img_FCC_vicini = ImageMobject("FCC_primi_vicini.png")

#         max_h = 3.4
#         max_w = config.frame_width / 2 - 0.8

#         for img in (img_SC_vicini, img_FCC_vicini):
#             img.scale_to_fit_height(max_h)
#             if img.width > max_w:
#                 img.scale_to_fit_width(max_w)

#         group_SC_vicini = Group(label_SC_vicini, img_SC_vicini).arrange(DOWN, buff=0.5)
#         group_FCC_vicini = Group(label_FCC_vicini, img_FCC_vicini).arrange(DOWN, buff=0.5)

#         gruppo_vicini = Group(group_SC_vicini, group_FCC_vicini).arrange(RIGHT, buff=3)
#         gruppo_vicini.next_to(Crystal_model, DOWN, buff=0.4)

#         U_totale = MathTex(r"U_{TOT} = U_{LJ} + U_{TB}.", font_size=44)
#         U_totale.next_to(gruppo_vicini, DOWN, buff=0.7)
#         U_totale.set_x(0)

#         mostra(Crystal_model)
#         passo()
#         mostra(group_SC_vicini)
#         passo()
#         mostra(group_FCC_vicini)
#         passo()
#         mostra(U_totale)
#         fine()
#         nascondi(Crystal_model, group_SC_vicini, group_FCC_vicini, U_totale)

#         # --- slide 4: potenziale -----------------------------------
#         titolo6 = Tex("Potential", font_size=44).to_edge(UP)

#         notation_label = Tex(r"\textbf{$\gamma_w$}:", font_size=38)
#         notation_eq = MathTex(
#             r"""
#             \begin{aligned}
#             45^\circ \leftrightarrow w=1 &.\qquad 120^\circ \leftrightarrow w=4&.\\[0.2cm]
#             60^\circ \leftrightarrow w=2 &.\qquad 135^\circ \leftrightarrow w=5&.\\[0.2cm]
#             90^\circ \leftrightarrow w=3 &.\qquad 180^\circ \leftrightarrow w=6&.
#             \end{aligned}
#             """,
#             font_size=32,
#         )

#         notation_group = VGroup(notation_label, notation_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
#         notation_group.to_corner(UR, buff=0.3).shift(DOWN * 0.78, RIGHT * 0.3)

#         lj_label = Tex(r"\textbf{U$_{LJ}$}:", font_size=36)
#         lj_eq = MathTex(
#             r"""
#             U_{LJ}(r_{ij}) &= \sum_{\text{pairs }i j} V_{LJ}(r_{ij})
#             = \sum_{i=1}^N \left[ \frac{1}{2} \sum_{j<i} V_{LJ}(r_{ij}) \right] \\
#             V_{LJ}(r) &= 4\epsilon \left[
#             \left(\frac{\sigma}{r}\right)^{12}
#             - \left(\frac{\sigma}{r}\right)^{6}
#             \right].
#             """,
#             font_size=32,
#         )
#         lj_group = VGroup(lj_label, lj_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

#         tb_label = Tex(r"\textbf{U$_{TB}$}:", font_size=36)
#         tb_eq = MathTex(
#             r"""
#             U_{TB} &= \sum_{\substack{i,j,l \\ i<j<l}}
#             \gamma(\theta_{0ijl})
#             \left[1-\cos(\theta_{ijl}-\theta_{0ijl})\right] \\
#             &\equiv \sum_{\substack{i,j,l \\ i<j<l}}
#             \gamma_{w}
#             \left[1-\cos(\theta_{ijl}-\theta_{0ijl})\right].
#             """,
#             font_size=32,
#         )
#         tb_group = VGroup(tb_label, tb_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

#         potenziali = VGroup(lj_group, tb_group).arrange(DOWN, aligned_edge=LEFT, buff=1.0)

#         x_split = 1.0
#         larghezza_disp = x_split - (-config.frame_width / 2) - 0.4 - 0.3
#         altezza_disp = config.frame_height - 2
#         if potenziali.width > larghezza_disp:
#             potenziali.scale_to_fit_width(larghezza_disp)
#         if potenziali.height > altezza_disp:
#             potenziali.scale_to_fit_height(altezza_disp)
#         potenziali.to_edge(LEFT, buff=0.4)

#         L = 2.5
#         theta0 = 110 * DEGREES
#         theta = 120 * DEGREES
#         dir_i = np.array([1.0, 0.0, 0.0])

#         def rot(v, ang):
#             return np.array([
#                 v[0] * np.cos(ang) - v[1] * np.sin(ang),
#                 v[0] * np.sin(ang) + v[1] * np.cos(ang),
#                 0,
#             ])

#         shift_x = 1
#         C = np.array([x_split + (config.frame_width / 2 - x_split) / 2 - shift_x,
#                       tb_group.get_center()[1], 0])
#         J = C - np.array([0.5, 0.85, 0])
#         I = J + L * dir_i
#         L0 = J + L * rot(dir_i, theta0)

#         bond_ji = Line(J, I, color=BLACK)
#         bond_jl0 = DashedLine(J, L0, color=BLACK, dash_length=0.12)
#         arc0 = Angle(Line(J, I), Line(J, L0), radius=1, color=GRAY)
#         lab0 = MathTex(r"\theta_{0ijl}", font_size=28, color=GRAY).move_to(
#             J + 1.15 * rot(dir_i, theta0 / 3) + np.array([0.15, 0.1, 0]))
#         ghost = Dot(L0, color=PURPLE, radius=0.08).set_opacity(0.8)
#         dot_i = Dot(I, color=GREEN, radius=0.1)
#         dot_j = Dot(J, color=BLUE, radius=0.1)
#         name_i = MathTex("i", font_size=28).next_to(dot_i, DOWN, buff=0.12)
#         name_j = MathTex("j", font_size=28).next_to(dot_j, DOWN, buff=0.12)
#         name_l = MathTex("l", font_size=28).next_to(L0, UP, buff=0.12)

#         triplet_static = VGroup(bond_ji, bond_jl0, arc0, lab0, ghost,
#                                 dot_i, dot_j, name_i, name_j, name_l)

#         t = ValueTracker(theta0)
#         bond_jl = always_redraw(lambda: Line(
#             J, J + L * rot(dir_i, t.get_value()), color=RED))
#         dot_l = always_redraw(lambda: Dot(
#             J + L * rot(dir_i, t.get_value()), color=RED, radius=0.1))
#         arc = always_redraw(lambda: Angle(
#             Line(J, I), Line(J, J + L * rot(dir_i, t.get_value())),
#             radius=0.45, color=RED))
#         lab = always_redraw(lambda: MathTex(r"\theta_{ijl}", font_size=28, color=RED).move_to(
#             J + 0.8 * rot(dir_i, t.get_value() / 2)))
#         triplet_live = VGroup(bond_jl, dot_l, arc, lab)

#         mostra(titolo6)
#         passo()
#         mostra(notation_group)
#         passo()
#         mostra(lj_group)
#         passo()
#         mostra(tb_group)
#         passo()
#         mostra(triplet_static)
#         passo()
#         if PDF_MODE:
#             t.set_value(theta)          # direttamente lo stato finale
#             mostra(triplet_live)
#         else:
#             self.add(triplet_live)
#             self.play(t.animate.set_value(theta), run_time=2.5, rate_func=smooth)
#         fine()
#         nascondi(titolo6, lj_group, tb_group, notation_group, triplet_static, triplet_live)

#         # --- slide 5: densità di energia ---------------------------
#         Energy_density = Tex("Energy density", font_size=44).to_edge(UP)

#         epsilon_tensor = Tex(r"\textbf{$\epsilon$} :", font_size=40)
#         general_deformation = MathTex(r"""
#                       x' &= (1 + \epsilon_{xx}  )\hat{x} + \epsilon_{xy}\hat{y} + \epsilon_{xz}\hat{z}. \\
#                       y' &= \epsilon_{yx}\hat{x} + (1 + \epsilon_{yy}  )\hat{y} + \epsilon_{yz}\hat{z}. \\
#                       z' &= \epsilon_{zx}\hat{x} + \epsilon_{zy}\hat{y} + (1 + \epsilon_{zz})\hat{z}.
#                       """, font_size=32)

#         Gruppo_Gen_trasf = VGroup(epsilon_tensor, general_deformation).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         Gruppo_Gen_trasf.next_to(Energy_density, DOWN, buff=0.4)
#         Gruppo_Gen_trasf.to_edge(LEFT, buff=0.2)

#         r_to_rprimo = Tex(r"\textbf{$r \rightarrow r'$} :", font_size=40)

#         spostamento_R = Tex(
#             r"\textbf{$R = r' - r = \xi(r)\,\hat{x} + \psi(r)\,\hat{y} + \zeta(r)\,\hat{z}$}.",
#             font_size=40,
#         )

#         energy_density_mix = MathTex(
#             r"u\equiv",
#             r"u-u_0 = \frac{U}{V}",
#             r"=",
#             r"\frac{1}{2}\tilde{C}_{\lambda\mu}e_\lambda e_\mu.",
#             font_size=36,
#         )

#         energy_density_symm = MathTex(
#             r"=",
#             r"\frac{1}{2}C_{11}(e_{xx}^2 + e_{yy}^2 + e_{zz}^2)"
#             r"+ \frac{1}{2}C_{44}(e_{yz}^2 + e_{zx}^2 + e_{xy}^2)"
#             r"+ C_{12}(e_{yy}e_{zz} + e_{zz}e_{xx} + e_{xx}e_{yy}).",
#             font_size=36,
#         )

#         energy_density_mix.next_to(Gruppo_Gen_trasf, DOWN, buff=2)
#         energy_density_mix.to_edge(LEFT, buff=0.2)
#         energy_density_symm.next_to(energy_density_mix, DOWN, buff=0.3)

#         dx = energy_density_mix[0].get_center()[0] - energy_density_symm[0].get_center()[0]
#         energy_density_symm.shift(RIGHT * dx)

#         gruppo_spostamentoR = VGroup(r_to_rprimo, spostamento_R).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         gruppo_spostamentoR.next_to(Energy_density, DOWN, buff=0.4)
#         gruppo_spostamentoR.to_edge(RIGHT, buff=0.2)

#         C_matrix = MathTex(
#             r"""
#             C = \begin{bmatrix}
#             C_{11} & C_{12} & C_{12} & 0 & 0 & 0 \\
#             C_{12} & C_{11} & C_{12} & 0 & 0 & 0 \\
#             C_{12} & C_{12} & C_{11} & 0 & 0 & 0 \\
#             0 & 0 & 0 & C_{44} & 0 & 0 \\
#             0 & 0 & 0 & 0 & C_{44} & 0 \\
#             0 & 0 & 0 & 0 & 0 & C_{44}
#             \end{bmatrix}.
#             """,
#             font_size=40,
#         )

#         C_matrix.next_to(gruppo_spostamentoR, DOWN, buff=0.5)
#         C_matrix.shift(LEFT * 0.5)
#         C_matrix.shift(DOWN * 0.23)

#         start = Gruppo_Gen_trasf.get_bottom()
#         end = energy_density_mix.get_top()

#         freccia = Arrow(
#             start=start,
#             end=[start[0], end[1], 0],
#             buff=0.15,
#             color=BLUE,
#             stroke_width=5,
#         )

#         testo_freccia = Tex(r"$\epsilon \rightarrow e$", font_size=30, color=BLACK)
#         testo_freccia.next_to(freccia, RIGHT, buff=0.2)

#         mostra(Energy_density)
#         passo()
#         mostra(Gruppo_Gen_trasf)
#         passo()
#         mostra(gruppo_spostamentoR)
#         passo()
#         mostra(energy_density_mix)
#         passo()
#         mostra(freccia)
#         passo()
#         mostra(testo_freccia)
#         passo()
#         mostra(C_matrix)
#         passo()
#         mostra(energy_density_symm)
#         fine()
#         nascondi(Energy_density, Gruppo_Gen_trasf, gruppo_spostamentoR, energy_density_mix,
#                  energy_density_symm, C_matrix, freccia, testo_freccia)

#         # --- slide 6: costanti elastiche ---------------------------
#         titolo_costanti = Tex("Elastic constants", font_size=44).to_edge(UP)

#         primo_epsilon = MathTex(
#             r"""& \boldsymbol{-e_{xx} \neq 0} \\
#             & \rightarrow u(e_{xx}) = \frac{1}{2}C_{11}\,e_{xx}^2.""",
#             font_size=36,
#         )
#         secondo_epsilon = MathTex(
#             r"""&\boldsymbol{ -e_{xx}=e_{yy}=e \neq 0} \\
#             & \rightarrow u(e) = (C_{11}+C_{12})\,e^2.""",
#             font_size=36,
#         )
#         terzo_epsilon = MathTex(
#             r"""&\boldsymbol{ -e_{xy} \neq 0 }\\
#             & \rightarrow u(e_{xy}) = \frac{1}{2}C_{44}\,e_{xy}^2.""",
#             font_size=36,
#         )

#         epsilon_def = VGroup(primo_epsilon, secondo_epsilon, terzo_epsilon).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
#         epsilon_def.to_edge(LEFT, buff=0.3)
#         epsilon_def.next_to(titolo_costanti, DOWN, buff=0.4)
#         epsilon_def.to_edge(LEFT, buff=0.3)

#         Elastic_constants = MathTex(
#             r"""
#             \text{SC: } &
#             \begin{cases}
#             C^{SC}_{11}=\frac{1}{r_0^3}\left[72 \epsilon + 4(\gamma_{1}+\gamma_{2}+2\gamma_{3}+\gamma_{4}+\gamma_{5})\right]. \\[0.4cm]
#             C^{SC}_{12}=-\frac{2}{r_{0}^3}(\gamma_{1}+\gamma_{2}+2\gamma_{3}+\gamma_{4}+\gamma_{5}). \\[0.4cm]
#             C^{SC}_{44}=\frac{2}{r_{0}^3}\left(\gamma_{1}+2\gamma_{2}+6\gamma_{3}+2\gamma_{4}+\gamma_{5}\right).
#             \end{cases}
#             \\[1cm]
#             \text{FCC: } &
#             \begin{cases}
#             C^{FCC}_{11}=\frac{\sqrt{2}}{r_{0}^3}\left[72 \epsilon + 4(\gamma_{2}+2\gamma_{3}+\gamma_{4})\right]. \\[0.4cm]
#             C^{FCC}_{12}=\frac{\sqrt{2}}{r_{0}^3}\left[36 \epsilon - 2(\gamma_{2}+2\gamma_{3}+\gamma_{4})\right]. \\[0.4cm]
#             C^{FCC}_{44}=\frac{4\sqrt2}{r_{0}^3}\left(9\epsilon +\gamma_{2}+\gamma_{4}\right).
#             \end{cases}
#             """,
#             font_size=28,
#         )
#         Elastic_constants.to_edge(RIGHT, buff=0.3)

#         y = Elastic_constants.get_center()[1]

#         frecciac = Arrow(
#             start=[epsilon_def.get_right()[0], y, 0],
#             end=[Elastic_constants.get_left()[0], y, 0],
#             buff=0.2,
#             color=BLUE,
#             stroke_width=6,
#         )

#         mostra(titolo_costanti, epsilon_def)
#         passo()
#         mostra(Elastic_constants, frecciac)
#         fine()
#         nascondi(titolo_costanti, epsilon_def, Elastic_constants, frecciac)

#         # --- slide 7: velocità del suono ---------------------------
#         titolo_vel = Tex("Sound velocities", font_size=44).to_edge(UP)

#         eigenv = MathTex(
#             r"""
#             \rho\, v^2
#             \begin{bmatrix} \xi_0 \\ \psi_0 \\ \zeta_0 \end{bmatrix}
#             = \Gamma(\vec{n})
#             \begin{bmatrix} \xi_0 \\ \psi_0 \\ \zeta_0 \end{bmatrix}.
#             """,
#             font_size=36,
#         )

#         dynmat = MathTex(
#             r"""
#             \Gamma(\vec{n}) =
#             \begin{bmatrix}
#             C_{11}n_x^2 + C_{44}(n_y^2 + n_z^2) & (C_{12}+C_{44})n_x n_y & (C_{12}+C_{44})n_x n_z \\[0.3cm]
#             (C_{12}+C_{44})n_x n_y & C_{11}n_y^2 + C_{44}(n_x^2 + n_z^2) & (C_{12}+C_{44})n_y n_z \\[0.3cm]
#             (C_{12}+C_{44})n_x n_z & (C_{12}+C_{44})n_y n_z & C_{11}n_z^2 + C_{44}(n_x^2 + n_y^2)
#             \end{bmatrix}.
#             """,
#             font_size=30,
#         )

#         eigenv.next_to(titolo_vel, DOWN, buff=0.8)
#         dynmat.next_to(eigenv, DOWN, buff=1)
#         dynmat.set_x(0)
#         eigenv.set_x(0)

#         mostra(titolo_vel)
#         passo()
#         mostra(eigenv)
#         passo()
#         mostra(dynmat)
#         fine()
#         nascondi(eigenv, dynmat, titolo_vel)

#         # --- slide 8: direzioni speciali ---------------------------
#         titolo5 = Tex("Special directions", font_size=44).to_edge(UP)
#         img5 = ImageMobject("map_gamma_TL_analytic.png")

#         altezza_disp = config.frame_height - titolo5.height - 1.2
#         img5.scale_to_fit_height(altezza_disp)
#         if img5.width > 0.6 * config.frame_width:
#             img5.scale_to_fit_width(0.6 * config.frame_width)

#         img5.to_edge(RIGHT, buff=0.3)
#         img5.shift(UP * (titolo5.get_bottom()[1] - 0.3 - img5.get_top()[1]))

#         sc_label = Tex(r"\textbf{SC}:", font_size=38)
#         sc_eq = MathTex(
#             r"""\begin{array}{@{}l@{\quad}r@{\,:\,}l@{}}
#             {[1\,0\,0]} & T>L   & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_1+\gamma_5}{2} \\[2.5ex]
#             {[1\,1\,0]} & T_1>L & \gamma_3 < -18\,\epsilon - \dfrac{\gamma_1+\gamma_2+\gamma_4+\gamma_5}{2} \\[2.5ex]
#                         & T_2>L & \gamma_3 < -\dfrac{\gamma_2+\gamma_4}{4} \\[2.5ex]
#             {[1\,1\,1]} & T>L   & \gamma_3 < -\dfrac{\gamma_2+\gamma_4}{4}.
#             \end{array}""",
#             font_size=32,
#         )
#         sc_group = VGroup(sc_label, sc_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

#         fcc_label = Tex(r"\textbf{FCC}:", font_size=38)
#         fcc_eq = MathTex(
#             r"""\begin{array}{@{}l@{\quad}r@{\,:\,}l@{}}
#             {[1\,0\,0]} & T>L   & \gamma_3 < -\dfrac{9}{2}\,\epsilon \\[2.5ex]
#             {[1\,1\,0]} & T_1>L & \gamma_3 < -27\,\epsilon - \dfrac{\gamma_2+\gamma_4}{2} \\[2.5ex]
#                         & T_2>L & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_2+\gamma_4}{2} \\[2.5ex]
#             {[1\,1\,1]} & T>L   & \gamma_3 > 18\,\epsilon + \dfrac{\gamma_2+\gamma_4}{2}\,.
#             \end{array}""",
#             font_size=32,
#         )
#         fcc_group = VGroup(fcc_label, fcc_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

#         relazioni_speciali = VGroup(sc_group, fcc_group).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

#         larghezza_disp = img5.get_left()[0] - (-config.frame_width / 2) - 0.4 - 0.3
#         if relazioni_speciali.width > larghezza_disp:
#             relazioni_speciali.scale_to_fit_width(larghezza_disp)
#         if relazioni_speciali.height > altezza_disp:
#             relazioni_speciali.scale_to_fit_height(altezza_disp)

#         relazioni_speciali.to_edge(LEFT, buff=0.4)
#         relazioni_speciali.match_y(img5)

#         mostra(titolo5)
#         passo()
#         mostra(img5)
#         passo()
#         mostra(sc_group)
#         passo()
#         mostra(fcc_group)
#         fine()
#         nascondi(titolo5, sc_group, fcc_group, img5)

#         # --- slide 9: mappe ----------------------------------------
#         titolo3 = Tex(r"General $\vec{q}$ phase diagrams", font_size=44).to_edge(UP)

#         img3 = ImageMobject("map_gamma_SC_TL.png")
#         img4 = ImageMobject("map_gamma_FCC_TL.png")

#         immagini = Group(img3, img4).arrange(RIGHT, buff=0.1)
#         immagini.scale_to_fit_height(6.6)
#         if immagini.width > config.frame_width - 0.6:
#             immagini.scale_to_fit_width(config.frame_width - 0.6)
#         immagini.next_to(titolo3, DOWN, buff=0.2)
#         immagini.shift(LEFT * 0.02)

#         mostra(titolo3)
#         passo()
#         mostra(img3)
#         passo()
#         mostra(img4)
#         fine()
#         nascondi(titolo3, img3, img4)

#         # --- slide 10: frazione di direzioni -----------------------
#         titolo2 = Tex("Fraction of directions", font_size=44).to_edge(UP)

#         img1 = ImageMobject("color_map_gamma_SC_TL_shared.png")
#         img2 = ImageMobject("color_map_gamma_FCC_TL_shared.png")

#         immagini = Group(img1, img2).arrange(DOWN, buff=0.2)
#         immagini.scale_to_fit_height(6.6)
#         if immagini.width > config.frame_width - 0.6:
#             immagini.scale_to_fit_width(config.frame_width - 0.6)
#         immagini.next_to(titolo2, DOWN, buff=0.2)

#         label_SC = Tex(r"\textbf{SC:}", font_size=38)
#         label_FCC = Tex(r"\textbf{FCC:}", font_size=38)

#         label_SC.next_to(img1, LEFT, buff=0.3)
#         label_FCC.next_to(img2, LEFT, buff=0.3)
#         label_FCC.align_to(label_SC, RIGHT)

#         mostra(titolo2)
#         passo()
#         mostra(img1, label_SC)
#         passo()
#         mostra(img2, label_FCC)
#         fine()
#         nascondi(titolo2, img1, img2, label_SC, label_FCC)

#         # --- slide 11: campionamento della sfera -------------------
#         titolo4 = Tex("Random sampling of the unit sphere", font_size=44).to_edge(UP)
#         N = 60
#         frames = [np.array(Image.open(f"frames/f_{i:03d}.png").convert("RGBA"))
#                   for i in range(N)]

#         def immagine(i):
#             img = ImageMobject(frames[i]).scale_to_fit_height(5.6)
#             img.next_to(titolo4, DOWN, buff=0.1)
#             return img

#         if PDF_MODE:
#             corrente = immagine(N - 1)      # direttamente l'ultimo frame
#             mostra(titolo4, corrente)
#         else:
#             corrente = immagine(0)
#             mostra(titolo4, corrente)
#             self.next_slide()               # click: parte la crescita

#             durata = 2.5
#             for i in range(1, N):
#                 nuovo = immagine(i)
#                 self.remove(corrente)
#                 self.add(nuovo)
#                 corrente = nuovo
#                 self.wait(durata / N)

#             self.next_slide()               # click: mostra i parametri

#         def x_pannello(frac):
#             return corrente.get_left()[0] + frac * corrente.width

#         par_sc = Tex(r"$\gamma_1 = \gamma_5 = 1.$\\$\gamma_3 = 50.$", font_size=32)
#         par_fcc = Tex(r"$\gamma_2 = \gamma_4 = 1.$\\$\gamma_3 = 50.$", font_size=32)

#         y = corrente.get_bottom()[1] + 0.2
#         par_sc.move_to([x_pannello(0.22), y, 0], aligned_edge=UP)
#         par_fcc.move_to([x_pannello(0.66), y, 0], aligned_edge=UP)

#         mostra(par_sc, par_fcc)
#         fine()
#         nascondi(corrente, titolo4, par_sc, par_fcc)

#         # --- slide 12: conclusioni ---------------------------------
#         titolo_concl = Tex("Conclusions", font_size=44).to_edge(UP)

#         concl = VGroup(
#             Tex(r"$\bullet$ In the adopted model, regions of the parameter space", font_size=34),
#             Tex(r"\phantom{$\bullet$} where the velocity inversion occurs have been found", font_size=34),
#             Tex(r"$\bullet$ No region was found where $v_L < v_{T_1}, v_{T_2}$", font_size=34),
#             Tex(r"\phantom{$\bullet$} for every propagation direction simultaneously", font_size=34),
#         )
#         concl.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
#         concl[2].shift(DOWN * 0.3)
#         concl[3].shift(DOWN * 0.3)
#         concl.next_to(titolo_concl, DOWN, buff=0.8)
#         concl.to_edge(LEFT, buff=0.8)

#         mostra(titolo_concl)
#         passo()
#         mostra(concl[0], concl[1])
#         passo()
#         mostra(concl[2], concl[3])
#         fine()
#         nascondi(titolo_concl, concl[0], concl[1], concl[2], concl[3])

#         # --- slide 13: sviluppi futuri -----------------------------
#         titolo_fine = Tex("Future developments", font_size=44).to_edge(UP)

#         punti = VGroup(
#             Tex(r"$\bullet$ Extend the analysis to other lattices, starting from BCC", font_size=34),
#             Tex(r"$\bullet$ Add second-neighbor angular terms for FCC, as done for SC", font_size=34),
#             Tex(r"$\bullet$ Enlarge the parameter space: independent parameters", font_size=34),
#             Tex(r"\phantom{$\bullet$} for each non-equivalent angular term", font_size=34),
#             Tex(r"$\bullet$ Replace fixed neighbor lists with a flexible force field", font_size=34),
#             Tex(r"\phantom{$\bullet$} (distances and angles on the fly, Stillinger-Weber style)", font_size=34),
#         )
#         punti.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
#         punti.next_to(titolo_fine, DOWN, buff=0.8)
#         punti.to_edge(LEFT, buff=0.8)

#         mostra(titolo_fine)
#         passo()
#         mostra(punti[0])
#         passo()
#         mostra(punti[1])
#         passo()
#         mostra(punti[2], punti[3])
#         passo()
#         mostra(punti[4], punti[5])
#         fine()
#         nascondi(titolo_fine, punti)