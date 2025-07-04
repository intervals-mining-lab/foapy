# References

## Mathematical Definition


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

Define $B = \{ Start, End \} \subset \{ Binding \}$

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
