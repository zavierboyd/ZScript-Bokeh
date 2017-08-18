spring = ''';; constant ;; values for this simulation
                dt = 0.001 ;;(1/210)
                ks := 6.83 ;; Spring Tension
                L0 := 0.1 ;; 0.123
                g := (0, -9.81)
                Mball := 0.402
                Xspring := (0, 0) ;;(-0.007, -0.0050)

            ;; initial values
                Xball := (0.108, -0.763)
                Vball := (0, 0) ;;(0.18, 0)*10
                ;;Vball := 50 * (1, 1) ;; throw it super hard to start the weight/spring spinning around
                p := Vball*Mball
                t := 0
                dLdt := 0
                Kfs := 1*2*(ks*Mball)^(1/2)  ;; optimal damping of spring
                Kfa := 0.01  ;; small air resistance

            ;; calculated values - current values, not 'next' values
                L = Xball - Xspring
                Lmag = mag L
                Lh = L/Lmag
                stretch = Lmag - L0
                Fs = -ks*stretch*Lh
                Ffs = -Kfs*dLdt*Lh ;; in the direction of the spring, against the spring movement
                Ffa = -Kfa*Vball ;; in the direction against velocity
                Fg = Mball*g
                Fnet = Fs + Fg + Ffs + Ffa;; take off friction for coolness
                Vball = p / Mball

            ;; next time step (create 'next' values)
                dLdt_ = (Lmag_ - Lmag)/dt  ;; differentiate length
                p_ = p + Fnet*dt  ;; momentum = integral of force
                Xball_ = Xball + Vball_*dt  ;; position = integral of velocity
                t_ = t + 1*dt  ;; Integrate time by a constant

            ;; run simulation
                trace t
                trace Xball'''

pendulum = ''';; constant ;; values for this simulation
                dt := 0.00033
                ks := 3000;;6.83 ;; Pendulum Tension
                length := 0.1 ;; 0.123
                g := (0, -9.81)
                Mball := 0.402
                Xspring := (0, 0) ;;(-0.007, -0.0050)

            ;; initial values
                angle := (1, 0)
                direction := angle / (mag angle)
                Xball := direction * L0 ;;(0.108, -0.763)
                Vball := (0, 0) ;;(0.18, 0)*10
                ;;Vball := 50 * (1, 1) ;; throw it super hard to start the weight/spring spinning around
                p := Vball*Mball
                t := 0
                dLdt := 0
                Kfs := 1*2*(ks*Mball)^(1/2)  ;; optimal damping of spring
                Kfa := 0.01  ;; small air resistance

            ;; calculated values - current values, not 'next' values
                L = Xball - Xspring
                Lmag = mag L
                Lh = L/Lmag
                stretch = Lmag - L0
                Fs = -ks*stretch*Lh
                Ffs = -Kfs*dLdt*Lh ;; in the direction of the spring, against the spring movement
                Ffa = -Kfa*Vball ;; in the direction against velocity
                Fg = Mball*g
                Fnet = Fs + Fg + Ffs ;;+ Ffa;; take off friction for coolness
                Vball = p / Mball

            ;; next time step (create 'next' values)
                dLdt_ = (Lmag_ - Lmag)/dt  ;; differentiate length
                p_ = p + Fnet*dt  ;; momentum = integral of force
                Xball_ = Xball + Vball_*dt  ;; position = integral of velocity
                t_ = t + 1*dt  ;; Integrate time by a constant

            ;; run simulation
                trace t
                trace Xball'''

# length | time^2       | measured
# 0.1    | 0.52 - 0.59  | 0.41
# 0.5    | 2.29         | 2.03
# 0.7    | 3.15 - 3.24  | 2.93

def serialize(n):
    nd = {}
    for var, val in n:
        if type(val) in (complex,):
            nd[var+'x'] = [val.real]
            nd[var+'y'] = [val.imag]
        else:
            nd[var] = [val]

    return nd
