close all
clear all
clc


% La lame
b = 73e-3;       % Base (largeur) 73 mm
h = 1.65e-3;     % Hauteur 1.65 mm
L = 240e-3;      % Longueur 240 mm 

J = b*h^3/12;    % Moment d'aire

m = 80;            % Masse moyenne de la lame et d'une pes�e
% Mat�riau

E = 1.8334e10;      % Module de Young    avant:3.7008e9  apr�s:1.8334e10
dens = 1937.18 ;     % Densit� Kg/m^3
mu =  dens*b*h;  % Masse lin�ique kg/m
 

B = 5.3/(2*m);      % Amortissement qu'on rajoute (c'est l'exponentielle des donn�es exp�rimentales (e^-gamma) c'est gamma)
F = -(1);         %Force du poids pesant sur la lame (F=mg environ 1 Newton)
F_actio = (1);   %Force de l'actionneur remontant la lame

dt = 9e-4;       % incr�ment temporel

nx = 20;         % Nb d'�l�ments spatiaux
nt = 9000;       % Nb d'�l�ments temporels


dx = L/(nx-1);        % incr�ment spatial
x  = -dx:dx:L+dx;     % grille spatiale
nx = nx+2;            % Pour s'ajuster pour avoir le dx de droite et de gauche

dx_n = dx/L;     % On travaille en dx normalis�
%dx_n = dx;        % Je decide de ne pas les normaliser pour augmenter la vitesse de la mod�lisation

% Stiffness params

kappa = sqrt(E*J/(mu*L^4));

% Doit �tre inf�rieur � 1/2 pour que ca soit stable
mu_simu = kappa*dt/dx_n^2;


% if(mu_simu >0.5)
%        warning('La simulation ne sera pas stable !')
% end
% 
% f1 = sqrt( (1.875/L).^4*(E*J/mu))/(2*pi)  % Fr�qunce theorique de la fondamentale
% f1 = 1.875^2*kappa/(2*pi)
%f1 = 4.73^2*kappa/(2*pi)  %% Clamped condition

%% Conditions initiales

temps = 0;
w = 1*fliplr(0.001*sin(pi*x/(2*L))-0.001);  % Conditions actuelles  fliplr(flip left to right)
w_old = w;                                  % un pas dans le pass�
w_new = zeros(1,nx);                        % ce qui sera calcul� � chaque tour (initialisation matrice de z�ros)
w_init = w;                                 % Pr�servation de la condition initiale

% POUR LA FORCE DE LA MASSE
f = zeros(1,nx);                            % On initialise un vecteur de z�ros pour la force appliqu�e (de la masse sur la lame)
f(10) = F;                                   % On applique la force sur la partie de la lame d�sir�e
%f(9, 10, 11) = F/3                         % Si on veut diviser la force sur un espace (aka le plateau)

% POUR LA FORCE DE L'ACTIONNEUR
f_a = zeros(1,nx);
f_a(10) = F_actio;

%% Vecteur qui condiendra la position de l'extr�mit� de la lame en fonction
% du temps

masse_bout = zeros(1,nt+1);

%% Pr�calcul des params de simulation pour acc�lerer la boucle

 
%coeff1 = (2-6*mu_simu^2);
%coeff2 = (4*mu_simu^2);
%coeff3 = -mu_simu^2;

coeff1 = (E*J)/(dx_n^4);
coeff2 = mu/(dt^2);
coeff3 = B/(dt);
coeff4 = ((mu/dt^2) + (B/dt))^(-1);


%% Pr�paration de la figure

h = plot(x,1000*w_init,x,1000*w_new);
xlabel('x [m]')
ylabel('D�flexion [mm]')
ylim([-1.2,1.2])
grid on


%% Boucle de simulation
for n=0:nt 
    
    w_new = zeros(1,nx) ;
    

    i = 3:nx-2;
    %w_new(i) = coeff1*w(i)+coeff2*(w(i+1)+w(i-1))+coeff3*(w(i+2)+w(i-2))-w_old(i);
    
    %�quation diff�rentielle r�solue par Sam
    w_new(i) = (-coeff1*(w(i+2)-4*w(i+1)+6*w(i)-4*w(i-1)+w(i-2)) - coeff2*(-2*w(i)+w_old(i)) + coeff3*w(i) + f(i)/dx_n + f_a(i)/dx_n)*coeff4;
    
    %% Conditions limites 
 
     w_new(1:2) =0;                 % Clamp� � zero, position et d�riv�e nulle (le bout de la lame est fixe)
   
     w_new(end-1) = 2*w_new(end-2)-w_new(end-3);    % Libre au bout d�riv�es 2e et 3e nulles
     w_new(end) = 2*w_new(end-1)-w_new(end-2);
   %  w_new(end-1:end)=0;           % Si on veut clamp� au deux bouts
    
    %% Pr�paration du prochain tour
    
    w_old = w;
    w = w_new;
    
    masse_bout(n+1) = w(end);
    
    %% Affichage
 
    set(h(2),'Ydata',1000*w_new);
    drawnow 
%     %pause
    
end

%%
figure
plot((0:dt:(nt*dt)),masse_bout)
grid


