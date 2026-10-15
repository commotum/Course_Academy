# Source and generated review

Originals come from frozen basis2275; source payloads and key omissions remain in source.json.


## Original q-127270

Find $By$ if 
$B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}$
and
$y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$


Source selection: $\begin{bmatrix}a \\ a-b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ 2a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a-b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$


## Original q-13554

Find $Ax$ if
$A = \begin{bmatrix}a & c \\ b & d\end{bmatrix}$
and
$x = \begin{bmatrix}1 \\ 2\end{bmatrix}$.

[Original worked solution absent; repaired replay is separately labeled.]


Source selection: $\begin{bmatrix}a + c \\ b + 2d\end{bmatrix}$; $\begin{bmatrix}a + 2c \\ 2b + 2d\end{bmatrix}$; $\begin{bmatrix}2a + 2c \\ b + 2d\end{bmatrix}$; $\begin{bmatrix}a + 2c \\ b + 2d\end{bmatrix}$; $\begin{bmatrix}a + 2c \\ b + d\end{bmatrix}$


## Original q-127276

Find $Mz$ if 
$M=\begin{bmatrix}s & t \\ -t & s\end{bmatrix}$
and
$z=\begin{bmatrix}s \\ t\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}s & t \\ -t & s\end{bmatrix}\begin{bmatrix}s \\ t\end{bmatrix} \\  & =\begin{bmatrix}s\cdot s+t\cdot t \\ (-t)\cdot s+s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}{s}^{2}+{t}^{2} \\ -st+st\end{bmatrix} \\  & =\begin{bmatrix}{s}^{2}+{t}^{2} \\ 0\end{bmatrix}\end{aligned}
$$


Source selection: $\begin{bmatrix}(s+t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}{s}^{2}+{t}^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}(s-t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}{s}^{2}+{t}^{2} \\ -2st\end{bmatrix}$; $\begin{bmatrix}(s+t)^{2} \\ -2st\end{bmatrix}$


## Original q-127277

Find $Qg$ if 
$Q=\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}$
and
$g=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qg & =\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}\begin{bmatrix}-2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}m\cdot (-2)+2m\cdot 3 \\ -m\cdot (-2)+n\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}-2m+6m \\ 2m+3n\end{bmatrix} \\  & =\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}\end{aligned}
$$


Source selection: $\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+3n\end{bmatrix}$; $\begin{bmatrix}4m \\ m+n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+n\end{bmatrix}$; $\begin{bmatrix}4m \\ 2m+n\end{bmatrix}$


## Original q-275597

If 
$Q=\begin{bmatrix}a & b & a \\ a & -b & a \\ 0 & 0 & a\end{bmatrix}$
and
$r=\begin{bmatrix}a \\ 0 \\ -a\end{bmatrix},$
find $Qr.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Qr=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qr & =\begin{bmatrix}a & b & a \\ a & -b & a \\ 0 & 0 & a\end{bmatrix}\begin{bmatrix}a \\ 0 \\ -a\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}a\cdot a & + & \,\,\,\,\,\,\,b\cdot 0 & + & a\cdot (-a) \\ a\cdot a & + & (-b)\cdot 0 & + & a\cdot (-a) \\ 0\cdot a & + & \,\,\,\,\,\,\,0\cdot 0 & + & a\cdot (-a)\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}{a}^{2} & + & 0 & + & (-{a}^{2}) \\ {a}^{2} & + & 0 & + & (-{a}^{2}) \\ 0 & + & 0 & + & (-{a}^{2})\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -{a}^{2}\end{bmatrix}\end{aligned}
$$


Source field-3: $-{a}^{2}$


Source field-2: $0$


Source field-1: $0$


## Original q-318589

If 
$A=\begin{bmatrix}b & a & -b \\ -b & a & b \\ -b & 0 & -b\end{bmatrix}$
and
$x=\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix},$
find $Ax.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Ax=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}b & a & -b \\ -b & a & b \\ -b & 0 & -b\end{bmatrix}\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}b\cdot (-b) & + & a\cdot 0 & + & (-b)\cdot b \\ (-b)\cdot (-b) & + & a\cdot 0 & + & \,\,\,\,\,\,b\cdot b \\ (-b)\cdot (-b) & + & 0\cdot 0 & + & (-b)\cdot b\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}-{b}^{2} & + & 0 & + & (-{b}^{2}) \\ {b}^{2} & + & 0 & + & {b}^{2} \\ {b}^{2} & + & 0 & + & (-{b}^{2})\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-2{b}^{2} \\ 2{b}^{2} \\ 0\end{bmatrix}.\end{aligned}
$$


Source field-3: $0$


Source field-1: $-2{b}^{2}$


Source field-2: $2{b}^{2}$


## Original q-318591

If 
$P=\begin{bmatrix}m & n & -m \\ m & -n & -m \\ 0 & 2 & 0\end{bmatrix}$
and
$u=\begin{bmatrix}1 \\ p \\ 1\end{bmatrix},$
find $Pu.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Pu=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pu & =\begin{bmatrix}m & n & -m \\ m & -n & -m \\ 0 & 2 & 0\end{bmatrix}\begin{bmatrix}1 \\ p \\ 1\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}m\cdot 1 & + & \,\,\,\,\,\,\,n\cdot p & + & (-m)\cdot 1 \\ m\cdot 1 & + & (-n)\cdot p & + & (-m)\cdot 1 \\ 0\cdot 1 & + & \,\,\,\,\,\,\,2\cdot p & + & \,\,\,\,\,\,\,\,\,0\cdot 1\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}m & + & \,\,\,\,\,np & + & (-m) \\ m & + & (-np) & + & (-m) \\ 0 & + & \,\,\,\,\,2p & + & 0\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}np \\ -np \\ 2p\end{bmatrix}.\end{aligned}
$$


Source field-3: $2p$


Source field-1: $np$


Source field-2: $-np$


## Original q-318595

Find $By$  if 
$B=\begin{bmatrix}6p & -4q \\ -5p & 2q\end{bmatrix}$
and
$y=\begin{bmatrix}p \\ q\end{bmatrix}.$

| $By=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}6p & -4q \\ -5p & 2q\end{bmatrix}\begin{bmatrix}p \\ q\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}6p\cdot p & + & (-4q)\cdot q \\ -5p\cdot p & + & \,\,\,\,\,\,\,2q\cdot q\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}6{p}^{2}-4{q}^{2} \\ -5{p}^{2}+2{q}^{2}\end{bmatrix}.\end{aligned}
$$


Source field-2: $-5{p}^{2}+2{q}^{2}$


Source field-1: $6{p}^{2}-4{q}^{2}$


## Original q-70226

Find $Tu$ if 
$T=\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}$
and
$u=\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Tu & =\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix} \\  & =\begin{bmatrix}x\cdot x+y\cdot 0+x\cdot (-x) \\ x\cdot x+(-y)\cdot 0+x\cdot (-x) \\ (-x)\cdot x+(-y)\cdot 0+x\cdot (-x)\end{bmatrix} \\  & =\begin{bmatrix}{x}^{2}+0-{x}^{2} \\ {x}^{2}+0-{x}^{2} \\ -{x}^{2}+0-{x}^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -2{x}^{2}\end{bmatrix}\end{aligned}
$$


Source selection: $\begin{bmatrix}0 \\ 0 \\ -2{x}^{2}\end{bmatrix}$; $\begin{bmatrix}{x}^{3}y \\ 0 \\ -{x}^{3}y\end{bmatrix}$; $\begin{bmatrix}{x}^{2}y \\ 0 \\ -{x}^{2}y\end{bmatrix}$; $\begin{bmatrix}{x}^{2} \\ -{x}^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}{x}^{2} \\ 0 \\ -{x}^{2}\end{bmatrix}$


## Original q-13556

Find $By$  if 
$B=\begin{bmatrix}b & b \\ c & c\end{bmatrix}$
and
$y=\begin{bmatrix}3 \\ 4\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product: 

$$
\begin{aligned}By & =\begin{bmatrix}b & b \\ c & c\end{bmatrix}\begin{bmatrix}3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}b\cdot 3+b\cdot 4 \\ c\cdot 3+c\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}3b+4b \\ 3c+4c\end{bmatrix} \\  & =\begin{bmatrix}7b \\ 7c\end{bmatrix}\end{aligned}
$$


Source selection: $\begin{bmatrix}-7b \\ -7c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7c\end{bmatrix}$; $\begin{bmatrix}7b \\ 7c\end{bmatrix}$; $\begin{bmatrix}7b \\ 7b\end{bmatrix}$; $\begin{bmatrix}7c \\ 7b\end{bmatrix}$


## Generated q-127270 observed 0

Find $By$ if 
$B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}$
and
$y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.$


selection: $\begin{bmatrix}a \\ a-b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ 2a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a-b \\ a+b\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$


## Generated q-127270 observed 1

Find $By$ if 
$B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}$
and
$y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.$


selection: $\begin{bmatrix}a \\ a-b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ 2a+b\end{bmatrix}$; $\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a-b \\ a+b\end{bmatrix}$; $\begin{bmatrix}3a \\ a+b \\ a+b\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$


## Generated q-127270 authored-operations 0

Find $By$ if 
$B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}$
and
$y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.$


selection: $\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}-a \\ -a-b \\ -a-b\end{bmatrix}$; $\begin{bmatrix}2a \\ a+2b \\ 2a+b\end{bmatrix}$; $\begin{bmatrix}a \\ a-b \\ 3a-b\end{bmatrix}$; $\begin{bmatrix}0 \\ b \\ -a+b\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$


## Generated q-127270 authored-operations 1

Find $By$ if 
$B=\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}$
and
$y=\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}.$


selection: $\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$; $\begin{bmatrix}-a \\ -a-b \\ -a-b\end{bmatrix}$; $\begin{bmatrix}a \\ a-b \\ 3a-b\end{bmatrix}$; $\begin{bmatrix}0 \\ b \\ -a+b\end{bmatrix}$; $\begin{bmatrix}2a \\ a+2b \\ 2a+b\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}a & -a & a \\ a & -2b & b \\ 2a & -b & a\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}a\cdot 1+(-a)\cdot (-1)+a\cdot (-1) \\ a\cdot 1+(-2b)\cdot (-1)+b\cdot (-1) \\ 2a\cdot 1+(-b)\cdot (-1)+a\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}a+a-a \\ a+2b-b \\ 2a+b-a\end{bmatrix} \\  & =\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}\end{aligned}
$$


## Generated q-13554 observed 0

Find $Ax$ if
$A = \begin{bmatrix}2a & 3c \\ b & 3d\end{bmatrix}$
and
$x = \begin{bmatrix}3 \\ 2\end{bmatrix}$.


selection: $\begin{bmatrix}6a+6c \\ 3b+3d\end{bmatrix}$; $\begin{bmatrix}4a+6c \\ 3b+6d\end{bmatrix}$; $\begin{bmatrix}6a+6c \\ 2b+6d\end{bmatrix}$; $\begin{bmatrix}6a+3c \\ 3b+6d\end{bmatrix}$; $\begin{bmatrix}6a+6c \\ 3b+6d\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}2a & 3c \\ b & 3d\end{bmatrix}\begin{bmatrix}3 \\ 2\end{bmatrix} \\ & =\begin{bmatrix}2a\cdot 3+3c\cdot 2 \\ b\cdot 3+3d\cdot 2\end{bmatrix} \\ & =\begin{bmatrix}6a+6c \\ 3b+6d\end{bmatrix}\end{aligned}
$$


## Generated q-13554 observed 1

Find $Ax$ if
$A = \begin{bmatrix}2a & c \\ 2b & d\end{bmatrix}$
and
$x = \begin{bmatrix}2 \\ 3\end{bmatrix}$.


selection: $\begin{bmatrix}4a+3c \\ 4b+3d\end{bmatrix}$; $\begin{bmatrix}4a+c \\ 4b+3d\end{bmatrix}$; $\begin{bmatrix}4a+3c \\ 6b+3d\end{bmatrix}$; $\begin{bmatrix}6a+3c \\ 4b+3d\end{bmatrix}$; $\begin{bmatrix}4a+3c \\ 4b+d\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}2a & c \\ 2b & d\end{bmatrix}\begin{bmatrix}2 \\ 3\end{bmatrix} \\ & =\begin{bmatrix}2a\cdot 2+c\cdot 3 \\ 2b\cdot 2+d\cdot 3\end{bmatrix} \\ & =\begin{bmatrix}4a+3c \\ 4b+3d\end{bmatrix}\end{aligned}
$$


## Generated q-127276 observed 0

Find $Mz$ if 
$M=\begin{bmatrix}2s & t \\ -t & 2s\end{bmatrix}$
and
$z=\begin{bmatrix}2s \\ t\end{bmatrix}.$


selection: $\begin{bmatrix}(2s+t)^{2} \\ -4st\end{bmatrix}$; $\begin{bmatrix}(2s+t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}4s^{2}+t^{2} \\ -4st\end{bmatrix}$; $\begin{bmatrix}(2s-t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}4s^{2}+t^{2} \\ 0\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}2s & t \\ -t & 2s\end{bmatrix}\begin{bmatrix}2s \\ t\end{bmatrix} \\  & =\begin{bmatrix}2s\cdot 2s+t\cdot t \\ (-t)\cdot 2s+2s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}4s^{2}+t^{2} \\ -2st+2st\end{bmatrix} \\  & =\begin{bmatrix}4s^{2}+t^{2} \\ 0\end{bmatrix}\end{aligned}
$$


## Generated q-127276 observed 1

Find $Mz$ if 
$M=\begin{bmatrix}s & t \\ -t & s\end{bmatrix}$
and
$z=\begin{bmatrix}s \\ t\end{bmatrix}.$


selection: $\begin{bmatrix}(s+t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}s^{2}+t^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}(s+t)^{2} \\ -2st\end{bmatrix}$; $\begin{bmatrix}(s-t)^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}s^{2}+t^{2} \\ -2st\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}s & t \\ -t & s\end{bmatrix}\begin{bmatrix}s \\ t\end{bmatrix} \\  & =\begin{bmatrix}s\cdot s+t\cdot t \\ (-t)\cdot s+s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}s^{2}+t^{2} \\ -st+st\end{bmatrix} \\  & =\begin{bmatrix}s^{2}+t^{2} \\ 0\end{bmatrix}\end{aligned}
$$


## Generated q-127276 authored-operations 0

Find $Mz$ if 
$M=\begin{bmatrix}2s & t \\ -t & 2s\end{bmatrix}$
and
$z=\begin{bmatrix}2s \\ t\end{bmatrix}.$


selection: $\begin{bmatrix}4st \\ 4s^{2}-t^{2}\end{bmatrix}$; $\begin{bmatrix}4s^{2}+t^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}4s^{2} \\ -2st\end{bmatrix}$; $\begin{bmatrix}t^{2} \\ 2st\end{bmatrix}$; $\begin{bmatrix}-4s^{2}-t^{2} \\ 0\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}2s & t \\ -t & 2s\end{bmatrix}\begin{bmatrix}2s \\ t\end{bmatrix} \\  & =\begin{bmatrix}2s\cdot 2s+t\cdot t \\ (-t)\cdot 2s+2s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}4s^{2}+t^{2} \\ -2st+2st\end{bmatrix} \\  & =\begin{bmatrix}4s^{2}+t^{2} \\ 0\end{bmatrix}\end{aligned}
$$


## Generated q-127276 authored-operations 1

Find $Mz$ if 
$M=\begin{bmatrix}s & t \\ -t & s\end{bmatrix}$
and
$z=\begin{bmatrix}s \\ t\end{bmatrix}.$


selection: $\begin{bmatrix}s^{2}+t^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}-s^{2}-t^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}2st \\ s^{2}-t^{2}\end{bmatrix}$; $\begin{bmatrix}t^{2} \\ st\end{bmatrix}$; $\begin{bmatrix}s^{2} \\ -st\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Mz & =\begin{bmatrix}s & t \\ -t & s\end{bmatrix}\begin{bmatrix}s \\ t\end{bmatrix} \\  & =\begin{bmatrix}s\cdot s+t\cdot t \\ (-t)\cdot s+s\cdot t\end{bmatrix} \\  & =\begin{bmatrix}s^{2}+t^{2} \\ -st+st\end{bmatrix} \\  & =\begin{bmatrix}s^{2}+t^{2} \\ 0\end{bmatrix}\end{aligned}
$$


## Generated q-127277 observed 0

Find $Qg$ if 
$Q=\begin{bmatrix}m & 2m \\ -m & 2n\end{bmatrix}$
and
$g=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$


selection: $\begin{bmatrix}4m \\ 2m+6n\end{bmatrix}$; $\begin{bmatrix}4m \\ m+2n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+2n\end{bmatrix}$; $\begin{bmatrix}4m \\ 2m+2n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+6n\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qg & =\begin{bmatrix}m & 2m \\ -m & 2n\end{bmatrix}\begin{bmatrix}-2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}m\cdot (-2)+2m\cdot 3 \\ (-m)\cdot (-2)+2n\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}-2m+6m \\ 2m+6n\end{bmatrix} \\  & =\begin{bmatrix}4m \\ 2m+6n\end{bmatrix}\end{aligned}
$$


## Generated q-127277 observed 1

Find $Qg$ if 
$Q=\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}$
and
$g=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$


selection: $\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+3n\end{bmatrix}$; $\begin{bmatrix}4m \\ 2m+n\end{bmatrix}$; $\begin{bmatrix}4m \\ m+n\end{bmatrix}$; $\begin{bmatrix}2m \\ 2m+n\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qg & =\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}\begin{bmatrix}-2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}m\cdot (-2)+2m\cdot 3 \\ (-m)\cdot (-2)+n\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}-2m+6m \\ 2m+3n\end{bmatrix} \\  & =\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}\end{aligned}
$$


## Generated q-127277 authored-operations 0

Find $Qg$ if 
$Q=\begin{bmatrix}m & 2m \\ -m & 2n\end{bmatrix}$
and
$g=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$


selection: $\begin{bmatrix}4m \\ 2m+6n\end{bmatrix}$; $\begin{bmatrix}6m \\ 6n\end{bmatrix}$; $\begin{bmatrix}-2m \\ 2m\end{bmatrix}$; $\begin{bmatrix}3m \\ -m+2n\end{bmatrix}$; $\begin{bmatrix}-4m \\ -2m-6n\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qg & =\begin{bmatrix}m & 2m \\ -m & 2n\end{bmatrix}\begin{bmatrix}-2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}m\cdot (-2)+2m\cdot 3 \\ (-m)\cdot (-2)+2n\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}-2m+6m \\ 2m+6n\end{bmatrix} \\  & =\begin{bmatrix}4m \\ 2m+6n\end{bmatrix}\end{aligned}
$$


## Generated q-127277 authored-operations 1

Find $Qg$ if 
$Q=\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}$
and
$g=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$


selection: $\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}$; $\begin{bmatrix}-4m \\ -2m-3n\end{bmatrix}$; $\begin{bmatrix}3m \\ -m+n\end{bmatrix}$; $\begin{bmatrix}6m \\ 3n\end{bmatrix}$; $\begin{bmatrix}-2m \\ 2m\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qg & =\begin{bmatrix}m & 2m \\ -m & n\end{bmatrix}\begin{bmatrix}-2 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}m\cdot (-2)+2m\cdot 3 \\ (-m)\cdot (-2)+n\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}-2m+6m \\ 2m+3n\end{bmatrix} \\  & =\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}\end{aligned}
$$


## Generated q-275597 observed 0

If 
$Q=\begin{bmatrix}2a & b & 2a \\ 2a & -b & 2a \\ 0 & 0 & 2a\end{bmatrix}$
and
$r=\begin{bmatrix}2a \\ 0 \\ -2a\end{bmatrix},$
find $Qr.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Qr=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $-4a^{2}$


field-2: $0$


field-1: $0$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qr & =\begin{bmatrix}2a & b & 2a \\ 2a & -b & 2a \\ 0 & 0 & 2a\end{bmatrix}\begin{bmatrix}2a \\ 0 \\ -2a\end{bmatrix} \\  & =\begin{bmatrix}2a\cdot 2a+b\cdot 0+2a\cdot (-2a) \\ 2a\cdot 2a+(-b)\cdot 0+2a\cdot (-2a) \\ 0\cdot 2a+0\cdot 0+2a\cdot (-2a)\end{bmatrix} \\  & =\begin{bmatrix}4a^{2}+0-4a^{2} \\ 4a^{2}+0-4a^{2} \\ 0+0-4a^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -4a^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-275597 observed 1

If 
$Q=\begin{bmatrix}2a & 2b & 2a \\ 2a & -2b & 2a \\ 0 & 0 & 2a\end{bmatrix}$
and
$r=\begin{bmatrix}2a \\ 0 \\ -2a\end{bmatrix},$
find $Qr.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Qr=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $-4a^{2}$


field-2: $0$


field-1: $0$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Qr & =\begin{bmatrix}2a & 2b & 2a \\ 2a & -2b & 2a \\ 0 & 0 & 2a\end{bmatrix}\begin{bmatrix}2a \\ 0 \\ -2a\end{bmatrix} \\  & =\begin{bmatrix}2a\cdot 2a+2b\cdot 0+2a\cdot (-2a) \\ 2a\cdot 2a+(-2b)\cdot 0+2a\cdot (-2a) \\ 0\cdot 2a+0\cdot 0+2a\cdot (-2a)\end{bmatrix} \\  & =\begin{bmatrix}4a^{2}+0-4a^{2} \\ 4a^{2}+0-4a^{2} \\ 0+0-4a^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -4a^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-318589 observed 0

If 
$A=\begin{bmatrix}b & 2a & -b \\ -b & 2a & b \\ -b & 0 & -b\end{bmatrix}$
and
$x=\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix},$
find $Ax.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Ax=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $0$


field-1: $-2b^{2}$


field-2: $2b^{2}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}b & 2a & -b \\ -b & 2a & b \\ -b & 0 & -b\end{bmatrix}\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix} \\  & =\begin{bmatrix}b\cdot (-b)+2a\cdot 0+(-b)\cdot b \\ (-b)\cdot (-b)+2a\cdot 0+b\cdot b \\ (-b)\cdot (-b)+0\cdot 0+(-b)\cdot b\end{bmatrix} \\  & =\begin{bmatrix}-b^{2}+0-b^{2} \\ b^{2}+0+b^{2} \\ b^{2}+0-b^{2}\end{bmatrix} \\  & =\begin{bmatrix}-2b^{2} \\ 2b^{2} \\ 0\end{bmatrix}.\end{aligned}
$$


## Generated q-318589 observed 1

If 
$A=\begin{bmatrix}2b & 2a & -2b \\ -2b & 2a & 2b \\ -2b & 0 & -2b\end{bmatrix}$
and
$x=\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix},$
find $Ax.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Ax=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $0$


field-1: $-4b^{2}$


field-2: $4b^{2}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Ax & =\begin{bmatrix}2b & 2a & -2b \\ -2b & 2a & 2b \\ -2b & 0 & -2b\end{bmatrix}\begin{bmatrix}-b \\ 0 \\ b\end{bmatrix} \\  & =\begin{bmatrix}2b\cdot (-b)+2a\cdot 0+(-2b)\cdot b \\ (-2b)\cdot (-b)+2a\cdot 0+2b\cdot b \\ (-2b)\cdot (-b)+0\cdot 0+(-2b)\cdot b\end{bmatrix} \\  & =\begin{bmatrix}-2b^{2}+0-2b^{2} \\ 2b^{2}+0+2b^{2} \\ 2b^{2}+0-2b^{2}\end{bmatrix} \\  & =\begin{bmatrix}-4b^{2} \\ 4b^{2} \\ 0\end{bmatrix}.\end{aligned}
$$


## Generated q-318591 observed 0

If 
$P=\begin{bmatrix}2m & n & -2m \\ 2m & -n & -2m \\ 0 & 2 & 0\end{bmatrix}$
and
$u=\begin{bmatrix}1 \\ p \\ 1\end{bmatrix},$
find $Pu.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Pu=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $2p$


field-1: $np$


field-2: $-np$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pu & =\begin{bmatrix}2m & n & -2m \\ 2m & -n & -2m \\ 0 & 2 & 0\end{bmatrix}\begin{bmatrix}1 \\ p \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2m\cdot 1+n\cdot p+(-2m)\cdot 1 \\ 2m\cdot 1+(-n)\cdot p+(-2m)\cdot 1 \\ 0\cdot 1+2\cdot p+0\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}2m+np-2m \\ 2m-np-2m \\ 0+2p+0\end{bmatrix} \\  & =\begin{bmatrix}np \\ -np \\ 2p\end{bmatrix}.\end{aligned}
$$


## Generated q-318591 observed 1

If 
$P=\begin{bmatrix}2m & 2n & -2m \\ 2m & -2n & -2m \\ 0 & 2 & 0\end{bmatrix}$
and
$u=\begin{bmatrix}1 \\ p \\ 1\end{bmatrix},$
find $Pu.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Pu=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |


field-3: $2p$


field-1: $2np$


field-2: $-2np$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pu & =\begin{bmatrix}2m & 2n & -2m \\ 2m & -2n & -2m \\ 0 & 2 & 0\end{bmatrix}\begin{bmatrix}1 \\ p \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2m\cdot 1+2n\cdot p+(-2m)\cdot 1 \\ 2m\cdot 1+(-2n)\cdot p+(-2m)\cdot 1 \\ 0\cdot 1+2\cdot p+0\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}2m+2np-2m \\ 2m-2np-2m \\ 0+2p+0\end{bmatrix} \\  & =\begin{bmatrix}2np \\ -2np \\ 2p\end{bmatrix}.\end{aligned}
$$


## Generated q-318595 observed 0

Find $By$  if 
$B=\begin{bmatrix}4p & -5q \\ -5p & q\end{bmatrix}$
and
$y=\begin{bmatrix}p \\ q\end{bmatrix}.$

| $By=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |


field-2: $-5p^{2}+q^{2}$


field-1: $4p^{2}-5q^{2}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}4p & -5q \\ -5p & q\end{bmatrix}\begin{bmatrix}p \\ q\end{bmatrix} \\  & =\begin{bmatrix}4p\cdot p+(-5q)\cdot q \\ (-5p)\cdot p+q\cdot q\end{bmatrix} \\  & =\begin{bmatrix}4p^{2}-5q^{2} \\ -5p^{2}+q^{2}\end{bmatrix}.\end{aligned}
$$


## Generated q-318595 observed 1

Find $By$  if 
$B=\begin{bmatrix}4p & -3q \\ -2p & 2q\end{bmatrix}$
and
$y=\begin{bmatrix}p \\ q\end{bmatrix}.$

| $By=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |


field-2: $-2p^{2}+2q^{2}$


field-1: $4p^{2}-3q^{2}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}4p & -3q \\ -2p & 2q\end{bmatrix}\begin{bmatrix}p \\ q\end{bmatrix} \\  & =\begin{bmatrix}4p\cdot p+(-3q)\cdot q \\ (-2p)\cdot p+2q\cdot q\end{bmatrix} \\  & =\begin{bmatrix}4p^{2}-3q^{2} \\ -2p^{2}+2q^{2}\end{bmatrix}.\end{aligned}
$$


## Generated q-70226 observed 0

Find $Tu$ if 
$T=\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}$
and
$u=\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix}.$


selection: $\begin{bmatrix}x^{2} \\ 0 \\ -x^{2}\end{bmatrix}$; $\begin{bmatrix}x^{2}y \\ 0 \\ -x^{2}y\end{bmatrix}$; $\begin{bmatrix}0 \\ 0 \\ -2x^{2}\end{bmatrix}$; $\begin{bmatrix}x^{2} \\ -x^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}x^{3}y \\ 0 \\ -x^{3}y\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Tu & =\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix} \\  & =\begin{bmatrix}x\cdot x+y\cdot 0+x\cdot (-x) \\ x\cdot x+(-y)\cdot 0+x\cdot (-x) \\ (-x)\cdot x+(-y)\cdot 0+x\cdot (-x)\end{bmatrix} \\  & =\begin{bmatrix}x^{2}+0-x^{2} \\ x^{2}+0-x^{2} \\ -x^{2}+0-x^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -2x^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-70226 observed 1

Find $Tu$ if 
$T=\begin{bmatrix}2x & 2y & 2x \\ 2x & -2y & 2x \\ -2x & -2y & 2x\end{bmatrix}$
and
$u=\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix}.$


selection: $\begin{bmatrix}0 \\ 0 \\ -4x^{2}\end{bmatrix}$; $\begin{bmatrix}2x^{2} \\ -2x^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}2x^{2}y \\ 0 \\ -2x^{2}y\end{bmatrix}$; $\begin{bmatrix}2x^{2} \\ 0 \\ -2x^{2}\end{bmatrix}$; $\begin{bmatrix}2x^{3}y \\ 0 \\ -2x^{3}y\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Tu & =\begin{bmatrix}2x & 2y & 2x \\ 2x & -2y & 2x \\ -2x & -2y & 2x\end{bmatrix}\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix} \\  & =\begin{bmatrix}2x\cdot x+2y\cdot 0+2x\cdot (-x) \\ 2x\cdot x+(-2y)\cdot 0+2x\cdot (-x) \\ (-2x)\cdot x+(-2y)\cdot 0+2x\cdot (-x)\end{bmatrix} \\  & =\begin{bmatrix}2x^{2}+0-2x^{2} \\ 2x^{2}+0-2x^{2} \\ -2x^{2}+0-2x^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -4x^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-70226 authored-operations 0

Find $Tu$ if 
$T=\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}$
and
$u=\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix}.$


selection: $\begin{bmatrix}2x^{2} \\ 2x^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}-x^{2} \\ -x^{2} \\ -x^{2}\end{bmatrix}$; $\begin{bmatrix}0 \\ 0 \\ -2x^{2}\end{bmatrix}$; $\begin{bmatrix}x^{2} \\ x^{2} \\ -x^{2}\end{bmatrix}$; $\begin{bmatrix}0 \\ 0 \\ 2x^{2}\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Tu & =\begin{bmatrix}x & y & x \\ x & -y & x \\ -x & -y & x\end{bmatrix}\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix} \\  & =\begin{bmatrix}x\cdot x+y\cdot 0+x\cdot (-x) \\ x\cdot x+(-y)\cdot 0+x\cdot (-x) \\ (-x)\cdot x+(-y)\cdot 0+x\cdot (-x)\end{bmatrix} \\  & =\begin{bmatrix}x^{2}+0-x^{2} \\ x^{2}+0-x^{2} \\ -x^{2}+0-x^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -2x^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-70226 authored-operations 1

Find $Tu$ if 
$T=\begin{bmatrix}2x & 2y & 2x \\ 2x & -2y & 2x \\ -2x & -2y & 2x\end{bmatrix}$
and
$u=\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix}.$


selection: $\begin{bmatrix}0 \\ 0 \\ -4x^{2}\end{bmatrix}$; $\begin{bmatrix}2x^{2} \\ 2x^{2} \\ -2x^{2}\end{bmatrix}$; $\begin{bmatrix}-2x^{2} \\ -2x^{2} \\ -2x^{2}\end{bmatrix}$; $\begin{bmatrix}4x^{2} \\ 4x^{2} \\ 0\end{bmatrix}$; $\begin{bmatrix}0 \\ 0 \\ 4x^{2}\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Tu & =\begin{bmatrix}2x & 2y & 2x \\ 2x & -2y & 2x \\ -2x & -2y & 2x\end{bmatrix}\begin{bmatrix}x \\ 0 \\ -x\end{bmatrix} \\  & =\begin{bmatrix}2x\cdot x+2y\cdot 0+2x\cdot (-x) \\ 2x\cdot x+(-2y)\cdot 0+2x\cdot (-x) \\ (-2x)\cdot x+(-2y)\cdot 0+2x\cdot (-x)\end{bmatrix} \\  & =\begin{bmatrix}2x^{2}+0-2x^{2} \\ 2x^{2}+0-2x^{2} \\ -2x^{2}+0-2x^{2}\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0 \\ -4x^{2}\end{bmatrix}\end{aligned}
$$


## Generated q-13556 observed 0

Find $By$  if 
$B=\begin{bmatrix}b & b \\ c & c\end{bmatrix}$
and
$y=\begin{bmatrix}3 \\ 4\end{bmatrix}.$


selection: $\begin{bmatrix}-7b \\ -7c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7c\end{bmatrix}$; $\begin{bmatrix}7b \\ 7b\end{bmatrix}$; $\begin{bmatrix}7c \\ 7b\end{bmatrix}$; $\begin{bmatrix}7b \\ 7c\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product: 

$$
\begin{aligned}By & =\begin{bmatrix}b & b \\ c & c\end{bmatrix}\begin{bmatrix}3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}b\cdot 3+b\cdot 4 \\ c\cdot 3+c\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}3b+4b \\ 3c+4c\end{bmatrix} \\  & =\begin{bmatrix}7b \\ 7c\end{bmatrix}\end{aligned}
$$


## Generated q-13556 observed 1

Find $By$  if 
$B=\begin{bmatrix}b & b \\ c & c\end{bmatrix}$
and
$y=\begin{bmatrix}3 \\ 4\end{bmatrix}.$


selection: $\begin{bmatrix}-7b \\ -7c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7b\end{bmatrix}$; $\begin{bmatrix}7b \\ 7c\end{bmatrix}$; $\begin{bmatrix}7b \\ 7b\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product: 

$$
\begin{aligned}By & =\begin{bmatrix}b & b \\ c & c\end{bmatrix}\begin{bmatrix}3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}b\cdot 3+b\cdot 4 \\ c\cdot 3+c\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}3b+4b \\ 3c+4c\end{bmatrix} \\  & =\begin{bmatrix}7b \\ 7c\end{bmatrix}\end{aligned}
$$


## Generated q-13556 authored-operations 0

Find $By$  if 
$B=\begin{bmatrix}b & b \\ c & c\end{bmatrix}$
and
$y=\begin{bmatrix}3 \\ 4\end{bmatrix}.$


selection: $\begin{bmatrix}7b \\ 7c\end{bmatrix}$; $\begin{bmatrix}-7b \\ -7c\end{bmatrix}$; $\begin{bmatrix}3b \\ 3c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7b\end{bmatrix}$; $\begin{bmatrix}4b \\ 4c\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product: 

$$
\begin{aligned}By & =\begin{bmatrix}b & b \\ c & c\end{bmatrix}\begin{bmatrix}3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}b\cdot 3+b\cdot 4 \\ c\cdot 3+c\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}3b+4b \\ 3c+4c\end{bmatrix} \\  & =\begin{bmatrix}7b \\ 7c\end{bmatrix}\end{aligned}
$$


## Generated q-13556 authored-operations 1

Find $By$  if 
$B=\begin{bmatrix}b & b \\ c & c\end{bmatrix}$
and
$y=\begin{bmatrix}3 \\ 4\end{bmatrix}.$


selection: $\begin{bmatrix}7b \\ 7c\end{bmatrix}$; $\begin{bmatrix}-7b \\ -7c\end{bmatrix}$; $\begin{bmatrix}7c \\ 7b\end{bmatrix}$; $\begin{bmatrix}4b \\ 4c\end{bmatrix}$; $\begin{bmatrix}3b \\ 3c\end{bmatrix}$

We multiply each row in the matrix by the column vector using the dot product: 

$$
\begin{aligned}By & =\begin{bmatrix}b & b \\ c & c\end{bmatrix}\begin{bmatrix}3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}b\cdot 3+b\cdot 4 \\ c\cdot 3+c\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}3b+4b \\ 3c+4c\end{bmatrix} \\  & =\begin{bmatrix}7b \\ 7c\end{bmatrix}\end{aligned}
$$
