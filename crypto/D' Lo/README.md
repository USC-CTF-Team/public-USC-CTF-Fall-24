# D' Lo

author: RJCyber

category: crypto

## Solve script

solve.sage
```python
from Crypto.Util.number import *
def recover_p_low(p_low, n):
        p_bits = (len(bin(n))-2)//2
        p_low_bits = len(bin(p_low)) - 2
        PR.<x> = PolynomialRing(Zmod(n))
        f = x * 2**p_low_bits + p_low
        x = f.monic().small_roots(X=2**(p_bits-p_low_bits), beta=0.4)
        if x == []:
                return None
        p = int(f(x[0]))
        return p

def recover(d_low, n, e):
    t = len(bin(d_low)) - 2
    for k in (range(1, e+1)):
        x = var('x')
        for r in solve_mod([x*e*d_low == x + k*(n*x - x**2 - n + x)], 2**t):
            p_low = int(r[0])
            try:
                p = recover_p_low(p_low, n)
                if p is not None:
                    return p
            except:
                continue

e = 7
n = 9537465719795794225039144316914692273057528543708841063782449957642336689023241057406145879616743252508032700675419312420008008674130918587435719504215151
c = 4845609252254934006909399633004175203346101095936020726816640779203362698009821013527198357879072429290619840028341235069145901864359947818105838016519415
d_low = 0xb9b24053029f5f424adc9278c750b42b0b2a134b0a52f13676e94c01ef77

p = recover(d_low, n, e)
q = n//p
d = pow(e, -1, (p-1)*(q-1))
print(long_to_bytes(int(pow(c,d,n))))
#CYBORG{H0w_w3ll_d0_y0u_th1nk_d'lo_w1ll_d0_7h15_53ason??}
```