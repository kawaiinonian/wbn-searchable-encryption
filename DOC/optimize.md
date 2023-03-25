旧算法的$OfflineAuth$过程中，DUA发给DUB的$offtok$实际上是$g^{F(K_{U_0},d)\cdot F(K_{U_0},u_1)\cdot F(K_{U_1},u_2)\cdot ...}$，而$F(K_{U_i},u_{i+1})^{-1}$则存储在$Aset$里面，因此每次要得到$g^{F(K_{U_0},d)}$，也就必须一并上传$AList$

考虑通过动态优化算法减少通讯开销。

设三个用户$U_1,U_2,U_3$，授权关系是$U_1\rightarrow U_2\rightarrow U_3$，其中$aid_1=F(\tilde{K_{u_1}},u_2),\ aid_2=F(\tilde{K_{u_2}},u_3)$

我们令服务器中存储$Aset[aid]=g^{F(K_{U_0},u_1)^{-1}\cdot F(K_{U_1},u_2)^{-1}\cdot ...}$，每次更新Aset的公式是$Aset[aid_2]=Aset[aid_1]^{F(K_{u_2},u_3)^{-1}}$

这样每次$u_3$进行查找的时候，只需给服务器上传自己的$offtok$和$aid_2$即可。进一步，每次的$OfflineAuth$也只需要传一个$aid$