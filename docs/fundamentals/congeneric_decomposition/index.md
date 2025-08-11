# Congeneric Decomposition

Any [_Sequence_](../order/sequence.md) (including [_Partial Sequence_](../partials_and_congenerics/sequence/index.md)) can be decomposed into $m$ (power of an [_Alphabet_](../order/alphabet.md)) [_Congeneric Sequences_](../partials_and_congenerics/sequence/congeneric.md) length of $l$. Each _congeneric sequence_ would be [_compatible_](../partials_and_congenerics/sequence/index.md#compatibility) with all other _congeneric sequences_, so the procedure is invertible. Result of the decomposition can be represented as a matrix $m \times l$

The sequence

``` mermaid
block-beta
  columns 36
  seq1["I"] seq2["N"] seq3["T"] seq4["E"] seq5["L"] seq6["L"] seq7["I"] seq8["G"] seq9["E"] seq10["N"]
  seq11["C"] seq12["E"] seq13[" "] seq14["I"] seq15["S"] seq16[" "] seq17["T"] seq18["H"] seq19["E"] seq20[" "]
  seq21["A"] seq22["B"] seq23["I"] seq24["L"] seq25["I"] seq26["T"] seq27["Y"] seq28[" "] seq29["T"] seq30["O"]
  seq31[" "] seq32["A"] seq33["D"] seq34["A"] seq35["P"] seq36["T"]

  classDef c1 fill:#ff7f0e,color:#fff;
  classDef c2 fill:#ffbb78,color:#000;
  classDef c3 fill:#2ca02c,color:#fff;
  classDef c4 fill:#98df8a,color:#000;
  classDef c5 fill:#d62728,color:#fff;
  classDef c6 fill:#ff9896,color:#000;
  classDef c7 fill:#9467bd,color:#fff;
  classDef c8 fill:#c5b0d5,color:#000;
  classDef c9 fill:#8c564b,color:#fff;
  classDef c10 fill:#c49c94,color:#000;
  classDef c11 fill:#e377c2,color:#fff;
  classDef c12 fill:#f7b6d2,color:#000;
  classDef c13 fill:#bcbd22,color:#fff;
  classDef c14 fill:#dbdb8d,color:#000;
  classDef c15 fill:#17becf,color:#fff;
  classDef c16 fill:#9edae5,color:#000;
  class seq1,seq7,seq14,seq23,seq25,i1,i7,i14,i23,i25 c1
  class seq2,seq10,n2,n10 c2
  class seq3,seq17,seq26,seq29,seq36,t3,t17,t26,t29,t36 c3
  class seq4,seq9,seq12,seq19,e4,e9,e12,e19  c4
  class seq5,seq6,seq24,l5,l6,l24 c5
  class seq8,g8 c6
  class seq11,c11 c7
  class seq13,seq16,seq20,seq28,seq31,sp13,sp16,sp20,sp28,sp31 c8
  class seq15,s15 c9
  class seq18,h18 c10
  class seq21,seq32,seq34,a21,a32,a34 c11
  class seq22,b22 c12
  class seq27,y27 c13
  class seq30,o30 c14
  class seq33,d33 c15
  class seq35,p35 c16
```

decomposed into

``` mermaid
block-beta
  columns 37
  diag["⟍"] col1["1"] col2["2"] space:16 col19["..."] space:16 col36["l"]
  row1["1"] i1["I"] i2["-"] i3["-"] i4["-"] i5["-"] i6["-"] i7["I"] i8["-"] i9["-"] i10["-"]
  i11["-"] i12["-"] i13["-"] i14["I"] i15["-"] i16["-"] i17["-"] i18["-"] i19["-"] i20["-"]
  i21["-"] i22["-"] i23["I"] i24["-"] i25["I"] i26["-"] i27["-"] i28["-"] i29["-"] i30["-"]
  i31["-"] i32["-"] i33["-"] i34["-"] i35["-"] i36["-"]
  row2["2"] n1["-"] n2["N"] n3["-"] n4["-"] n5["-"] n6["-"] n7["-"] n8["-"] n9["-"] n10["N"]
  n11["-"] n12["-"] n13["-"] n14["-"] n15["-"] n16["-"] n17["-"] n18["-"] n19["-"] n20["-"]
  n21["-"] n22["-"] n23["-"] n24["-"] n25["-"] n26["-"] n27["-"] n28["-"] n29["-"] n30["-"]
  n31["-"] n32["-"] n33["-"] n34["-"] n35["-"] n36["-"]
  space t1["-"] t2["-"] t3["T"] t4["-"] t5["-"] t6["-"] t7["-"] t8["-"] t9["-"] t10["-"]
  t11["-"] t12["-"] t13["-"] t14["-"] t15["-"] t16["-"] t17["T"] t18["-"] t19["-"] t20["-"]
  t21["-"] t22["-"] t23["-"] t24["-"] t25["-"] t26["T"] t27["-"] t28["-"] t29["T"] t30["-"]
  t31["-"] t32["-"] t33["-"] t34["-"] t35["-"] t36["T"]
  space e1["-"] e2["-"] e3["-"] e4["E"] e5["-"] e6["-"] e7["-"] e8["-"] e9["E"] e10["-"]
  e11["-"] e12["E"] e13["-"] e14["-"] e15["-"] e16["-"] e17["-"] e18["-"] e19["E"] e20["-"]
  e21["-"] e22["-"] e23["-"] e24["-"] e25["-"] e26["-"] e27["-"] e28["-"] e29["-"] e30["-"]
  e31["-"] e32["-"] e33["-"] e34["-"] e35["-"] e36["-"]
  space l1["-"] l2["-"] l3["-"] l4["-"] l5["L"] l6["L"] l7["-"] l8["-"] l9["-"] l10["-"]
  l11["-"] l12["-"] l13["-"] l14["-"] l15["-"] l16["-"] l17["-"] l18["-"] l19["-"] l20["-"]
  l21["-"] l22["-"] l23["-"] l24["L"] l25["-"] l26["-"] l27["-"] l28["-"] l29["-"] l30["-"]
  l31["-"] l32["-"] l33["-"] l34["-"] l35["-"] l36["-"]
  space g1["-"] g2["-"] g3["-"] g4["-"] g5["-"] g6["-"] g7["-"] g8["G"] g9["-"] g10["-"]
  g11["-"] g12["-"] g13["-"] g14["-"] g15["-"] g16["-"] g17["-"] g18["-"] g19["-"] g20["-"]
  g21["-"] g22["-"] g23["-"] g24["-"] g25["-"] g26["-"] g27["-"] g28["-"] g29["-"] g30["-"]
  g31["-"] g32["-"] g33["-"] g34["-"] g35["-"] g36["-"]
  space c1["-"] c2["-"] c3["-"] c4["-"] c5["-"] c6["-"] c7["-"] c8["-"] c9["-"] c10["-"]
  c11["C"] c12["-"] c13["-"] c14["-"] c15["-"] c16["-"] c17["-"] c18["-"] c19["-"] c20["-"]
  c21["-"] c22["-"] c23["-"] c24["-"] c25["-"] c26["-"] c27["-"] c28["-"] c29["-"] c30["-"]
  c31["-"] c32["-"] c33["-"] c34["-"] c35["-"] c36["-"]
  space sp1["-"] sp2["-"] sp3["-"] sp4["-"] sp5["-"] sp6["-"] sp7["-"] sp8["-"] sp9["-"] sp10["-"]
  sp11["-"] sp12["-"] sp13[" "] sp14["-"] sp15["-"] sp16[" "] sp17["-"] sp18["-"] sp19["-"] sp20[" "]
  sp21["-"] sp22["-"] sp23["-"] sp24["-"] sp25["-"] sp26["-"] sp27["-"] sp28[" "] sp29["-"] sp30["-"]
  sp31[" "] sp32["-"] sp33["-"] sp34["-"] sp35["-"] sp36["-"]
  row9["⋮"] s1["-"] s2["-"] s3["-"] s4["-"] s5["-"] s6["-"] s7["-"] s8["-"] s9["-"] s10["-"]
  s11["-"] s12["-"] s13["-"] s14["-"] s15["S"] s16["-"] s17["-"] s18["-"] s19["-"] s20["-"]
  s21["-"] s22["-"] s23["-"] s24["-"] s25["-"] s26["-"] s27["-"] s28["-"] s29["-"] s30["-"]
  s31["-"] s32["-"] s33["-"] s34["-"] s35["-"] s36["-"]
  space h1["-"] h2["-"] h3["-"] h4["-"] h5["-"] h6["-"] h7["-"] h8["-"] h9["-"] h10["-"]
  h11["-"] h12["-"] h13["-"] h14["-"] h15["-"] h16["-"] h17["-"] h18["H"] h19["-"] h20["-"]
  h21["-"] h22["-"] h23["-"] h24["-"] h25["-"] h26["-"] h27["-"] h28["-"] h29["-"] h30["-"]
  h31["-"] h32["-"] h33["-"] h34["-"] h35["-"] h36["-"]
  space a1["-"] a2["-"] a3["-"] a4["-"] a5["-"] a6["-"] a7["-"] a8["-"] a9["-"] a10["-"]
  a11["-"] a12["-"] a13["-"] a14["-"] a15["-"] a16["-"] a17["-"] a18["-"] a19["-"] a20["-"]
  a21["A"] a22["-"] a23["-"] a24["-"] a25["-"] a26["-"] a27["-"] a28["-"] a29["-"] a30["-"]
  a31["-"] a32["A"] a33["-"] a34["A"] a35["-"] a36["-"]
  space b1["-"] b2["-"] b3["-"] b4["-"] b5["-"] b6["-"] b7["-"] b8["-"] b9["-"] b10["-"]
  b11["-"] b12["-"] b13["-"] b14["-"] b15["-"] b16["-"] b17["-"] b18["-"] b19["-"] b20["-"]
  b21["-"] b22["B"] b23["-"] b24["-"] b25["-"] b26["-"] b27["-"] b28["-"] b29["-"] b30["-"]
  b31["-"] b32["-"] b33["-"] b34["-"] b35["-"] b36["-"]
  space y1["-"] y2["-"] y3["-"] y4["-"] y5["-"] y6["-"] y7["-"] y8["-"] y9["-"] y10["-"]
  y11["-"] y12["-"] y13["-"] y14["-"] y15["-"] y16["-"] y17["-"] y18["-"] y19["-"] y20["-"]
  y21["-"] y22["-"] y23["-"] y24["-"] y25["-"] y26["-"] y27["Y"] y28["-"] y29["-"] y30["-"]
  y31["-"] y32["-"] y33["-"] y34["-"] y35["-"] y36["-"]
  space o1["-"] o2["-"] o3["-"] o4["-"] o5["-"] o6["-"] o7["-"] o8["-"] o9["-"] o10["-"]
  o11["-"] o12["-"] o13["-"] o14["-"] o15["-"] o16["-"] o17["-"] o18["-"] o19["-"] o20["-"]
  o21["-"] o22["-"] o23["-"] o24["-"] o25["-"] o26["-"] o27["-"] o28["-"] o29["-"] o30["O"]
  o31["-"] o32["-"] o33["-"] o34["-"] o35["-"] o36["-"]
  space d1["-"] d2["-"] d3["-"] d4["-"] d5["-"] d6["-"] d7["-"] d8["-"] d9["-"] d10["-"]
  d11["-"] d12["-"] d13["-"] d14["-"] d15["-"] d16["-"] d17["-"] d18["-"] d19["-"] d20["-"]
  d21["-"] d22["-"] d23["-"] d24["-"] d25["-"] d26["-"] d27["-"] d28["-"] d29["-"] d30["-"]
  d31["-"] d32["-"] d33["D"] d34["-"] d35["-"] d36["-"]
  row16["m"] p1["-"] p2["-"] p3["-"] p4["-"] p5["-"] p6["-"] p7["-"] p8["-"] p9["-"] p10["-"]
  p11["-"] p12["-"] p13["-"] p14["-"] p15["-"] p16["-"] p17["-"] p18["-"] p19["-"] p20["-"]
  p21["-"] p22["-"] p23["-"] p24["-"] p25["-"] p26["-"] p27["-"] p28["-"] p29["-"] p30["-"]
  p31["-"] p32["-"] p33["-"] p34["-"] p35["P"] p36["-"]


  classDef c1 fill:#ff7f0e,color:#fff;
  classDef c2 fill:#ffbb78,color:#000;
  classDef c3 fill:#2ca02c,color:#fff;
  classDef c4 fill:#98df8a,color:#000;
  classDef c5 fill:#d62728,color:#fff;
  classDef c6 fill:#ff9896,color:#000;
  classDef c7 fill:#9467bd,color:#fff;
  classDef c8 fill:#c5b0d5,color:#000;
  classDef c9 fill:#8c564b,color:#fff;
  classDef c10 fill:#c49c94,color:#000;
  classDef c11 fill:#e377c2,color:#fff;
  classDef c12 fill:#f7b6d2,color:#000;
  classDef c13 fill:#bcbd22,color:#fff;
  classDef c14 fill:#dbdb8d,color:#000;
  classDef c15 fill:#17becf,color:#fff;
  classDef c16 fill:#9edae5,color:#000;
  classDef text fill:#fff,color:#000,stroke-width:0px

  class row1,row2,row9,row16 text
  class col1,col2,col19,col36 text
  class diag text


  class i2,i3,i4,i5,i6,i8,i9,i10 text
  class i11,i12,i13,i15,i16,i17,i18,i19,i20 text
  class i21,i22,i24,i26,i27,i28,i29,i30 text
  class i31,i32,i33,i34,i35,i36 text

  class n1,n3,n4,n5,n6,n7,n8,n9 text
  class n11,n12,n13,n14,n15,n16,n17,n18,n19,n20 text
  class n21,n22,n23,n24,n25,n26,n27,n28,n29,n30 text
  class n31,n32,n33,n34,n35,n36 text

  class t1,t2,t4,t5,t6,t7,t8,t9,t10 text
  class t11,t12,t13,t14,t15,t16,t18,t19,t20 text
  class t21,t22,t23,t24,t25,t27,t28,t30 text
  class t31,t32,t33,t34,t35 text

  class e1,e2,e3,e5,e6,e7,e8,e10 text
  class e11,e13,e14,e15,e16,e17,e18,e20 text
  class e21,e22,e23,e24,e25,e26,e27,e28,e29,e30 text
  class e31,e32,e33,e34,e35,e36 text

  class l1,l2,l3,l4,l7,l8,l9,l10 text
  class l11,l12,l13,l14,l15,l16,l17,l18,l19,l20 text
  class l21,l22,l23,l25,l26,l27,l28,l29,l30 text
  class l31,l32,l33,l34,l35,l36 text

  class g1,g2,g3,g4,g5,g6,g7,g9,g10 text
  class g11,g12,g13,g14,g15,g16,g17,g18,g19,g20 text
  class g21,g22,g23,g24,g25,g26,g27,g28,g29,g30 text
  class g31,g32,g33,g34,g35,g36 text

  class c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 text
  class c12,c13,c14,c15,c16,c17,c18,c19,c20 text
  class c21,c22,c23,c24,c25,c26,c27,c28,c29,c30 text
  class c31,c32,c33,c34,c35,c36 text

  class sp1,sp2,sp3,sp4,sp5,sp6,sp7,sp8,sp9,sp10 text
  class sp11,sp12,sp14,sp15,sp17,sp18,sp19 text
  class sp21,sp22,sp23,sp24,sp25,sp26,sp27,sp28,sp29,sp30 text
  class sp31,sp32,sp33,sp34,sp35,sp36 text

  class s1,s2,s3,s4,s5,s6,s7,s8,s9,s10 text
  class s11,s12,s13,s14,s16,s17,s18,s19,s20 text
  class s21,s22,s23,s24,s25,s26,s27,s28,s29,s30 text
  class s31,s32,s33,s34,s35,s36 text

  class h1,h2,h3,h4,h5,h6,h7,h8,h9,h10 text
  class h11,h12,h13,h14,h15,h16,h17,h19,h20 text
  class h21,h22,h23,h24,h25,h26,h27,h28,h29,h30 text
  class h31,h32,h33,h34,h35,h36 text


  class a1,a2,a3,a4,a5,a6,a7,a8,a9,a10 text
  class a11,a12,a13,a14,a15,a16,a17,a18,a19,a20 text
  class a22,a23,a24,a25,a26,a27,a28,a29,a30 text
  class a31,a33,a35,a36 text

  class b1,b2,b3,b4,b5,b6,b7,b8,b9,b10 text
  class b11,b12,b13,b14,b15,b16,b17,b18,b19,b20 text
  class b21,b23,b24,b25,b26,b27,b28,b29,b30 text
  class b31,b32,b33,b34,b35,b36 text

  class y1,y2,y3,y4,y5,y6,y7,y8,y9,y10 text
  class y11,y12,y13,y14,y15,y16,y17,y18,y19,y20 text
  class y21,y22,y23,y24,y25,y26,y28,y29,y30 text
  class y31,y32,y33,y34,y35,y36 text

  class o1,o2,o3,o4,o5,o6,o7,o8,o9,o10 text
  class o11,o12,o13,o14,o15,o16,o17,o18,o19,o20 text
  class o21,o22,o23,o24,o25,o26,o27,o28,o29 text
  class o31,o32,o33,o34,o35,o36 text

  class d1,d2,d3,d4,d5,d6,d7,d8,d9,d10 text
  class d11,d12,d13,d14,d15,d16,d17,d18,d19,d20 text
  class d21,d22,d23,d24,d25,d26,d27,d28,d29,d30 text
  class d31,d32,d34,d35,d36 text

  class p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 text
  class p11,p12,p13,p14,p15,p16,p17,p18,p19,p20 text
  class p21,p22,p23,p24,p25,p26,p27,p28,p29,p30 text
  class p31,p32,p33,p34,p36 text

  class seq1,seq7,seq14,seq23,seq25,i1,i7,i14,i23,i25 c1
  class seq2,seq10,n2,n10 c2
  class seq3,seq17,seq26,seq29,seq36,t3,t17,t26,t29,t36 c3
  class seq4,seq9,seq12,seq19,e4,e9,e12,e19  c4
  class seq5,seq6,seq24,l5,l6,l24 c5
  class seq8,g8 c6
  class seq11,c11 c7
  class seq13,seq16,seq20,seq28,seq31,sp13,sp16,sp20,sp28,sp31 c8
  class seq15,s15 c9
  class seq18,h18 c10
  class seq21,seq32,seq34,a21,a32,a34 c11
  class seq22,b22 c12
  class seq27,y27 c13
  class seq30,o30 c14
  class seq33,d33 c15
  class seq35,p35 c16
```

Applying [operations](../order/index.md) to [_Congeneric sequences_](./sequences.md) and its derivatives produces [_Congenerics Orders_](./orders.md), [_Congenerics Intervals Chains_](./intervals_chains.md),
[_Congenerics Intervals Distributions_](./intervals_distribution.md) and finally [_Characteristics_](./characteristics/index.md) specific for _congeneric_ matrix.
