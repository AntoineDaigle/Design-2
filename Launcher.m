%UNITÉS DU SI PARTOUT

%Masse deposee
M = 0.05;

%PARAMÈTRES À MODIFIER SUR L'INTERFACE

%Paramètres de la poutre
b = 74e-3;
h = 1.59e-3;
l = 301e-3;
L = 240e-3;
m = 66e-3;
densite = 1937.18;
f = 12.17;
%Densité linéique
mu = densite*b*h;
%Moment quadratique
J = b*h^3/12;
%Module de Young
E = (mu*(2*pi*f)^2/J)*(L/1.875)^4;
%E = 1.4432*10^10;
%Amortissement
gamma = 1.5*5.91;
B = gamma*(mu*L + M);
%Nombre d'incréments à calculer (par exemple, 0 à 11000 bonds de dt dans la
%simulation)
%nx = 20;
nx = 19;
nt = 8000;
%Incréments
dt = 2e-5;
dx = L/(nx-1);
%Liste d'éléments spaciaux
x = -dx:dx:L+dx; 
nx = nx + 2;
%Array de force appliquée
F = zeros(1, nx);

% w = 1 * fliplr(0.001*sin(pi*x/(2*L)));
%Initialisation des arrays d'état passé, présent et futur
w_old = zeros(1, nx);
w = zeros(1, nx);
w_new = zeros(1, nx);

%Forme initiale de lame
w_init = 1:nx; 

%Position du bout de la lame en fonction du temps
%position_bout = zeros(1, nt+1); 

%Pour l'EDO
coeff1 = (E * J)/(dx^4);
coeff2 = mu/(dt^2);
coeff3 = B/dt;
coeff4 = ((mu/dt^2)+(B/dt))^(-1);
coeffs = [coeff1, coeff2, coeff3, coeff4];

%Pour le systeme 2e ordre
a1 = (M+mu*L)*L^4 / (l*E*J*1.875^4);
b1 = 5.91*(M+mu*L);
c1 = 3*E*J/L^3;
K = 1;

ModelWorkspace = get_param('mode_lame_2019b','ModelWorkspace');
assignin(ModelWorkspace,'coeffs',coeffs);
assignin(ModelWorkspace,'nx',nx);
assignin(ModelWorkspace,'dx',dx);
assignin(ModelWorkspace,'w_old',w_old);
assignin(ModelWorkspace,'w',w);
assignin(ModelWorkspace,'w_new',w_new);
assignin(ModelWorkspace,'w_init',w_init);
assignin(ModelWorkspace,'F',F);
assignin(ModelWorkspace,'a1',a1);
assignin(ModelWorkspace,'b1',b1);
assignin(ModelWorkspace,'c1',c1);
assignin(ModelWorkspace,'K',K);
assignin(ModelWorkspace,'dt',dt);


%sim('modelName','StartTime','0','StopTime','10','FixedStep','0.2');
%sim("mode_lame_2019b",'StartTime',"0",'StopTime',"3",'FixedStep',"0.1")
