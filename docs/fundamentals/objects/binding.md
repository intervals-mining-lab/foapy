# Binding

A __binding__ is a method of iterating over equivalent elements of the sequence.
Two binding ​are defined - $Start$ and $End$.
$Start$ binding seeks back the previous occurrence of the element, and the $End$ binding seeks the next occurrence.
In practice, there is no good reason to prefer one binding over the other.
The definition of all possible `binding` is made in the interests of a consistent and fully encompassing mathematical theory.

## Mathematical Definition

=== "Old"
    Let $X$ is [_Carrier set_](./carrier_set.md#Mathematical Definition)

    Let $S$ is [_Sequence_](./sequence.md#Mathematical Definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

    Let $P$ is _n-tuple_ of `iterating positions` of equivalent elements $P : \{1,...,n\} \longrightarrow \{0,...,n+1\}$

    Define

    $$Binding : \big\{S\big\} \longrightarrow \big\{P \big\},$$

    $$if \ \exists \ Binding^{-1} : \big\{P \big\} \longrightarrow \big\{\{1,...,n\} \longrightarrow \{1,...,m\}\big\}\ that$$

    $$\forall i \in \{1,...,n\} Binding(S)(i) = Binding(Binding^{-1}(Binding(S)))(i)$$

    $$Start(S)(i) = \Bigg\{\begin{array}{l} max \big\{j \in \{1,..., i - 1\}\big|S(j) = S(i) \big\} & if \ exists \\ 0 & otherwise   \end{array}$$

    $$Start^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{1,...i\} | P(j)=0 >\big| & if \ P(i)=0 \\ Start^{-1}(P, P(i)) & otherwise   \end{array}$$

    $$End(S)(i) = \Bigg\{\begin{array}{l} min \big\{j \in \{i+1,..., n\}\big|S(j) = S(i) \big\} & if \ exists \\ n+1 & \ otherwise   \end{array}$$

    $$End^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{i,...n\} | P(j)=n+1 >\big| & if \ P(i)=n+1 \\ End^{-1}(P, P(i)) & otherwise   \end{array}$$

    Define $B = \{ Start, End \} \subset \{ Binding \}$


=== "New"
    Let $X$ is [_Carrier set_](./carrier_set.md#Mathematical Definition)

    Let $S$ is [_Sequence_](./sequence.md#Mathematical Definition)  length of $n$ described as function $S : \{1,...,n\} \longrightarrow X$

    Let

    $$S_{cycled} : \big\{ \{1,...,n\} \longrightarrow X \big\} \longrightarrow \big\{ Z \longrightarrow X \big\}$$

    $$S_{cycled}(S)(i) = S\big( i - n \times \lfloor ( i - 1) \div n \rfloor \big)$$

    $$R : \{1,...,n\} \longrightarrow \{-n,...,2n\} $$

    $$Binding : \big\{S\big\} \longrightarrow \big\{ R \big\},$$


    $$if \ \exists \ Binding^{-1} : \big\{R \big\} \longrightarrow \big\{\{1,...,n\} \longrightarrow \{1,...,m\}\big\}\ that$$

    $$\forall i \in \{1,...,n\} Binding(R)(i) = Binding(Binding^{-1}(Binding(R)) )(i)$$


    $$Start(S)(i) = max(\big\{j \in Z \big|S_{cycled}(j) = S(i) \land j \leq i-1 \big\})$$

    $$Start^{-1}(R)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{1,...i\} | R(j)=\leq 0 >\big| & if \ R(i) \leq 0 \\ Start^{-1}(R, R(i)) & otherwise   \end{array}$$

    $$End(S)(i) = min(\big\{j \in Z \big|S_{cycled}(j) = S(i) \land j \geq i+1 \big\}$$

    $$End^{-1}(R)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{i,...n\} | R(j) \geq n+1 >\big| & if \ R(i) \geq n+1 \\ End^{-1}(R, R(i)) & otherwise   \end{array}$$

    Lemma:

    $$\forall S : \{1,...,n\} \longrightarrow X, \ \forall i \in \{1,..n\} \Big| 1 \leq |\ Start(S)(i) - i\ | \leq n \land 1 \leq | End(S)(i) - i\ | \leq n$$


    Let $Mode$ is __Mode__

    $$Mode : \big\{ \{1,...,n\} \longrightarrow \{-n,...,2n\} \big\} \longrightarrow \big\{ \{1,...,n\} \longrightarrow  \{1,...,n\} \big\}$$

    Define

    $$Cycle(R)(i) = \Bigg\{\begin{array}{l} R(i) - i  & , R(j) > j \ | \ \forall j \in \{1,..,n\} \\ i - R(i)  & , R(j) < j \ | \ \forall j \in \{1,..,n\}\end{array}$$

    $$Cycle^{-1}(IO)(i) = \Bigg\{\begin{array}{l} i - IO(i) & , \exists j \in \{1,..,n\} | IO(j) > j  \\ i + IO(i) & , \exists j \in \{1,..,n\} | IO(j) > n - j \end{array}$$

    $$Boundary(R)(i) = \Bigg\{\begin{array}{l} i  & , R(i) < 1 \\ Cycle(R)(i)  & , 1 \leq R(i) \leq n \\ n - i + 1 & , R(i) > n \end{array}$$

    $$Boundary^{-1}(IO)(i) = \Bigg\{\begin{array}{l} i - IO(i) & , \exists j \in \{1,..,n\} | IO(j) = j  \\ i + IO(i) & , \exists j \in \{1,..,n\} | IO(j) = n - j +1\end{array}$$



    $$Binding : M \times \big\{S\big\} \longrightarrow \big\{ \big\},$$


    $$if \ \exists \ Binding^{-1} : M \times \big\{R \big\} \longrightarrow \big\{\{1,...,n\} \longrightarrow \{1,...,m\}\big\}\ that$$

    $$\forall i \in \{1,...,n\} Binding(mo, R)(i) = Binding(mo, R)( Binding^{-1}(mo, Binding(mo, R)) )(i)$$

    $$Start(S)(i) = \Bigg\{\begin{array}{l} max \big\{j \in \{1,..., i - 1\}\big|S(j) = S(i) \big\} & if \ exists \\ m(S, i) & otherwise   \end{array}$$

    $$Start^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{1,...i\} | P(j)=0 >\big| & if \ P(i)=0 \\ Start^{-1}(P, P(i)) & otherwise   \end{array}$$

    $$End(S)(i) = \Bigg\{\begin{array}{l} min \big\{j \in \{i+1,..., n\}\big|S(j) = S(i) \big\} & if \ exists \\ n+1 & \ otherwise   \end{array}$$

    $$End^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{i,...n\} | P(j)=n+1 >\big| & if \ P(i)=n+1 \\ End^{-1}(P, P(i)) & otherwise   \end{array}$$

    Define $B = \{ Start, End \} \subset \{ Binding \}$


<!-- $$if \ \exists \ Binding^{-1} : \big\{P \big\} \longrightarrow \big\{\{1,...,n\} \longrightarrow \{1,...,m\}\big\}\ that$$

$$\forall i \in \{1,...,n\} Binding(S)(i) = Binding(Binding^{-1}(Binding(S)))(i)$$

$$Start(S)(i) = \Bigg\{\begin{array}{l} max \big\{j \in \{1,..., i - 1\}\big|S(j) = S(i) \big\} & if \ exists \\ 0 & otherwise   \end{array}$$

$$Start^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{1,...i\} | P(j)=0 >\big| & if \ P(i)=0 \\ Start^{-1}(P, P(i)) & otherwise   \end{array}$$

$$End(S)(i) = \Bigg\{\begin{array}{l} min \big\{j \in \{i+1,..., n\}\big|S(j) = S(i) \big\} & if \ exists \\ n+1 & \ otherwise   \end{array}$$

$$End^{-1}(P)(i) = \Bigg\{\begin{array}{l} \big|<j \in \{i,...n\} | P(j)=n+1 >\big| & if \ P(i)=n+1 \\ End^{-1}(P, P(i)) & otherwise   \end{array}$$ -->



## Examples

=== "$Start$ binding"

    ``` mermaid
    block-beta
      columns 8
      p0["0"]        p1["1"] space:3         p5["5"]                p6["n"] p7["n + 1"]
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["⊥"]
      e0["0 = Start(1)"]:2 space:6
      space      t1["1 = Start(5)"]:5         space:2

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p5,p6,p7 position

      classDef c1 fill:#ff7f0e,color:#fff;
      classDef c2 fill:#ffbb78,color:#000;
      classDef c2a fill:#ffbb788a,color:#000;
      classDef c3 fill:#2ca02c,color:#fff;
      classDef c4 fill:#98df8a,color:#000;
      classDef c4a fill:#98df8a8a,color:#000;
      classDef c5 fill:#d62728,color:#fff;
      classDef c6 fill:#ff9896,color:#000;
      classDef c6a fill:#ff98968a,color:#000;
      classDef c7 fill:#9467bd,color:#fff;
      classDef c8 fill:#c5b0d5,color:#000;
      classDef c9 fill:#8c564b,color:#fff;
      classDef c10 fill:#c49c94,color:#000;
      classDef c11 fill:#e377c2,color:#fff;
      classDef c12 fill:#f7b6d2,color:#000;
      classDef c13 fill:#bcbd22,color:#fff;
      classDef c14 fill:#dbdb8d,color:#000;
      classDef c14a fill:#dbdb8d8a,color:#000;
      classDef c15 fill:#17becf,color:#fff;
      classDef c16 fill:#9edae5,color:#000;

      class s1,s5 c4
      class inf,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```

=== "$End$ binding"

    ``` mermaid
    block-beta
      columns 8
      p0["0"]        p1["1"] space:3         p5["5"]                p6["n"] p7["n + 1"]
      inf["⊥"] s1["A"] s2["C"] s3["T"] s4["C"] s5["A"] s6["G"] sup["⊥"]
      space      t1["End(1) = 5"]:5         space:2
      space:5 e0["End(5) = n+1"]:3

      classDef imaginary fill:#526cfe09,color:#000,stroke-dasharray: 10 5;
      classDef position fill:#fff,color:#000,stroke-width:0px;
      class inf,sup imaginary
      class p0,p1,p5,p6,p7 position

      classDef c1 fill:#ff7f0e,color:#fff;
      classDef c2 fill:#ffbb78,color:#000;
      classDef c2a fill:#ffbb788a,color:#000;
      classDef c3 fill:#2ca02c,color:#fff;
      classDef c4 fill:#98df8a,color:#000;
      classDef c4a fill:#98df8a8a,color:#000;
      classDef c5 fill:#d62728,color:#fff;
      classDef c6 fill:#ff9896,color:#000;
      classDef c6a fill:#ff98968a,color:#000;
      classDef c7 fill:#9467bd,color:#fff;
      classDef c8 fill:#c5b0d5,color:#000;
      classDef c9 fill:#8c564b,color:#fff;
      classDef c10 fill:#c49c94,color:#000;
      classDef c11 fill:#e377c2,color:#fff;
      classDef c12 fill:#f7b6d2,color:#000;
      classDef c13 fill:#bcbd22,color:#fff;
      classDef c14 fill:#dbdb8d,color:#000;
      classDef c14a fill:#dbdb8d8a,color:#000;
      classDef c15 fill:#17becf,color:#fff;
      classDef c16 fill:#9edae5,color:#000;

      class s1,s5 c4
      class sup,t1,e0 c4a
      class pomn,p00,p01,p06,p07,p02n position
      class t1,t2,t5,e0,e1 position

    ```
