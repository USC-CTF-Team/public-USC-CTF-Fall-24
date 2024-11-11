# unpopcorn

Author: neonlian

Category: crypto

## Solution

You are given an encoded message and the python script that encoded the message. 

This is what each function in `encoder.py` does:
* pop - XORs each character of the input message with 42
* butter - Outputs `x * p % m` where `x` is a character/number passed into the function, `p` is an unknown number, and `m = 57983`
* churn
  * Bit shifts all values left by 3 places
  * Rotates the order of the list by 16 places
  * Outputs the final list as a string of hexadecimal numbers

To decode the message we need to reverse each of these functions.

First, read the hexadecimal values and reverse the list rotate and bit shift operations:
```python
def unchurn(hex_str_list):
    decimal_ints = list(map(lambda x: int(x, 16), hex_str_list))
    unrotated = decimal_ints[-16:] + decimal_ints[:-16]
    return list(map(lambda x: (x >> 3), unrotated))
```

The next step is to reverse the `x * p % m` operation. To reverse this, we need to find the [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) to multiply with `p` to get the original `x`. Represented mathematically, let $e$ be our encoded number and $p^{-1}$ be the inverse:

$$
\begin{align*}
x \cdot p &\equiv e &\pmod m \\
x \cdot p \cdot p^{-1} &\equiv e \cdot p^{-1} &\pmod m \\
x &\equiv e \cdot p^{-1} &\pmod m
\end{align*}
$$

We do not have the value of `p` to be able to calculate `p_inverse` directly. However, because `m` is small, we can brute force all possible values of `p_inverse` from 1 to 57983. 

Below is code to try all `p_inverse` values to reverse the `butter` and `pop` functions. It detects if a `p_inverse` is correct by seeing if all remaining bytes are valid ascii characters.
```python
def unbutterpop(ints):
    for p_inv in range(1, m+1):
        unbuttered = list(map(lambda x: x * p_inv % m, ints))
        unxored = list(map(lambda x: x ^ 42, unbuttered))
        try:
            possible_flag = bytes(unxored)
            flag = possible_flag.decode('ascii')
            print(flag)
        except (ValueError, UnicodeDecodeError):
            pass
```