# Rectangular region signs review

Originals retain complete source banks. Generated variants are labeled; authored defaults use truth flips. q-96475 has an inferred marker and authored solution, not source solution fidelity.

## original q-96475

Template `numbered_bilinear`, profile `q-96475`.

Parameters: `{"h": 1, "k": -2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [1, -1, 1]]}`.



Consider the differential equation $\frac{dy}{dx} = (x - 1)(y + 2)$ and its slope field. Which of the following statements are true?

1. At every point $(x, y)$ where $x > 1$ and $y > - 2$, the slope of the slope field is positive
2. At every point $(x, y)$ where $x < 1$ and $y > - 2$, the slope of the slope field is positive
3. At every point $(x, y)$ where $x > 1$ and $y < - 2$, the slope of the slope field is positive



- I only **correct**
- I, II, and III
- I and II only
- III only
- I and III only



First, we define $f(x,y)=(x-1)(y+2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/846e9001b0aa3180074b-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/846e9001b0aa3180074b-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x>1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## generated observed-bank variant q-96475 1

Template `numbered_bilinear`, profile `q-96475`.

Parameters: `{"h": -1, "k": -2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [1, -1, 1]]}`.



Consider the differential equation $\frac{dy}{dx} = (x + 1)(y + 2)$ and its slope field. Which of the following statements are true?

1. At every point $(x, y)$ where $x > - 1$ and $y > - 2$, the slope of the slope field is positive
2. At every point $(x, y)$ where $x < - 1$ and $y > - 2$, the slope of the slope field is positive
3. At every point $(x, y)$ where $x > - 1$ and $y < - 2$, the slope of the slope field is positive



- I and II only
- I, II, and III
- I and III only
- I only **correct**
- III only



First, we define $f(x,y)=(x+1)(y+2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/40fea4783b4352dd22bb-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/40fea4783b4352dd22bb-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>-1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<-1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x>-1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## generated observed-bank variant q-96475 2

Template `numbered_bilinear`, profile `q-96475`.

Parameters: `{"h": 1, "k": 2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [1, -1, 1]]}`.



Consider the differential equation $\frac{dy}{dx} = (x - 1)(y - 2)$ and its slope field. Which of the following statements are true?

1. At every point $(x, y)$ where $x > 1$ and $y > 2$, the slope of the slope field is positive
2. At every point $(x, y)$ where $x < 1$ and $y > 2$, the slope of the slope field is positive
3. At every point $(x, y)$ where $x > 1$ and $y < 2$, the slope of the slope field is positive



- I, II, and III
- I only **correct**
- I and II only
- III only
- I and III only



First, we define $f(x,y)=(x-1)(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/9bf9e9090028d8635d5f-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/9bf9e9090028d8635d5f-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x>1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## original q-97538

Template `x_squared`, profile `q-97538`.

Parameters: `{"h": -1, "k": 2, "ox": 1, "oy": 1, "px": 2, "py": 1, "regions": [[-1, 1, 1], [-1, -1, -1], [1, -1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)^{2}(y-2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y>2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-1$ and $y<2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y<2,$ the slope of the slope field is negative



- I and III only
- I, II, and III **correct**
- I only
- III only
- II and III only



First, we define $f(x,y)=(x+1)^{2}(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](images/1f/1f4b1b2ca736fb83eff0a4b85a3f479bf99b3b337492d0a77abe739038ed141f.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/fd/fdafadd1631a75c2998aaed5c6bad62a3ea1dcc0ac57d245a00d167e74aa3bb4.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## generated observed-bank variant q-97538 1

Template `x_squared`, profile `q-97538`.

Parameters: `{"h": 1, "k": 2, "ox": 1, "oy": 1, "px": 2, "py": 1, "regions": [[-1, 1, 1], [-1, -1, -1], [1, -1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-1)^{2}(y-2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y>2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<1$ and $y<2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y<2,$ the slope of the slope field is negative



- I only
- I, II, and III **correct**
- II and III only
- I and III only
- III only



First, we define $f(x,y)=(x-1)^{2}(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/5d07000192c7d72a3644-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/5d07000192c7d72a3644-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## generated observed-bank variant q-97538 2

Template `x_squared`, profile `q-97538`.

Parameters: `{"h": -1, "k": -2, "ox": 1, "oy": -1, "px": 2, "py": 1, "regions": [[-1, 1, -1], [-1, -1, 1], [1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)^{2}(-2-y)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y>-2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-1$ and $y<-2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>-1$ and $y<-2,$ the slope of the slope field is positive



- I, II, and III **correct**
- I and III only
- I only
- III only
- II and III only



First, we define $f(x,y)=(x+1)^{2}(-2-y).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/9d604500af40b22e7828-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/9d604500af40b22e7828-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is true. If $x<-1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## original q-119797

Template `bilinear`, profile `q-119797`.

Parameters: `{"h": 2, "k": -1, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[1, -1, 1], [-1, -1, -1], [-1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(2-x)(y+1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>2$ and $y<-1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<2$ and $y>-1,$ the slope of the slope field is positive



- II only
- I, II, and III **correct**
- II and III only
- I only
- I and II only



First, we define $f(x,y)=(2-x)(y+1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](images/ca/caa61190f1a5565c58838556529715c08f9f00402c6f4b3ccb99a914e748f198.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/01/01e91ecf01cfc64ed87e29081a6b9f8a3fc5afade1b25be08039b8778d981cf7.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## generated observed-bank variant q-119797 1

Template `bilinear`, profile `q-119797`.

Parameters: `{"h": -2, "k": -1, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[1, -1, 1], [-1, -1, -1], [-1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-2-x)(y+1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>-2$ and $y<-1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-2$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-2$ and $y>-1,$ the slope of the slope field is positive



- II and III only
- I, II, and III **correct**
- I and II only
- II only
- I only



First, we define $f(x,y)=(-2-x)(y+1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-2$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/42a0f6d5c7adf441d076-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/42a0f6d5c7adf441d076-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>-2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<-2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## generated observed-bank variant q-119797 2

Template `bilinear`, profile `q-119797`.

Parameters: `{"h": 2, "k": 1, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[1, -1, 1], [-1, -1, -1], [-1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(2-x)(y-1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>2$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y<1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<2$ and $y>1,$ the slope of the slope field is positive



- I, II, and III **correct**
- II only
- II and III only
- I only
- I and II only



First, we define $f(x,y)=(2-x)(y-1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/ea3a90fb7791b67b2ed0-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/ea3a90fb7791b67b2ed0-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>2$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<2$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<2$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## original q-119800

Template `bilinear`, profile `q-119800`.

Parameters: `{"h": 1, "k": 2, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, 1, -1], [1, -1, -1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(1-x)(y-2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y>2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y<2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<1$ and $y<2,$ the slope of the slope field is positive



- II and III only
- III only
- II only
- I and II only
- None of those listed **correct**



First, we define $f(x,y)=(1-x)(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](images/47/47784a3201e93648e495827b12078073cc9f1a03cd3c11904a875bad10a3bde2.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/73/73631c178777b4489e35fa87d08474ccf2b8b484b9bf5fe7272b1ce25d45f1b0.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x>1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x<1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "None of those listed."



## generated observed-bank variant q-119800 1

Template `bilinear`, profile `q-119800`.

Parameters: `{"h": -1, "k": 2, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, 1, -1], [1, -1, -1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-1-x)(y-2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y>2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y<2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-1$ and $y<2,$ the slope of the slope field is positive



- II only
- III only
- None of those listed **correct**
- II and III only
- I and II only



First, we define $f(x,y)=(-1-x)(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/6d6ca0f5b89f5396550f-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/6d6ca0f5b89f5396550f-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-1$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x>-1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x<-1$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "None of those listed."



## generated observed-bank variant q-119800 2

Template `bilinear`, profile `q-119800`.

Parameters: `{"h": 1, "k": -2, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, 1, -1], [1, -1, -1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(1-x)(y+2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y>-2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y<-2,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<1$ and $y<-2,$ the slope of the slope field is positive



- III only
- II and III only
- II only
- I and II only
- None of those listed **correct**



First, we define $f(x,y)=(1-x)(y+2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/eee8924ef064332a4010-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/eee8924ef064332a4010-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<1$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x>1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x<1$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "None of those listed."



## original q-119816

Template `x_squared`, profile `q-119816`.

Parameters: `{"h": 2, "k": -1, "ox": 1, "oy": 1, "px": 2, "py": 1, "regions": [[-1, 1, -1], [-1, -1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-2)^{2}(y+1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<2$ and $y>-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<2$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>2$ and $y>-1,$ the slope of the slope field is positive



- I and II only
- I and III only
- I only
- II and III only **correct**
- II only



First, we define $f(x,y)=(x-2)^{2}(y+1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](images/ca/caa61190f1a5565c58838556529715c08f9f00402c6f4b3ccb99a914e748f198.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/d8/d836463631120853e05b3b5fb9e534822cf5611747a3eb17e22333901bfb8fd3.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "II and III only."



## generated observed-bank variant q-119816 1

Template `x_squared`, profile `q-119816`.

Parameters: `{"h": -2, "k": -1, "ox": 1, "oy": 1, "px": 2, "py": 1, "regions": [[-1, 1, -1], [-1, -1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+2)^{2}(y+1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-2$ and $y>-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-2$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-2$ and $y>-1,$ the slope of the slope field is positive



- I only
- I and III only
- II only
- I and II only
- II and III only **correct**



First, we define $f(x,y)=(x+2)^{2}(y+1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-2$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/5af778ac993d04cc777b-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/5af778ac993d04cc777b-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-2$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-2$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "II and III only."



## generated observed-bank variant q-119816 2

Template `x_squared`, profile `q-119816`.

Parameters: `{"h": 2, "k": 1, "ox": 1, "oy": -1, "px": 2, "py": 1, "regions": [[-1, 1, 1], [-1, -1, 1], [1, 1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-2)^{2}(1-y)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<2$ and $y>1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>2$ and $y>1,$ the slope of the slope field is negative



- I and III only
- I and II only
- I only
- II and III only **correct**
- II only



First, we define $f(x,y)=(x-2)^{2}(1-y).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/377e3623b1f008244bb2-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/377e3623b1f008244bb2-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<2$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is true. If $x<2$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>2$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "II and III only."



## original q-97495

Template `bilinear`, profile `q-97495`.

Parameters: `{"h": -2, "k": -2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+2)(y+2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>-2$ and $y>-2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-2$ and $y>-2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-2$ and $y<-2,$ the slope of the slope field is positive



- I only
- II and III only
- I and II only
- I and III only **correct**
- II only



First, we define $f(x,y)=(x+2)(y+2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-2$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](images/7d/7d225d82eee3043380eda76506b28e81aee06d42a232348b91b0d5ceb04f3318.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/bd/bd9eedd3b8d82415e8f3126236f2e3a3b4e326a7072057bbd21406da92a08139.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>-2$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<-2$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<-2$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## generated observed-bank variant q-97495 1

Template `bilinear`, profile `q-97495`.

Parameters: `{"h": 2, "k": -2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-2)(y+2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>2$ and $y>-2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y>-2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y<-2,$ the slope of the slope field is positive



- I and II only
- II and III only
- II only
- I only
- I and III only **correct**



First, we define $f(x,y)=(x-2)(y+2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=-2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/0b9ca0b7224244f45c03-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/0b9ca0b7224244f45c03-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>2$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<2$ and $y>-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<2$ and $y<-2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## generated observed-bank variant q-97495 2

Template `bilinear`, profile `q-97495`.

Parameters: `{"h": -2, "k": 2, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, 1, 1], [-1, 1, 1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+2)(y-2)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>-2$ and $y>2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-2$ and $y>2,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-2$ and $y<2,$ the slope of the slope field is positive



- II and III only
- I only
- I and II only
- I and III only **correct**
- II only



First, we define $f(x,y)=(x+2)(y-2).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-2$ or $y=2.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/75d495a8a49de4147945-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/75d495a8a49de4147945-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>-2$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<-2$ and $y>2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<-2$ and $y<2,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## original q-97534

Template `y_squared`, profile `q-97534`.

Parameters: `{"h": 1, "k": 1, "ox": 1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, -1, 1], [1, -1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-1)(y-1)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>1$ and $y<1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y>1,$ the slope of the slope field is positive



- I only
- None of those listed
- III only **correct**
- I and II only
- II only



First, we define $f(x,y)=(x-1)(y-1)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](images/07/075264fa042adc64e160a83f03a2b125dd5a9b0927fc3ed318778c0004689ec4.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](images/57/5716d59a745fc148b504a4db523286d7c7209fe793fcf369a90d220125f7e9fb.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x>1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## generated observed-bank variant q-97534 1

Template `y_squared`, profile `q-97534`.

Parameters: `{"h": -1, "k": 1, "ox": 1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, -1, 1], [1, -1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)(y-1)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>-1$ and $y<1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y>1,$ the slope of the slope field is positive



- III only **correct**
- None of those listed
- II only
- I only
- I and II only



First, we define $f(x,y)=(x+1)(y-1)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/ebbcbf9faabd89a97f5d-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/ebbcbf9faabd89a97f5d-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x>-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.



## generated observed-bank variant q-97534 2

Template `y_squared`, profile `q-97534`.

Parameters: `{"h": 1, "k": -1, "ox": -1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, -1, -1], [1, -1, 1], [1, 1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(1-x)(y+1)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y<-1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>1$ and $y>-1,$ the slope of the slope field is negative



- None of those listed
- I only
- III only **correct**
- I and II only
- II only



First, we define $f(x,y)=(1-x)(y+1)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/29b79202d6ec8cea2e22-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/29b79202d6ec8cea2e22-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<1$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x>1$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>1$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.



## authored easy seed 13

Template `easy_bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": 1, "k": -1, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, 1, -1], [1, -1, -1], [-1, -1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-1)(y+1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<1$ and $y>-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>1$ and $y<-1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<1$ and $y<-1,$ the slope of the slope field is negative



- III only
- I, II, and III
- I only
- II only
- I and II only **correct**



First, we define $f(x,y)=(x-1)(y+1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=1$ or $y=-1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/041df1aa0ac13ec4ba5a-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/041df1aa0ac13ec4ba5a-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<1$ and $y>-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is true. If $x>1$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x<1$ and $y<-1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I and II only."



## authored easy seed 14

Template `easy_bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -1, "k": 1, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[1, -1, 1], [-1, 1, 1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)(y-1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>-1$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-1$ and $y>1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-1$ and $y<1,$ the slope of the slope field is positive



- II and III only
- I and III only
- III only **correct**
- I and II only
- None of those listed



First, we define $f(x,y)=(x+1)(y-1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/cf1eec810fd3fce7b4dd-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/cf1eec810fd3fce7b4dd-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x>-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x<-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x<-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "III only."



## authored moderate seed 13

Template `bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -1, "k": 3, "ox": -1, "oy": -1, "px": 1, "py": 1, "regions": [[-1, 1, -1], [-1, -1, -1], [1, -1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-1-x)(3-y)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-1$ and $y<3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y<3,$ the slope of the slope field is negative



- II only
- I only
- III only
- I and III only **correct**
- I, II, and III



First, we define $f(x,y)=(-1-x)(3-y).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/13fa9249ceaeb6ebf8ca-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/13fa9249ceaeb6ebf8ca-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-1$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x<-1$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "I and III only."



## authored moderate seed 14

Template `bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": 2, "k": 3, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[1, -1, 1], [-1, 1, 1], [-1, -1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(2-x)(y-3)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>2$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y>3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<2$ and $y<3,$ the slope of the slope field is positive



- I only
- II only
- I and II only **correct**
- III only
- I, II, and III



First, we define $f(x,y)=(2-x)(y-3).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/cfd6d75491aa2951db15-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/cfd6d75491aa2951db15-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>2$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<2$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x<2$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "I and II only."



## authored hard seed 13

Template `y_squared`, profile `authored_truth_flips`.

Parameters: `{"h": -1, "k": 3, "ox": -1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, 1, -1], [1, -1, -1], [-1, -1, -1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-1-x)(y-3)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y<3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<-1$ and $y<3,$ the slope of the slope field is negative



- I and III only
- II and III only
- None of those listed
- I and II only
- II only **correct**



First, we define $f(x,y)=(-1-x)(y-3)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/1d69755ad5edcd2a6472-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/1d69755ad5edcd2a6472-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-1$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x>-1$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x<-1$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "II only."



## authored hard seed 14

Template `x_squared`, profile `authored_truth_flips`.

Parameters: `{"h": 2, "k": 3, "ox": 1, "oy": -1, "px": 2, "py": 1, "regions": [[1, -1, 1], [1, 1, -1], [-1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x-2)^{2}(3-y)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x>2$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x>2$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x<2$ and $y>3,$ the slope of the slope field is positive



- I and II only **correct**
- II only
- III only
- I, II, and III
- I only



First, we define $f(x,y)=(x-2)^{2}(3-y).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=2$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/1346bec4abd729362055-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/1346bec4abd729362055-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x>2$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x>2$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x<2$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "I and II only."



## authored boundary easy_bilinear -1

Template `easy_bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -1, "k": 1, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)(y-1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-1$ and $y>1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y>1,$ the slope of the slope field is positive



- I and II only
- I and III only
- I, II, and III **correct**
- None of those listed
- II and III only



First, we define $f(x,y)=(x+1)(y-1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/cf1eec810fd3fce7b4dd-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/cf1eec810fd3fce7b4dd-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## authored boundary easy_bilinear 1

Template `easy_bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -1, "k": 1, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+1)(y-1)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-1$ and $y<1,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-1$ and $y>1,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-1$ and $y>1,$ the slope of the slope field is positive



- I and II only
- I and III only
- I, II, and III **correct**
- None of those listed
- II and III only



First, we define $f(x,y)=(x+1)(y-1).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-1$ or $y=1.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/cf1eec810fd3fce7b4dd-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/cf1eec810fd3fce7b4dd-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-1$ and $y<1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-1$ and $y>1,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## authored boundary bilinear -1

Template `bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": -1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-3-x)(y-3)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- III only
- II only
- None of those listed **correct**
- I, II, and III
- I only



First, we define $f(x,y)=(-3-x)(y-3).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/9098fd9dfc1562359664-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/9098fd9dfc1562359664-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "None of those listed."



## authored boundary bilinear 1

Template `bilinear`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": 1, "oy": 1, "px": 1, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+3)(y-3)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- I and II only
- I and III only
- I, II, and III **correct**
- None of those listed
- II and III only



First, we define $f(x,y)=(x+3)(y-3).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/1bf88afdee765eccc7d5-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/1bf88afdee765eccc7d5-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "I, II, and III."



## authored boundary x_squared -1

Template `x_squared`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": 1, "oy": -1, "px": 2, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+3)^{2}(3-y)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- I, II, and III
- I only
- I and II only **correct**
- III only
- II only



First, we define $f(x,y)=(x+3)^{2}(3-y).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/6f96f5812c0a034c9c22-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/6f96f5812c0a034c9c22-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is true. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is false. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "I and II only."



## authored boundary x_squared 1

Template `x_squared`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": 1, "oy": 1, "px": 2, "py": 1, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+3)^{2}(y-3)$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- None of those listed
- II and III only
- III only **correct**
- I and II only
- I and III only



First, we define $f(x,y)=(x+3)^{2}(y-3).$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/f6ec345c727c30bbab32-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/f6ec345c727c30bbab32-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is false. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is true. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "III only."



## authored boundary y_squared -1

Template `y_squared`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": -1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(-3-x)(y-3)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- I and III only
- I and II only
- I only **correct**
- II and III only
- None of those listed



First, we define $f(x,y)=(-3-x)(y-3)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/67c3a33a85d6391c36d2-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/67c3a33a85d6391c36d2-signs.png)

With that in mind, let's check each statement:

- Statement I is true. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement II is false. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

- Statement III is false. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

Therefore, the correct answer is "I only."



## authored boundary y_squared 1

Template `y_squared`, profile `authored_truth_flips`.

Parameters: `{"h": -3, "k": 3, "ox": 1, "oy": 1, "px": 1, "py": 2, "regions": [[-1, -1, 1], [-1, 1, -1], [1, 1, 1]]}`.



Consider the differential equation $\frac{\text{d}y}{\text{d}x}=(x+3)(y-3)^{2}$ and its slope field. Which of the following statements are true?

- At every point $(x,y)$ where $x<-3$ and $y<3,$ the slope of the slope field is positive
- At every point $(x,y)$ where $x<-3$ and $y>3,$ the slope of the slope field is negative
- At every point $(x,y)$ where $x>-3$ and $y>3,$ the slope of the slope field is positive



- II only
- III only
- II and III only **correct**
- I only
- I, II, and III



First, we define $f(x,y)=(x+3)(y-3)^{2}.$ Then, our differential equation is $\frac{\text{d}y}{\text{d}x}=f(x,y).$ 

Notice that $f(x,y)=0$ when $x=-3$ or $y=3.$ This divides the $xy$-plane into four regions, as shown below.

![](plots/f089bf8306c9769737a8-partition.png)

If we compute the sign of $f(x,y)$ in each of those four regions (by considering some test points, for example), we get the following:

![](plots/f089bf8306c9769737a8-signs.png)

With that in mind, let's check each statement:

- Statement I is false. If $x<-3$ and $y<3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement II is true. If $x<-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)<0.
$$

This implies that the slope of the slope field is negative for any point $(x,y)$ in this region.

- Statement III is true. If $x>-3$ and $y>3,$ then according to our diagram, we have

$$
{\frac{\text{d}y}{\text{d}x}|}_{(x,y)}=f(x,y)>0.
$$

This implies that the slope of the slope field is positive for any point $(x,y)$ in this region.

Therefore, the correct answer is "II and III only."


