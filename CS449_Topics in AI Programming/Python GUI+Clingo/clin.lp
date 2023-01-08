{nod(X)}:-node(X).

:-path(X,Y),not nod(X),nod(Y).

:-path(X,Y),nod(X),not nod(Y).

:-path(X,Y),not nod(X),not nod(Y).

:-path(X,Y),N=#count{X1:nod(X1),X1!=X, X1!=Y},N=0, N1=#count{X1:connect(X1,Y,_), nod(X1)},N2=#count{X1:connect(Y,X1,_), nod(X1)},N1+N2!=1.

:-path(X,Y),N=#count{X1:nod(X1),X1!=X, X1!=Y},N=0, N3=#count{X1:connect(X,X1,_), nod(X1)},N4=#count{X1:connect(X1,X,_), nod(X1)},N3+N4!=1.

:-path(X,Y), X1!=X, X1!=Y, nod(X1), N1=#count{X2:connect(X1,X2,_),nod(X2)},N2=#count{X2:connect(X2,X1,_), nod(X2)}, N1+N2!=2.

:-path(X,Y),N=#count{X1:nod(X1),X1!=X, X1!=Y},N!=0, N1=#count{X1:connect(X,X1,_),path(X,Y), nod(X1),X1!=X, X1!=Y},
 N2=#count{X1:connect(X1,X,_), nod(X1),path(X,Y), nod(X1),X1!=X, X1!=Y}, N1+N2!=1.

:-path(X,Y),N=#count{X1:nod(X1),X1!=X, X1!=Y},N!=0, N1=#count{X1:connect(Y,X1,_),path(X,Y), nod(X1),X1!=X, X1!=Y},
 N2=#count{X1:connect(X1,Y,_), nod(X1),path(X,Y), nod(X1),X1!=X, X1!=Y}, N1+N2!=1.


1{con(X1,Y1,N)}1:-connect(X1,Y1,N),nod(X1),nod(Y1).

n(X,Y,N):-path(X,Y), N=#sum{N10,X1,Y1:con(X1,Y1,N10)}, 1=#count{N10,X1,Y1:con(X1,Y1,N10)}.

n(X,Y,N):-path(X,Y), N1=#sum{N10,X1,Y1:con(X1,Y1,N10)}, N2=#sum{N20,X1,Y1:con(X1,Y1,N20), path(X,Y), X1=X, Y1=Y}, 
N3=#sum{N30,X1,Y1:con(X1,Y1,N30), path(X,Y), X1=Y, Y1=X}, N=N1-N2-N3,1<#count{N10,X1,Y1:con(X1,Y1,N10)}.

#minimize{N:n(X1,Y1,N)}.

#show con/3.
#show n/3.
#show nod/1.