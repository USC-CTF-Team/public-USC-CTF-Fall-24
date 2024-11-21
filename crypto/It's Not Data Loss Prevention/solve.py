from Crypto.Util.number import *
from sympy.ntheory.residue_ntheory import n_order, _discrete_log_trial_mul
from sympy.ntheory.factor_ import factorint
from sympy.ntheory.modular import crt

def _discrete_log_pohlig_hellman(n, a, b, factors):
    f = factors
    l = [0] * len(f)
    a %= n
    b %= n
    order = n - 1
    for i, (pi, ri) in enumerate(f.items()):
        print(f"factor {pi}...")
        for j in range(ri):
            gj = pow(b, l[i], n)
            aj = pow(a * pow(gj, -1, n), order // pi**(j + 1), n)
            bj = pow(b, order // pi, n)
            cj = _discrete_log_trial_mul(n, aj, bj, pi)
            l[i] += cj * pi**j

    d, _ = crt([pi**ri for pi, ri in f.items()], l)
    return d

p = 72582273207584409523836416205503873456840672244861668902068962428022358668644213717033410220094858213785909158082084409697781833525734642650576180002727864094178853739590888445753712196268567738582111704293273201721006648707008913242412196989487167851968618303659742648153352883917176492356546118351747721810800909873736282570227177961197335450387989276806079489
g = 3
a = 24393771488717960431147269064624631828310604373526026598603386491263061338072489803153972728250242949112187407825532440328751180404635401465476512488685185622725060580628770654048867200033806585934697471249921972700552978079752695585970921337459580789152970187925768085334409084092041192304935279345047595337816976845617649400223935358270007572542969925561362228
flag = _discrete_log_pohlig_hellman(p, a, g, {2:10, 787:4, 32587:3 , 708667:7})
flag = long_to_bytes(flag)
print(flag)
#CYBORG{p0hl1g_h3llm4n_f7w!!}
#implementation from: https://connor-mccartney.github.io/cryptography/diffie-hellman/logloglog-Angstrom-CTF-2022
