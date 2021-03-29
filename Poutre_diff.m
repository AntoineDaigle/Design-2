close all 
clear all
clc

%UNITÉS DU SI PARTOUT

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
%Amortissement
B = 5.91*(mu*L + 20e-3);

%Nombre d'incréments à calculer (par exemple, 0 à 11000 bonds de dt dans la
%simulation)
nx = 20;
nt = 8000;

%Incréments
dt = 2e-5;
dx = L/(nx-1);



%Liste d'éléments spaciaux
x = -dx:dx:L+dx; 
nx = nx + 2; %Nombre d'elements



% if(mu_simu > 0.5)
%     warning("La simulation ne sera pas stable")
% end

%Array de force appliquée
F = zeros(1, nx);
F(11) = -100e-3*9.81;
% F(20) = -0.588;

w = 1 * fliplr(0.001*sin(pi*x/(2*L)));

%Initialisation des arrays d'état passé, présent et futur
w_old = zeros(1, nx);
w = zeros(1, nx);
w_new = zeros(1, nx);

%Forme initiale de lame
w_init = zeros(1, nx); 

%Position du bout de la lame en fonction du temps
position_bout = zeros(1, nt+1); 

%Pour l'EDO
coeff1 = (E * J)/(dx^4);
coeff2 = mu/(dt^2);
coeff3 = B/dt;
coeff4 = ((mu/dt^2)+(B/dt))^(-1);

% Figure animée du bout de la lame
% h2 = plot(0:nt, position_bout);
% xlabel("temps [s]")
% ylabel("Déflexion [m]")
% ylim([-0.01,0.01])
% grid on

%Figure qui sera animée
h = plot(x, w_init, x, w_new);
xlabel("X [m]")
ylabel("Déflexion [m]")
ylim([-0.01,0.01])
grid on




for n = 0:nt
    i = 3:nx-2;
    
    w_new = zeros(1, nx);
    w_new(i) = (-coeff1*(w(i+2)-4*w(i+1)+6*w(i)-4*w(i-1)+w(i-2)) - coeff2*(-2*w(i)+w_old(i)) + coeff3*w(i) + F(i)/dx)*coeff4;
    
    %Déflexion à l'extrémité
    w_new(end-1) = 2*w(end-2)-w(end-3);
    w_new(end) = 2*w(end-1)-w(end-2);
    
    %Réassignations
    w_old = w;
    w = w_new;
    
    position_bout(n+1) = w(end);
    
    %set(h(2), "Ydata", w_new);
    drawnow
    %set(h2(1), "Ydata", position_bout);
    
end
figure 
plot((0:dt:(nt*dt)), position_bout)
grid on