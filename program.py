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


spring_adaptive = ''';; constant ;; values for this simulation
                dt := 0.00001 ;;(1/210)
                ks := 6.83 ;; Spring Tension
                L0 := 0.1 ;; 0.123
                g := (0, -9.81)
                Mball := 0.402
                Xspring := (0, 0) ;;(-0.007, -0.0050)

            ;; initial values
                x := (0.108, -0.763)
                v := (0, 0) ;;(0.18, 0)*10
                ;;v := 50 * (1, 1) ;; throw it super hard to start the weight/spring spinning around
                p := v*Mball
                t := 0
                dLdt := 0
                Kfs := 1*2*(ks*Mball)^(1/2)  ;; optimal damping of spring
                Kfa := 0.01  ;; small air resistance

            ;; calculated values - current values, not 'next' values
                L = x - Xspring
                Lmag = mag L
                Lh = L/Lmag
                stretch = Lmag - L0
                Fs = -ks*stretch*Lh
                Ffs = -Kfs*dLdt*Lh ;; in the direction of the spring, against the spring movement
                Ffa = -Kfa*v ;; in the direction against velocity
                Fg = Mball*g
                Fnet = Fs + Fg + Ffs + Ffa;; take off friction for coolness
                ;; v = p / Mball

            ;; next time step (create 'next' values)
                dLdt_ = (Lmag_ - Lmag)/dt  ;; differentiate length
                ;; p_ = p + Fnet*dt  ;; momentum = integral of force
                ;; x_ = x + v_*dt  ;; position = integral of velocity
                t_ = t + dt  ;; Integrate time by a constant


a = Fnet/Mball
p = v/Mball

x_ = x + v*dt + 0.5*a*dt^2
v_ = v + 0.5(a + a_)dt

;; setting up constants
phi = (1 + 5^0.5)/2
up-factor = phi
down-factor = 1 / phi

work = Fnet * v * dt
max-error := 0.1
potential-error := 0
potential-error_ =  mag (work_ - work)
too-big = potential-error > max-error
big-count := 0
big-count_ = (big-count + 1) * too-big
dt-up = NOT too-big AND big-count < 3  ;; AND bounce-count < 8
dt-factor = dt-up * up-factor + (not dt-up)*down-factor
dt_ = dt*dt-factor_

;; bounceCount_ = (bounce-count + 1) * (too-big != too-big_)



            ;; run simulation
                trace t
                trace x'''

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
